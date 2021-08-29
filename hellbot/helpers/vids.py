import asyncio
import os
import re
import requests
import time
import zipfile

from bs4 import BeautifulSoup
import PIL.ImageOps
from PIL import Image
from validators.url import url

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions
from telethon.utils import get_input_document

from hellbot import LOGS, bot

# generate thumbnail from audio...
async def thumb_from_audio(audio_path, output):
    await runcmd(f"ffmpeg -i {audio_path} -filter:v scale=500:500 -an {output}")

# take a frame from video
async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + "/" + str(time.time()) + ".jpg"
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
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None

# trim vids
async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + "/" + str(round(time.time())) + ".mp4"
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
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        logger.info(e_response)
        logger.info(t_response)
        return None

#####################################
# for animated sticker to gif.....
#
# unzipper
async def unzip(downloaded_file_name):
    with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
        zip_ref.extractall("./temp")
    downloaded_file_name = os.path.splitext(downloaded_file_name)[0]
    return f"{downloaded_file_name}.gif"


# silent conv..
async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


# makes animated sticker to gif
async def make_gif(event, file):
    chat = "@tgstogifbot"
    async with event.client.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await event.client.send_file(chat, file)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return "`This file is not supported`"
            response = response if response.media else await conv.get_response()
            hellresponse = response if response.media else await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            hellfile = await event.client.download_media(hellresponse, "./temp")
            return await unzip(hellfile)
        except YouBlockedUserError:
            return "Unblock @tgstogifbot"


# Unsaves the gif from gif keyboard
async def unsave_gif(event, hgif):
    try:
        await bot(
            functions.messages.SaveGifRequest(
                id=get_input_document(hgif),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.info(e)


async def unsave_stcr(hstcr):
    try:
        await bot(
            functions.messages.SaveRecentStickerRequest(
                id=get_input_document(hstcr),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.info(e)


# hellbot
