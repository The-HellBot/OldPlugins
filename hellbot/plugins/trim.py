import asyncio
import datetime
import os
import time

from . import *

FF_MPEG_DOWN_LOAD_MEDIA_PATH = "./trim/hellbot.media.ffmpeg"


@hell_cmd(pattern="tsave$")
async def ff_mpeg_trim_cmd(event):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        reply_message = await event.get_reply_message()
        if reply_message:
            start = datetime.datetime.now()
            media = media_type(reply_message)
            if media not in ["Video", "Audio", "Voice", "Round Video", "Gif"]:
                return await eod(event, "`Only media files are supported`")
            hellevent = await eor(event, "`Saving the file...`")
            try:
                c_time = time.time()
                downloaded_file_name = await event.client.download_media(
                    reply_message,
                    FF_MPEG_DOWN_LOAD_MEDIA_PATH,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, hellevent, c_time, "trying to download")
                    ),
                )
            except Exception as e:
                await hellevent.edit(str(e))
            else:
                end = datetime.datetime.now()
                ms = (end - start).seconds
                await hellevent.edit(
                    f"Saved file to `{downloaded_file_name}` in `{ms}` seconds."
                )
        else:
            await eod(event, "`Reply to a any media file`")
    else:
        await eod(event, f"A media file already exists in path. Please remove the media and try again!\n`{hl}tclear`")


@hell_cmd(pattern="vtrim(?:\s|$)([\s\S]*)")
async def ff_mpeg_trim_cmd(event):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await eod(event,f"A media file needs to be download, and save to the following path:  `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")
        return
    hellevent = await eor(event, "`Triming the media......`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
        )
        if o is None:
            return await eod(hellevent, f"**Error : **`Can't complete the process`")
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hellevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await eod(hellevent, f"**Error : **`{e}`")
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await take_screen_shot(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH, Config.TMP_DOWNLOAD_DIRECTORY, start_time
        )
        if o is None:
            return await eod(hellevent, f"**Error : **`Can't complete the process`")
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hellevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await eod(hellevent, f"**Error : **`{e}`")
    else:
        await eod(hellevent, "RTFM")
        return
    end = datetime.datetime.now()
    ms = (end - start).seconds
    await eod(hellevent, f"`Completed Process in {ms} seconds`")


@hell_cmd(pattern="atrim(?:\s|$)([\s\S]*)")
async def ff_mpeg_trim_cmd(event):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await eod(event, f"A media file needs to be download, and save to the following path:  `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`")
        return
    hellevent = await eor(event, "`Triming the media.....`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.datetime.now()
    out_put_file_name = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, f"{str(round(time.time()))}.mp3"
    )
    if len(cmt) == 3:
        # output should be audio
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
            out_put_file_name,
        )
        if o is None:
            return await eod(hellevent, f"**Error : **`Can't complete the process`")
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hellevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await eod(hellevent, f"**Error : **`{e}`")
    else:
        await eod(hellevent, "RTFM")
        return
    end = datetime.datetime.now()
    ms = (end - start).seconds
    await eod(hellevent, f"`Completed Process in {ms} seconds`", 3)


@hell_cmd(pattern="tclear$")
async def ff_mpeg_trim_cmd(event):
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await eod(event, "`There is no media saved in bot for triming`")
    else:
        os.remove(FF_MPEG_DOWN_LOAD_MEDIA_PATH)
        await eod(event, f"Deleted saved trimming media. You can save new media by `{hl}tsave`")


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = os.path.join(output_directory, f"{str(time.time())}.jpg")
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name,
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None


# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26


async def cult_small_video(
    video_file, output_directory, start_time, end_time, out_put_file_name=None
):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = out_put_file_name or os.path.join(
        output_directory, f"{str(round(time.time()))}.mp4"
    )
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None


CmdHelp("trim").add_command(
  "tsave", "<reply to a media>", "Saves the media file in bot to trim mutliple times"
).add_command(
  "vtrim", "<time>", "Sends you the screenshot of the video at the given specific time"
).add_command(
  "vtrim", "<starttime> <endtime>", "Trims the saved media with specific given time interval and outputs as video"
).add_command(
  "atrim", "<starttime> <endtime>", "Trims the saved media with specific given time interval and output as audio"
).add_command(
  "tclean", None, "Deletes the saved media. So you can save new one🚶"
).add_info(
  "Trim Media By Ffmpeg."
).add_warning(
  "✅ Harmless Module."
).add()
