import os
import subprocess
import time
import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from hellbot.sql.gvar_sql import addgvar, delgvar, gvarstat
from . import *

thumb_image_path = Config.THUMB_IMG


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen(
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
    if not p.returncode and os.path.lexists(file):
        return output


@hell_cmd(pattern="rename(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[8:]
    if input_str == "":
        return await eod(event, "Give a new file name..")
    hell = await eor(event, f"Renaming it to `{input_str}`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message, downloaded_file_name
        )
        end = datetime.datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await hell.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )
        else:
            await eod(hell, "Error Occurred\n {}".format(input_str))
    else:
        await eod(hell, f"**Syntax Wrong !!** \n\n• `{hl}rename new file name` as reply to a Telegram file")

@hell_cmd(pattern="rnupload(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[10:]
    hell = await eor(event, f"Renaming to `{input_str}`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message, downloaded_file_name
        )
        end = datetime.datetime.now()
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            time.time()
            thumb = None
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            else:
                thumb = get_video_thumb(downloaded_file_name, thumb_image_path)
            await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
            )
            end_two = datetime.datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await hell.edit("Downloaded in {} seconds. Uploaded in {} seconds.".format(ms_one, ms_two))
        else:
            await eod(event, "File Not Found {}".format(input_str))
    else:
        await hell.edit(f"**Syntax Wrong !!** \n\n• `{hl}rnupload new file name`")

@hell_cmd(pattern="rnsupload(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "Rename & Upload as streamable format is in progress...")
    input_str = event.text[11:]
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        time.time()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await event.client.download_media(
            reply_message, downloaded_file_name
        )
        end_one = datetime.datetime.now()
        ms_one = (end_one - start).seconds
        if os.path.exists(downloaded_file_name):
            thumb = None
            if not downloaded_file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
                await eor(event, 
                    "Sorry. But I don't think {} is a streamable file. Please try again.\n**Supported Formats**: MKV, MP4, MP3, FLAC".format(
                        downloaded_file_name
                    )
                )
                return False
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            else:
                thumb = get_video_thumb(downloaded_file_name, thumb_image_path)
            start = datetime.datetime.now()
            metadata = extractMetadata(createParser(downloaded_file_name))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if os.path.exists(thumb_image_path):
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")

            try:
                await event.client.send_file(
                    event.chat_id,
                    downloaded_file_name,
                    thumb=thumb,
                    caption="reuploaded by HellBot",
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
                )
            except Exception as e:
                await hell.edit(event, str(e))
            else:
                end = datetime.datetime.now()
                os.remove(downloaded_file_name)
                ms_two = (end - end_one).seconds
                await hell.edit("Downloaded in {} seconds. Uploaded in {} seconds.".format(
                        ms_one, ms_two
                    )
                )
        else:
            await eod(hell, "File Not Found {}".format(input_str))
    else:
        await hell.edit(f"**Syntax Wrong !!** \n\n• `{hl}rnsupload new file name` as reply to a Telegram file")


CmdHelp("rename").add_command(
  "rename", "<reply to media> <new name>", "Renames the replied media and downloads it to userbot local storage"
).add_command(
  "rnupload", "<reply to media> <new name>", "Renames the replied media and directly uploads it to the chat"
).add_command(
  "rnsupload", "<reply to media> <new name>", "Renames the replied media and directly upload in streamable format."
).add_info(
  "Rename Yiur Files."
).add_warning(
  "✅ Harmless Module."
).add()
