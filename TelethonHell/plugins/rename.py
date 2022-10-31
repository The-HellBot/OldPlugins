import asyncio
import datetime
import os
import subprocess
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from TelethonHell.plugins import *


@hell_cmd(pattern="rename(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[8:]
    if input_str == "":
        return await eod(event, "Give a new file name.")
    hell = await eor(event, f"Renaming to `{input_str}`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str.strip()
        reply = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply,
                os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name),
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
        end = datetime.datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await hell.edit(f"**✅ Renamed File!!** \n\n__• File Path:__ `{downloaded_file_name}` \n__• Time taken:__ `{ms} seconds`")
        else:
            await parse_error(hell, "Unexpected Error Occured.")
    else:
        await eod(hell, f"**Syntax Wrong !!** \n\n• `{hl}rename new file name` as reply to a Telegram file")


@hell_cmd(pattern="rnupload(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[10:]
    if input_str == "":
        return await eod(event, "Give a new file name.")
    hell = await eor(event, f"Renaming to `{input_str}`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str.strip()
        reply = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply,
                os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name),
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
        end = datetime.datetime.now()
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            thumb = None
            if os.path.exists(Config.THUMB_IMG):
                thumb = Config.THUMB_IMG
            else:
                thumb = get_video_thumb(downloaded_file_name, Config.THUMB_IMG)
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Uploading ...", downloaded_file_name)
                ),
            )
            end_two = datetime.datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await hell.edit(f"**✅ Renamed File!!** \n\n__• Renamed to:__ `{file_name}` \n__• Download time:__ `{ms_one} seconds` \n__• Upload time:__ `{ms_two} seconds` \n__• Total time:__ `{ms_one + ms_two} seconds`")
        else:
            await parse_error(hell, "Unexpected Error Occured.")
    else:
        await hell.edit(f"**Syntax Wrong !!** \n\n• `{hl}rnupload new file name` as reply to a telegram file.")


@hell_cmd(pattern="rnsupload(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[11:]
    if input_str == "":
        return await eod(event, "Give a new file name.")
    hell = await eor(event, f"Renaming to `{input_str}`")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        file_name = input_str.strip()
        reply = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply,
                os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name),
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
        end_one = datetime.datetime.now()
        ms_one = (end_one - start).seconds
        if os.path.exists(downloaded_file_name):
            if not downloaded_file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
                return await parse_error(event, "__Only__ `.mkv`, `.mp4`, `.mp3`, `.flac` __supports streaming upload.__", False)
            thumb = None
            if os.path.exists(Config.THUMB_IMG):
                thumb = Config.THUMB_IMG
            else:
                thumb = get_video_thumb(downloaded_file_name, Config.THUMB_IMG)
            start = datetime.datetime.now()
            metadata = extractMetadata(createParser(downloaded_file_name))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if os.path.exists(Config.THUMB_IMG):
                metadata = extractMetadata(createParser(Config.THUMB_IMG))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")

            try:
                await event.client.send_file(
                    event.chat_id,
                    downloaded_file_name,
                    thumb=thumb,
                    caption=f"`{file_name}`",
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
                        progress(d, t, hell, c_time, "Uploading ...", downloaded_file_name)
                    ),
                )
            except Exception as e:
                await parse_error(event, e)
            else:
                end = datetime.datetime.now()
                os.remove(downloaded_file_name)
                ms_two = (end - end_one).seconds
                await hell.edit(f"**✅ Renamed File!!** \n\n__• Renamed to:__ `{file_name}` \n__• Download time:__ `{ms_one} seconds` \n__• Upload time:__ `{ms_two} seconds` \n__• Total time:__ `{ms_one + ms_two} seconds`")
        else:
            await parse_error(hell, "Unexpected Error Occured.")
    else:
        await hell.edit(f"**Syntax Wrong !!** \n\n• `{hl}rnsupload new file name` as reply to a Telegram file")


CmdHelp("rename").add_command(
    "rename", "<reply to media> <new name>", "Renames the replied media and downloads it to userbot local storage"
).add_command(
    "rnupload", "<reply to media> <new name>", "Renames the replied media and directly uploads it to the chat"
).add_command(
    "rnsupload", "<reply to media> <new name>", "Renames the replied media and directly upload in streamable format."
).add_info(
    "Rename your files."
).add_warning(
    "✅ Harmless Module."
).add()
