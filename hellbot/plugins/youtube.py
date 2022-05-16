import asyncio
import json
import os
import time
import yt_dlp

from telethon.tl.types import DocumentAttributeAudio

from . import *


@hell_cmd(pattern="yt(a|v)(?:\s|$)([\s\S]*)")
async def download_video(event):
    url = event.text[5:]
    type_ = event.text[3:4]
    reply = await event.get_reply_message()
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
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
            await hell.edit(f"**••• Uploading Audio •••** \n\n__» {ytdl_data['title']}__\n__»» {ytdl_data['uploader']}__")
            await event.client.send_file(
                event.chat_id,
                audio_file,
                supports_streaming=True,
                caption=f"**✘ Audio -** `{ytdl_data['title']}` \n**✘ Views -** `{ytdl_data['views']}` \n\n**« ✘ »** {hell_mention}",
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
                        d, t, event, c_time, "Uploading..", f"{ytdl_data['title']}.mp3"
                    )
                ),
            )
            os.remove(audio_file)
            await hell.delete()
        except Exception as e:
            return await eod(hell, f"**ERROR:** \n`{str(e)}`")
    elif video:
        try:
            await hell.edit("**Fetching YT link...**")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                vid_file = ydl.extract_info(url, download=True)
            file_ = f"{vid_file['id']}.mp4"
            await hell.edit(f"**••• Uploading Video •••** \n\n__» {vid_file['title']}__\n__»» {vid_file['uploader']}__")
            await event.client.send_file(
                event.chat_id,
                open(file_, "rb"),
                supports_streaming=True,
                caption=f"**✘ Video -** `{vid_file['title']}` \n**✘ Views -** `{vid_file['views']}` \n\n**« ✘ »** {hell_mention}",
                reply_to=reply,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d, t, event, c_time, "Uploading..", f"{vid_file['title']}.mp4"
                    )
                ),
            )
            os.remove(file_)
            await hell.delete()
        except Exception as e:
            await eod(hell, f"**ERROR:** \n`{str(e)}`")


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
        output += f"--> `{i['title']}`\nhttps://www.youtube.com{i['url_suffix']}\n\n"
    await event.edit(output, link_preview=False)


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
