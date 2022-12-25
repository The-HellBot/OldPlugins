import asyncio
import os
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from TelethonHell.plugins import *


@hell_cmd(pattern="upload(?:\s|$)([\s\S]*)")
async def upload(event):
    hell = await eor(event, "Uploader in action ...")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(hell, "Upload path not given.")
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
                progress(d, t, hell, c_time, "Uploading ...", file_path)
            ),
        )
        await eod(hell, f"__Uploaded__ `{file_path}` __successfully !!__")
    else:
        await eod(hell, "**404:** __File Not Found__")


@hell_cmd(pattern="uploadir(?:\s|$)([\s\S]*)")
async def uploadir(event):
    hell = await eor(event, "Uploader in action ...")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(hell, "Upload path not given.")
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
                            progress(d, t, hell, c_time, "Uploading ...", single_file)
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
                            progress(d, t, hell, c_time, "Uploading...", single_file)
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
    lists = event.text.split(" ", 2)
    if not len(lists) == 3:
        return await parse_error(hell, "Upload path or upload type not given.")
    type_of_upload = lists[1].strip()
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
                        progress(d, t, hell, c_time, "Uploading...", file_name)
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
                        progress(d, t, hell, c_time, "Uploading...", file_name)
                    ),
                )
            elif spam_big_messages:
                await eod(hell, "**TODO:** Not (yet) Implemented")
            os.remove(thumb)
            await eod(hell, f"__Uploaded__ `files` __successfully !!__")
        except FileNotFoundError as err:
            await eod(hell, f"**ERROR !!** \n\n`{str(err)}`")
    else:
        await hell.edit("**404:** __File Not Found__")


CmdHelp("uploads").add_command(
    "upload", "<path>", "Uploads a locally stored file to the chat"
).add_command(
    "uploadas stm", "<path>", "Uploads the locally stored video in streamable format."
).add_command(
    "uploadas vnr", "<path>", "Uploads the locally stored video in video note format."
).add_command(
    "uploadir", "<path>", "Uploads all the files in directory"
).add_info(
    "File upload from bot's server."
).add_warning(
    "✅ Harmless Module."
).add()
