import asyncio
import json
import os
import requests
import subprocess
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from . import *


@hell_cmd(pattern="upload(?:\s|$)([\s\S]*)")
async def upload(event):
    hell = await eor(event, "Uploader in action ...")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    if not len(lists) >= 2:
        return await eod(hell, f"**WRONG SYNTAX !!** \n\n`{hl}upload <path>`")
    file_path = lists[1]
    if file_path in INVALID_UPLOAD:
        return await eod(hell, "For security reasons this file is prohibited for uploading.")
    if os.path.exists(file_path):
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            file_path,
            force_document=True,
            allow_cache=False,
            reply_to=reply,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading ...", file_path)
            ),
        )
        await eod(hell, f"__Uploaded__ `{file_path}` __successfully !!__")
    else:
        await eod(hell, "**404:** __File Not Found__")


@hell_cmd(pattern="uploadir(?:\s|$)([\s\S]*)")
async def uploadir(event):
    hell = await eor(event, "Uploader in action ...")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    if not len(lists) >= 2:
        return await eod(hell, f"**WRONG SYNTAX !!** \n\n`{hl}uploadir <directory path>`")
    file_path = lists[1]
    if os.path.exists(file_path):
        lst_of_files = []
        for r, d, f in os.walk(file_path):
            for file in f:
                lst_of_files.append(os.path.join(r, file))
            for file in d:
                lst_of_files.append(os.path.join(r, file))
        LOGS.info(lst_of_files)
        uploaded = 0
        await hell.edit(f"__Starting to Upload..__ \n**Total Files:** `{len(lst_of_files)}`")
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=reply,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "Uploading ...", single_file)
                        ),
                    )
                else:
                    thumb_image = Config.THUMB_IMG
                    c_time = time.time()
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        thumb=thumb_image,
                        force_document=False,
                        allow_cache=False,
                        reply_to=reply,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "Uploading...", single_file)
                        ),
                    )
                os.remove(single_file)
                uploaded += 1
        await eod(hell, f"__Uploaded__ `{uploaded} files` __successfully !!__")
    else:
        await eod(hell, "**404:** __Directory Not Found__")


@hell_cmd(pattern="uploadas(?:\s|$)([\s\S]*)")
async def uploadas(event):
    hell = await eor(event, "Uploader in action ...")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 3)
    if not len(lists) >= 3:
        return await eod(hell, f"**WRONG SYNTAX:** \n\n`{hl}uploadas <stm/vnr/all> <path>`")
    type_of_upload = lists[1]
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stm":
        supports_streaming = True
    if type_of_upload == "vnr":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    file_path = lists[2]
    thumb = None
    file_name = file_path
    thumb_path = "hell_thumb" + ".jpg"
    thumb = get_video_thumb(file_name, output=thumb_path)
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await event.client.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=file_name,
                    force_document=False,
                    allow_cache=False,
                    reply_to=reply,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, c_time, "Uploading...", file_name)
                    ),
                )
            elif round_message:
                c_time = time.time()
                await event.client.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=reply,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, c_time, "Uploading...", file_name)
                    ),
                )
            elif spam_big_messages:
                await eod(hell, "**TODO:** Not (yet) Implemented")
            os.remove(thumb)
            await eod(hell, f"__Uploaded__ `{uploaded} files` __successfully !!__")
        except FileNotFoundError as err:
            await eod(hell, f"**ERROR !!** \n\n`{str(err)}`")
    else:
        await hell.edit("**404:** __File Not Found__")


@hell_cmd(pattern="webup(?:\s|$)([\s\S]*)")
async def labstack(event):
    hell = await eor(event, "Uploader in action ...")
    lists = event.text.split(" ", 2)
    reply = await event.get_reply_message()
    if reply:
        filebase = await event.client.download_media(reply.media, Config.TMP_DOWNLOAD_DIRECTORY)
    elif len(lists) >= 2:
        filebase = lists[1]
    else:
        return await eod(hell, f"**WRONG SYNTAX:** \n\n`{hl}webup <path or reply>`")
    filesize = os.path.getsize(filebase)
    filename = os.path.basename(filebase)
    headers2 = {"Up-User-ID": "IZfFbjUcgoo3Ao3m"}
    files2 = {
        "ttl": 604800,
        "files": [{"name": filename, "type": "", "size": filesize}],
    }
    r2 = requests.post("https://up.labstack.com/api/v1/links", json=files2, headers=headers2)
    r2json = json.loads(r2.text)
    url = f"https://up.labstack.com/api/v1/links/{r2json['code']}/send"
    max_days = 7
    command_to_exec = [
        "curl",
        "-F",
        "files=@" + filebase,
        "-H",
        "Transfer-Encoding: chunked",
        "-H",
        "Up-User-ID: IZfFbjUcgoo3Ao3m",
        url,
    ]
    try:
        logger.info(command_to_exec)
        t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        logger.info("Status : FAIL", exc.returncode, exc.output)
        await eod(hell, f"**ERROR !!** \n\n`{exc.output.decode('UTF-8')}`")
        return
    else:
        logger.info(t_response)
        t_response_arry = f"https://up.labstack.com/api/v1/links/{r2json['code']}/receive"
    await eor(hell, f"{t_response_arry} \nMax Days: {str(max_days)}", link_preview=False)


CmdHelp("uploads").add_command(
    "upload", "<path>", "Uploads a locally stored file to the chat"
).add_command(
    "uploadas stm", "<path>", "Uploads the locally stored video in streamable format."
).add_command(
    "uploadas vnr", "<path>", "Uploads the locally stored video in video note format."
).add_command(
    "uploadir", "<path>", "Uploads all the files in directory"
).add_command(
    "webup", "<reply to media>", "Makes a direct download link of the replied media for a limited time"
).add_info(
    "File upload from bot's server."
).add_warning(
    "✅ Harmless Module."
).add()
