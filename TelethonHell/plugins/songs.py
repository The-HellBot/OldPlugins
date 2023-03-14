import asyncio
import os
import shutil
import time

import requests
import yt_dlp
from lyricsgenius import Genius
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio
from TelethonHell.plugins import *


@hell_cmd(pattern="song(?:\s|$)([\s\S]*)")
async def songs(event):
    ForGo10God, _, hell_mention = await client_id(event)
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Nothing given to search.")
    reply = await event.get_reply_message()
    query = lists[1].strip()
    if not query:
        return await parse_error(event, "Nothing given to search.")
    hell = await eor(event, f"<b><i>Searching “ {query} ”</i></b>", parse_mode="HTML")
    try:
        song_dict = await song_search(hell, query, 1)
        link = song_dict[1]['link']
        title = song_dict[1]['title']
        views = song_dict[1]['views']
        channel = song_dict[1]['channel']
        duration = song_dict[1]['duration']
        thumbnail = song_dict[1]['thumbnail']
        thumb_name = f'thumb{ForGo10God}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
    except Exception as e:
        return await parse_error(hell, f"__No song found. Maybe give different name or check spelling.__ \n`{str(e)}`", False)
    try:
        upload_text = f"**••• Uploading Song •••** \n\n__» {title}__\n__»» {channel}__"
        with yt_dlp.YoutubeDL(song_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        await hell.edit(upload_text)
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            f"{audio_file}.mp3",
            supports_streaming=True,
            caption=f"**✘ Song -** [{title}]({link}) \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**« ✘ »** {hell_mention}",
            thumb=thumb_name,
            reply_to=reply,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, hell, c_time, upload_text)
            ),
            attributes=[
                DocumentAttributeAudio(
                    duration=int(info_dict['duration']),
                    title=str(info_dict['title']),
                    performer=perf,
                )
            ],
        )
        await hell.delete()
    except Exception as e:
        await parse_error(hell, e)
    try:
        os.remove(f"{audio_file}.mp3")
        os.remove(f"{audio_file}.webp")
        os.remove(thumb_name)
    except:
        pass


@hell_cmd(pattern="vsong(?:\s|$)([\s\S]*)")
async def vsong(event):
    ForGo10God, _, hell_mention = await client_id(event)
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Nothing given to search.")
    reply = await event.get_reply_message()
    query = lists[1].strip()
    if not query:
        return await parse_error(event, "Nothing given to search.")
    hell = await eor(event, f"<b><i>Searching “ {query} ”</i></b>", parse_mode="HTML")
    try:
        song_dict = await song_search(hell, query, 1)
        link = song_dict[1]['link']
        title = song_dict[1]['title']
        views = song_dict[1]['views']
        channel = song_dict[1]['channel']
        duration = song_dict[1]['duration']
        thumbnail = song_dict[1]['thumbnail']
        thumb_name = f'thumb{ForGo10God}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
    except Exception as e:
        return await parse_error(hell, f"__No song found. Maybe give different name or check spelling.__ \n`{str(e)}`", False)
    try:
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
        file_ = f"{info_dict['id']}.mp4"
        upload_text = f"**••• Uploading video •••** \n\n__» {title}__\n__»» {channel}__"
        await hell.edit(upload_text)
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            open(file_, "rb"),
            supports_streaming=True,
            caption=f"**✘ Video -** [{title}]({link}) \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**« ✘ »** {hell_mention}",
            thumb=thumb_name,
            reply_to=reply,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, hell, c_time, upload_text)
            ),
        )
        await hell.delete()
        os.remove(file_)
        os.remove(thumb_name)
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="lyrics(?:\s|$)([\s\S]*)")
async def lyrics(event):
    if not Config.LYRICS_API:
        return await parse_error(event, "`LYRICS_API` is not configured!", False)
    lists = event.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(event, "Nothing given to search.")
    _input_ = lists[1].strip()
    query = _input_.split("-", 1)
    if len(query) == 2:
        song = query[0].strip()
        artist = query[1].strip()
    else:
        song = query[0].strip()
        artist = ""
    text = f"**Searching lyrics ...** \n\n__Song:__ `{song}`"
    if artist != "":
        text += f"\n__Artist:__ `{artist}`"
    hell = await eor(event, text)
    client = Genius(Config.LYRICS_API)
    results = client.search_song(song, artist)
    if results:
        result = results.to_dict()
        title = result['full_title']
        image = result['song_art_image_url']
        lyrics = result['lyrics']
        final = f"<b><i>• Song:</b></i> <code>{title}</code> \n<b><i>• Lyrics:</b></i> \n<code>{lyrics}</code>"
        if len(final) >= 4095:
            to_paste = f"<img src='{image}'/> \n{final} \n<img src='https://te.legra.ph/file/2c546060b20dfd7c1ff2d.jpg'/>"
            link = await telegraph_paste(title, to_paste)
            await hell.edit(f"**Lyrics too big! Get it from here:** \n\n• [{title}]({link})", link_preview=False)
        else:
            await hell.edit(final, parse_mode="HTML")
    else:
        await parse_error(hell, "Unexpected Error Occured.")


@hell_cmd(pattern="wsong(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to a mp3 file.")
    rply = await event.get_reply_message()
    chat = "@auddbot"
    hell = await eor(event, "Trying to identify song...")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            third = await conv.send_message(rply)
            fourth = await conv.get_response()
            if not fourth.text.startswith("Audio received"):
                await hell.edit("Error identifying audio.")
                await event.client.delete_messages(
                    conv.chat_id, [first.id, second.id, third.id, fourth.id]
                )
                return
            await hell.edit("Processed...")
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await hell.edit("Please unblock @auddbot and try again")
    audio = f"**Song Name: **{fifth.text.splitlines()[0]}\n\n**Details: **__{fifth.text.splitlines()[2]}__"
    await hell.edit(audio)
    await event.client.delete_messages(
        conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id]
    )



CmdHelp("songs").add_command(
    "song", "<song name>", "Downloads the song from YouTube."
).add_command(
    "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
    "wsong", "<reply to a song file>", "Searches for the details of replied mp3 song file and uploads it's details."
).add_command(
    "lyrics", "<song - artist>", "Gives the lyrics of that song. Give arists name to get accurate results.", "lyrics Happier - Marshmallow"
).add_info(
    "Songs & Lyrics."
).add_warning(
    "✅ Harmless Module."
).add()
