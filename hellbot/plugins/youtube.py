import asyncio
import json
import os
import re
import time

from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError, DownloadError, ExtractorError, GeoRestrictedError, MaxDownloadsReached, PostProcessingError, UnavailableVideoError, XAttrMetadataError

from . import *


@hell_cmd(pattern="yt(a|v)(?:\s|$)([\s\S]*)")
async def download_video(event):
    url = event.text[5:]
    type_ = event.text[3:4]
    event = await eor(event, "`Preparing to download...`")
    if type_ == "a":
        opts = song_opts
        video = False
        song = True
    elif type_ == "v":
        opts = video_opts
        song = False
        video = True
    try:
        await event.edit("**Fetching YT link...**")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await eod(event, f"`{str(DE)}`")
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
        await eod(event, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
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
        await event.client.send_file(
            event.chat_id,
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
                    d, t, event, c_time, "Uploading..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
        await event.delete()
    elif video:
        await eor(event, 
            f"`Preparing to upload video:`\
        \n\n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await event.client.send_file(
            event.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, event, c_time, "Uploading..", f"{ytdl_data['title']}.mp4"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
        await event.delete()


@hell_cmd(pattern="ytlink(?:\s|$)([\s\S]*)")
async def hmm(event):
    query = event.text[8:]
    if query == "":
        await eod(event, "`Enter query to search on yt`")
    event = await eor(event, "`Processing...`")
    try:
        results = json.loads(Hell_YTS(query, max_results=7).to_json())
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
