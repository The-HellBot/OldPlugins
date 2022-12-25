import asyncio
import datetime
import os
import time

from TelethonHell.plugins import *


async def trimmer(file, out_dir, start, end=None, file_name=None):
    if end:
        file_name = file_name or os.path.join(out_dir, f"{str(round(time.time()))}.mp4")
        command = [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            start,
            "-to",
            end,
            "-async",
            "1",
            "-strict",
            "-2",
            file_name,
        ]
    else:
        file_name = os.path.join(out_dir, f"{str(time.time())}.jpg")
        command = [
            "ffmpeg",
            "-ss",
            str(start),
            "-i",
            file,
            "-vframes",
            "1",
            file_name,
        ]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    if os.path.lexists(file_name):
        return file_name
    return None


@hell_cmd(pattern="vtrim(?:\s|$)([\s\S]*)")
async def video(event):
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    hell = await eor(event, "Starting video trim ...")
    reply = await event.get_reply_message()
    if not reply:
        return await parse_error(hell, "Reply to a video/gif to trim.")
    dl_start = datetime.datetime.now()
    media = media_type(reply)
    if media not in ["Video", "Round Video", "Gif"]:
        return await parse_error(hell, "Only video/gif is supported.")
    await hell.edit("Starting to download media ...")
    try:
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, hell, c_time, "Downloading ...")
            ),
        )
    except Exception as e:
        return await parse_error(hell, e)
    else:
        dl_end = datetime.datetime.now()
        dl_ms = (dl_end - dl_start).seconds
        await hell.edit(f"**Downloaded Media !** \n\n__◈ Path:__ `{downloaded_file_name}` \n__◈ Time Taken:__ `{dl_ms} seconds`\n\n__Starting to trim video ...__")
    lists = event.text.split(" ")
    start = datetime.datetime.now()
    if len(lists) == 3:
        start_time = lists[1].strip()
        end_time = lists[2].strip()
        o = await trimmer(
            downloaded_file_name,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
        )
        if o is None:
            return await parse_error(hell, f"Unexpected error occured.")
        try:
            await hell.edit("**Trimmed!** Uploading now ...")
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=f"**Trimmed:** `{start_time} to {end_time}`",
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "**Trimmed!** Uploading now ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
    elif len(lists) == 2:
        start_time = lists[1].strip()
        o = await trimmer(
            downloaded_file_name,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
        )
        if o is None:
            return await parse_error(hell, "Unexpected error occured.")
        try:
            await hell.edit("**Screenshot Completed!** Uploading now ...")
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=f"**Screeenshot Completed:** `{start_time}`",
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "**Screenshot Completed!** Uploading now ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
    else:
        return await parse_error(hell, f"__Give proper command:__ \n__Example:__ `{hl}vtrim 60 70`", False)
    end = datetime.datetime.now()
    ms = (end - start).seconds
    await eod(hell, f"**Trimmed!!**\n__Time taken:__ `{ms} seconds`")
    os.remove(downloaded_file_name)
    os.remove(o)


@hell_cmd(pattern="atrim(?:\s|$)([\s\S]*)")
async def audio(event):
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    hell = await eor(event, "Starting audio trim ...")
    reply = await event.get_reply_message()
    if not reply:
        return await parse_error(hell, "Reply to a media file to trim.")
    dl_start = datetime.datetime.now()
    media = media_type(reply)
    if media not in ["Video", "Audio", "Voice", "Round Video", "Gif"]:
        return await parse_error(hell, "Only media file is supported.")
    await hell.edit("Starting to download media ...")
    try:
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, hell, c_time, "Downloading ...")
            ),
        )
    except Exception as e:
        return await parse_error(hell, e)
    else:
        dl_end = datetime.datetime.now()
        dl_ms = (dl_end - dl_start).seconds
        await hell.edit(f"**Downloaded Media !** \n\n__◈ Path:__ `{downloaded_file_name}` \n__◈ Time Taken:__ `{dl_ms} seconds`\n\n__Starting to trim audio ...__")
    file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, f"{str(round(time.time()))}.mp3")
    lists = event.text.split(" ")
    start = datetime.datetime.now()
    if len(lists) == 3:
        start_time = lists[1].strip()
        end_time = lists[2].strip()
        o = await trimmer(
            downloaded_file_name,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
            file_name,
        )
        if o is None:
            return await parse_error(hell, "Unexpected error occured.")
        try:
            await hell.edit("**Trimmed !!** Uploading now ...")
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=f"**Trimmed:** `{start_time} to {end_time}`",
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "**Trimmed !!** Uploading now ...")
                ),
            )
        except Exception as e:
            return await parse_error(hell, e)
    else:
        return await parse_error(hell, f"__Give proper command:__ \n__Example:__ `{hl}atrim 60 70`", False)
    end = datetime.datetime.now()
    ms = (end - start).seconds
    await eod(hell, f"**Trimmed!!**\n__Time taken:__ `{ms} seconds`")
    os.remove(downloaded_file_name)
    os.remove(o)


CmdHelp("trim").add_command(
    "vtrim", "<start time> <end time>", "Trimes replied video within given time stamps. To generate a screenshot given single time-stamp."
).add_command(
    "atrim", "<starttime> <endtime>", "Trimes replied media within given time stamps and gives audio file as output."
).add_info(
    "Trim & Screenshot."
).add_warning(
    "✅ Harmless Module."
).add()
