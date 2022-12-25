import asyncio
import datetime
import math
import os
import subprocess
import time

from pySmartDL import SmartDL
from TelethonHell.plugins import *


@hell_cmd(pattern="download(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "Downloader in action ...")
    _, _, hell_mention = await client_id(event)
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        reply = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await parse_error(hell, e)
        else:
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await hell.edit(
                f"**Downloading Completed !!**\n**• Downloaded to:** `{downloaded_file_name}`\n**Time Taken:** `{ms} seconds` \n**• Downloaded by:** {hell_mention}"
            )
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
                current_message = f"**Downloading the file**\n\
                                \n__URL:__ `{url}`\
                                \n__File Name:__ `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)}` __of__ `{humanbytes(total_length)}`\
                                \n__ETA:__ `{estimated_total_time}`"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await hell.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
        end = datetime.datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await hell.edit(
                f"**Downloading Completed !!**\n**• Downloaded to:** `{downloaded_file_name}`\n**Time Taken:** `{ms} seconds` \n**• Downloaded by:** {hell_mention}"
            )
        else:
            await parse_error(hell, f"__Incorrect URL:__ {input_str}", False)
    else:
        await eod(hell, f"**WRONG SYNTAX:** \n\n`{hl}download <reply or url>`")


@hell_cmd(pattern="getc(?:\s|$)([\s\S]*)")
async def get_media(event):
    dir = "./channel_dl/"
    if not os.path.isdir(dir):
        os.makedirs(dir)
    lists = event.text.split(" ", 3)
    if not len(lists) >= 3:
        return await eod(event, "Invalid command.")
    limit = lists[1]
    channel_username = lists[2]
    hell = await eor(event, f"Downloading medias from {channel_username} channel.")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "channel_dl"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await hell.edit("Downloaded " + output + " files.")


@hell_cmd(pattern="geta(?:\s|$)([\s\S]*)")
async def get_media(event):
    dir = "./channel_dl/"
    if not os.path.isdir(dir):
        os.makedirs(dir)
    lists = event.text.split(" ", 2)
    if not len(lists) >= 2:
        return await eod(event, "Invalid command.")
    hell = await eor(event, f"Downloading All Media From {lists[1]} Channel.")
    msgs = await event.client.get_messages(lists[1], limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "channel_dl"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await hell.edit("Downloaded " + output + " files.")


CmdHelp("downloads").add_command(
    "download", "<link | filename> or <reply to media>", "Downloads the replied file or file from given url to bot's server"
).add_command(
    "geta", "channel username", "Will download all media from channel into your bot server but there is limit of 3000 to prevent API limits."
).add_command(
    "getc", "<limit> <channel username>", "Will download latest given number of media from channel into your bot server", "getc 10 @Its_HellBot"
).add_info(
    "File download to bot's server."
).add_warning(
    "✅ Harmless Module."
).add()
