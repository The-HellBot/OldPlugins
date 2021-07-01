import re
import random
import json
from pathlib import Path
import asyncio
import math
import os
import time

from telethon.tl.types import DocumentAttributeAudio

from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from . import *


@bot.on(hell_cmd(pattern="yt(a|v) (.*)"))
@bot.on(sudo_cmd(pattern="yt(a|v) (.*)", allow_sudo=True))
async def download_video(v_url):
    if v_url.fwd_from:
        return
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    event = await eor(v_url, "`Preparing to download...`")

    if type == "a":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True

    try:
        await event.edit("**Fetching YT link...**")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await edit_or_reply(v_url, f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await eod(event, "`The download content was too short.`")
        return
    except GeoRestrictedError:
        await eod(event, 
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await eod(event, "`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await eod(event, "`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await eod(event, "`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await edit_or_reply(v_url, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await eod(event, "`There was an error during info extraction.`")
        return
    except Exception as e:
        await eod(event, f"{str(type(e)): {str(e)}}", 10)
        return
    c_time = time.time()
    if song:
        await eor(event, 
            f"📤 `Preparing to upload audio:`\
        \n\n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=perf,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, "Uploading..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await eor(event, 
            f"`Preparing to upload video:`\
        \n\n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, "Uploading..", f"{ytdl_data['title']}.mp4"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
        await v_url.delete()


@bot.on(hell_cmd(pattern="ytlink ?(.*)"))
@bot.on(sudo_cmd(pattern="ytlink ?(.*)", allow_sudo=True))
async def hmm(ytwala):
    query = ytwala.pattern_match.group(1)
    if not query:
        await eod(ytwala, "`Enter query to search on yt`")
    event = await eor(ytwala, "`Processing...`")
    try:
        results = json.loads(YoutubeSearch(query, max_results=7).to_json())
    except KeyError:
        return await eod(event, "Unable to find relevant search queries...")
    output = f"**Search Query:**\n`{query}`\n\n**Results:**\n\n"
    for i in results["videos"]:
        output += (f"--> `{i['title']}`\nhttps://www.youtube.com{i['url_suffix']}\n\n")
    await event.edit(output, link_preview=False)


CmdHelp("youtube").add_command(
  "yta", "<yt link>", "Extracts the audio from given youtube link and uploads it to telegram"
).add_command(
  "ytv", "<yt link>", "Extracts the video from given youtube link and uploads it to telegram"
).add_command(
  "ytlink", "<search keyword>", "Extracts 7 links from youtube based on the given search query"
).add_info(
  "Youthoob ki duniya."
).add_warning(
  "✅ Harmless Module."
).add()
