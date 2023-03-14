import asyncio
import json
import os
import time

import yt_dlp
from telethon.tl.types import DocumentAttributeAudio
from TelethonHell.plugins import *


@hell_cmd(pattern="yt(a|v)(?:\s|$)([\s\S]*)")
async def download_video(event):
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Give a YT link to download.")
    url = lists[1].strip()
    type_ = lists[0][3:4]
    reply = await event.get_reply_message()
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "`Preparing to download...`")
    if type_ == "a":
        opts = song_opts
        video = False
        song = True
    elif type_ == "v":
        opts = video_opts
        song = False
        video = True
    if song:
        try:
            await hell.edit("**Fetching YT link...**")
            with yt_dlp.YoutubeDL(opts) as ytdl:
                ytdl_data = ytdl.extract_info(url)
                audio_file = ytdl.prepare_filename(ytdl_data)
                ytdl.process_info(ytdl_data)
            c_time = time.time()
            upload_txt = f"**••• Uploading Audio •••** \n\n__» {ytdl_data['title']}__\n__»»__ [{ytdl_data['uploader']}]({ytdl_data['uploader_url']})"
            await hell.edit(upload_txt)
            await event.client.send_file(
                event.chat_id,
                f"{audio_file}.mp3",
                supports_streaming=True,
                caption=f"**✘ Audio:** `{ytdl_data['title']}` \n**✘ Channel:** [{ytdl_data['uploader']}]({ytdl_data['uploader_url']}) \n**✘ Views:** `{ytdl_data['view_count']} views` \n\n**« ✘ »** {hell_mention}",
                reply_to=reply,
                attributes=[
                    DocumentAttributeAudio(
                        duration=int(ytdl_data["duration"]),
                        title=str(ytdl_data["title"]),
                        performer=perf,
                    )
                ],
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, hell, c_time, upload_txt, f"{ytdl_data['title']}.mp3"
                    )
                ),
            )
            os.remove(f"{audio_file}.mp3")
            os.remove(f"{audio_file}.webp")
            await hell.delete()
        except Exception as e:
            return await parse_error(hell, e)
    elif video:
        try:
            await hell.edit("**Fetching YT link...**")
            with yt_dlp.YoutubeDL(opts) as ydl:
                vid_file = ydl.extract_info(url, download=True)
            file_ = f"{vid_file['id']}.mp4"
            c_time = time.time()
            upload_txt = f"**••• Uploading Video •••** \n\n__» {vid_file['title']}__\n__»»__ [{vid_file['uploader']}]({vid_file['uploader_url']})"
            await hell.edit(upload_txt)
            await event.client.send_file(
                event.chat_id,
                open(file_, "rb"),
                supports_streaming=True,
                caption=f"**✘ Video:** `{vid_file['title']}` \n**✘ Channel:** [{vid_file['uploader']}]({vid_file['uploader_url']}) \n**✘ Views:** `{vid_file['view_count']} views` \n\n**« ✘ »** {hell_mention}",
                reply_to=reply,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, hell, c_time, upload_txt, f"{vid_file['title']}.mp4"
                    )
                ),
            )
            os.remove(file_)
            await hell.delete()
        except Exception as e:
            await parse_error(hell, e)


@hell_cmd(pattern="ytlink(?:\s|$)([\s\S]*)")
async def hmm(event):
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Give some texts to search on Youtube.")
    query = lists[1].strip()
    hell = await eor(event, "`Processing...`")
    try:
        results = json.loads(Hell_YTS(query, max_results=7).to_json())
    except KeyError:
        return await eod(event, "Unable to find relevant search queries...")
    output = f"**◈ Search Query:**\n`{query}`\n\n**◈ Results:**\n\n"
    for i in results["videos"]:
        output += f"⇝ __{i['title']}__\nhttps://www.youtube.com{i['url_suffix']}\n\n"
    await hell.edit(output, link_preview=False)


CmdHelp("youtube").add_command(
    "yta", "<yt link>", "Extracts the audio from given youtube link and uploads it to telegram"
).add_command(
    "ytv", "<yt link>", "Extracts the video from given youtube link and uploads it to telegram"
).add_command(
    "ytlink", "<search keyword>", "Extracts 7 links from youtube based on the given search query"
).add_info(
    "YouTube Utilities"
).add_warning(
    "✅ Harmless Module."
).add()
