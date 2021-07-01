import asyncio
import re
import json
import os
import time

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio
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
try:
    from youtubesearchpython import SearchVideos
except:
    os.system("pip install pip install youtube-search-python")
    from youtubesearchpython import SearchVideos

from . import *

@bot.on(hell_cmd(pattern="lyrics(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="lyrics(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.pattern_match.group(1)
    await eor(kraken, f"Searching lyrics for  `{hell}` ...")
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(kraken, "Give song name to get lyrics...")
            return

    troll = await bot.inline_query("iLyricsBot", f"{(deEmojify(hell))}")

    await troll[0].click(
        kraken.chat_id,
        reply_to=kraken.reply_to_msg_id,
        silent=True if kraken.is_reply else False,
        hide_via=True,
    )

    await kraken.delete()
    

@bot.on(hell_cmd(pattern="song(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="song(?: |$)(.*)", allow_sudo=True))
async def download_video(v_url):
    lazy = v_url
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()

    if not sender.id == me.id:
        rkp = await eor(lazy, "`Wait. Processing your request....`")
    else:
        rkp = await eor(lazy, "`Wait. Processing your request....`")
    url = v_url.pattern_match.group(1)
    if not url:
        return await eod(rkp, f"**Error** \n__Usage:__ `{hl}song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except:
        return await eod(rkp, "`Failed to process your request....`")
    type = "audio"
    await rkp.edit("Request processed. **Downloading Now!!!**")
    if type == "audio":
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
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    try:
        await rkp.edit("**Fetching Song**")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await eod(rkp, f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await eod(rkp, "`The download content was too short.`")
        return
    except GeoRestrictedError:
        await eod(rkp,
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await eod(rkp, "`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await eod(rkp, "`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await eod(rkp, "`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await eod(rkp, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await eod(rkp, "`There was an error during info extraction.`")
        return
    except Exception as e:
        await eod(rkp, f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(
            f"🎶 Preparing to upload song 🎶 :-\
        \n\n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(rip_data["duration"]),
                    title=str(rip_data["title"]),
                    performer=perf,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp3")
            ),
        )
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await rkp.edit(
            f"🎶 Preparing to upload song 🎶 :-\
        \n\n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=url,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp4")
            ),
        )
        os.remove(f"{rip_data['id']}.mp4")
        await rkp.delete()


@bot.on(hell_cmd(pattern="vsong(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="vsong(?: |$)(.*)", allow_sudo=True))
async def download_video(v_url):
    lazy = v_url
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await eor(lazy, "Processing video song request....")
    else:
        rkp = await eor(lazy, "Processing video song request....")
    url = v_url.pattern_match.group(1)
    if not url:
        return await eod(rkp, f"**Error** \n__Usage:__ `{hl}vsong <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except:
        return await eod(rkp, "`failed to find`")
    type = "audio"
    await rkp.edit("Video Song Request Processed. **Downloading Now!!**")
    if type == "audio":
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
        await rkp.edit("Fetching Video Song")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await eod(rkp, f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await eod(rkp, "`The download content was too short.`")
        return
    except GeoRestrictedError:
        await eod(rkp,
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await eod(rkp, "`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await eod(rkp, "`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await eod(rkp, "`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await eod(rkp, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await eod(rkp, "`There was an error during info extraction.`")
        return
    except Exception as e:
        await eod(rkp, f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(
            f"🎶 Preparing to upload video song 🎶 :-\
        \n\n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(rip_data["duration"]),
                    title=str(rip_data["title"]),
                    performer=perf,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp3")
            ),
        )
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await rkp.edit(
            f"🎶 Preparing to upload video song 🎶 :-\
        \n\n**{rip_data['title']}**\
        \nby __{rip_data['uploader']}__"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp4")
            ),
        )
        os.remove(f"{rip_data['id']}.mp4")
        await rkp.delete()


CmdHelp("songs").add_command(
	"song", "<song name>", "Downloads the song from YouTube."
).add_command(
	"vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
	"lyrics", "<song name>", "Gives the lyrics of that song.."
).add_info(
	"Songs & Lyrics."
).add_warning(
	"✅ Harmless Module."
).add()
