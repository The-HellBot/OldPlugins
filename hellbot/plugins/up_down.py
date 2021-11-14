import asyncio
import datetime
import json
import math
import os
import requests
import subprocess
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pySmartDL import SmartDL
from telethon.tl.types import DocumentAttributeVideo

from . import *

@hell_cmd(pattern="webup(?:\s|$)([\s\S]*)")
async def labstack(event):
    await eor(event, "Processing...")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filebase = input_str
    elif reply:
        filebase = await event.client.download_media(
            reply.media, Config.TMP_DOWNLOAD_DIRECTORY
        )
    else:
        await eod(event, "Reply to a media file or provide a directory to upload the file to labstack"
        )
        return
    filesize = os.path.getsize(filebase)
    filename = os.path.basename(filebase)
    headers2 = {"Up-User-ID": "IZfFbjUcgoo3Ao3m"}
    files2 = {
        "ttl": 604800,
        "files": [{"name": filename, "type": "", "size": filesize}],
    }
    r2 = requests.post(
        "https://up.labstack.com/api/v1/links", json=files2, headers=headers2
    )
    r2json = json.loads(r2.text)

    url = "https://up.labstack.com/api/v1/links/{}/send".format(r2json["code"])
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
        await eor(event, exc.output.decode("UTF-8"))
        return
    else:
        logger.info(t_response)
        t_response_arry = "https://up.labstack.com/api/v1/links/{}/receive".format(
            r2json["code"]
        )
    await eor(event, t_response_arry + "\nMax Days:" + str(max_days), link_preview=False
    )

@hell_cmd(pattern="upld_dir(?:\s|$)([\s\S]*)")
async def uploadir(event):
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        hell = await eor(event, "Downloading Using Userbot Server....")
        lst_of_files = []
        for r, d, f in os.walk(input_str):
            for file in f:
                lst_of_files.append(os.path.join(r, file))
            for file in d:
                lst_of_files.append(os.path.join(r, file))
        LOGS.info(lst_of_files)
        uploaded = 0
        await hell.edit("Found {} files. Uploading will start soon. Please wait!".format(len(lst_of_files)))
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=event.message.id,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d,
                                t,
                                event,
                                c_time,
                                "Uploading in Progress.......",
                                single_file,
                            )
                        ),
                    )
                else:
                    thumb_image = os.path.join(input_str, "thumb.jpg")
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
                        reply_to=event.message.id,
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
                            progress(
                                d, t, event, c_time, "Uploading...", single_file
                            )
                        ),
                    )
                os.remove(single_file)
                uploaded = uploaded + 1
        await hell.edit("Uploaded {} files successfully !!".format(uploaded))
    else:
        await hell.edit("404: Directory Not Found")

@hell_cmd(pattern="upload(?:\s|$)([\s\S]*)")
async def upload(event):
    hell = await eor(event, "Processing ...")
    input_str = event.pattern_match.group(1)
    cap = "Chala Jaa Bhosdike. Hack hona h kya tujhe"
    if input_str == "config.env":
        await event.client.send_file(event.chat_id, cjb, caption=cap)
        await event.delete()
        return
    if os.path.exists(input_str):
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "Uploading...", input_str)
            ),
        )
        await hell.edit("Uploaded successfully !!")
    else:
        await hell.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    """ Get video thumbnail """
    metadata = extractMetadata(createParser(file))
    popen = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            "-filter:v",
            "scale={}:-1".format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not popen.returncode and os.path.lexists(file):
        return output
    return None


def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@hell_cmd(pattern="upld_as_(stm|vnr|all)(?:\s|$)([\s\S]*)")
async def uploadas(event):
    hell = await eor(event, "Processing ...")
    type_of_upload = event.text[9:12]
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stm":
        supports_streaming = True
    if type_of_upload == "vnr":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    input_str = event.text[13:]
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb_path = "a_random_f_file_name" + ".jpg"
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
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
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
                    reply_to=event.message.id,
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
                await hell.edit("TBD: Not (yet) Implemented")
                return
            os.remove(thumb)
            await hell.edit("Uploaded successfully !!")
        except FileNotFoundError as err:
            await hell.edit(str(err))
    else:
        await hell.edit("404: File Not Found")

@hell_cmd(pattern="download(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "`Processing ...`")
    cid = await client_id(event)
    hell_mention = cid[2]
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "trying to download")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await hell.edit(str(e))
        else:
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await hell.edit(f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- ** `{downloaded_file_name}`\n**•  Downloaded by :-** {hell_mention}")
    elif input_str:
        start = datetime.datetime.now()
        url = input_str
        file_name = os.path.basename(url)
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        if "|" in input_str:
            url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            downloader.get_speed()
            progress_str = "`{0}{1} {2}`%".format(
                "".join(["▰" for i in range(math.floor(percentage / 5))]),
                "".join(["▱" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2),
            )
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"Downloading the file\
                                \n\n**URL : **`{url}`\
                                \n**File Name :** `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)} of {humanbytes(total_length)}`\
                                \n**ETA : **`{estimated_total_time}``"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await hell.edit(current_message)
                    display_message = current_message
            except Exception as e:
                logger.info(str(e))
        end = datetime.datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await hell.edit(
                f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- ** `{downloaded_file_name}`"
            )
        else:
            await hell.edit("Incorrect URL\n {}".format(input_str))
    else:
        await hell.edit("Reply to a message to download to my local server.")


CmdHelp("up_down").add_command(
  "upload", "<path>", "Uploads a locally stored file to the chat"
).add_command(
  "upld_as_stm", "<path>", "Uploads the locally stored file in streamable format"
).add_command(
  "upld_as_vnr", "<path>", "Uploads the locally stored file in vs format"
).add_command(
  "upld_dir", "<path>", "Uploads all the files in directory"
).add_command(
  "download", "<link/filename> or reply to media", "Downloads the file to the server"
).add_command(
  "webup", "<reply to media>", "Makes a direct download link of the replied media for a limited time"
).add_info(
  "Upload & Download."
).add_warning(
  "✅ Harmless Module."
).add()
