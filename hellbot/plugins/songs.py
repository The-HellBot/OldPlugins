import asyncio
import os

import requests
import yt_dlp
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio

from . import *


@hell_cmd(pattern="song(?:\s|$)([\s\S]*)")
async def songs(event):
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
    query = event.text[6:]
    reply = await event.get_reply_message()
    if not query:
        return await eod(event, "Give something to search and download 😑")
    hell = await eor(event, f"<b><i>Searching “ {query} ”</i></b>", parse_mode="HTML")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = Hell_YTS(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{ForGo10God}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        views = results[0]["views"]
    except Exception as e:
        return await eod(hell, f"<b><i>ERROR !!</b></i> \n\n<i>No song found. Maybe give different name or check spelling.</i> \n\n<code>{str(e)}</code>", parse_mode="HTML")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        await hell.edit(f"**••• Uploading Song •••** \n\n__» {info_dict['title']}__\n__»» {info_dict['uploader']}__")
        await event.client.send_file(
            event.chat_id,
            audio_file,
            supports_streaming=True,
            caption=f"**✘ Song -** `{title}` \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**« ✘ »** {hell_mention}",
            thumb=thumb_name,
            reply_to=reply,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(info_dict['duration']),
                    title=str(info_dict['title']),
                    performer=perf,
                )
            ],
        )
        await hell.delete()
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        await eod(hell, str(e))


@hell_cmd(pattern="vsong(?:\s|$)([\s\S]*)")
async def vsong(event):
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
    query = event.text[7:]
    reply = await event.get_reply_message()
    if not query:
        return await eod(event, "Give something to search and download 😑")
    hell = await eor(event, f"<b><i>Searching “ {query} ”</i></b>", parse_mode="HTML")
    ydl_opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        results = Hell_YTS(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{ForGo10God}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        views = results[0]["views"]
    except Exception as e:
        return await eod(hell, f"<b><i>ERROR !!</b></i> \n\n<i>No song found. Maybe give different name or check spelling.</i> \n\n<code>{str(e)}</code>", parse_mode="HTML")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            vid_file = ydl.extract_info(link, download=True)
        file_ = f"{vid_file['id']}.mp4"
        await hell.edit(f"**••• Uploading video •••** \n\n__» {vid_file['title']}__\n__»» {vid_file['uploader']}__")
        await event.client.send_file(
            event.chat_id,
            open(file_, "rb"),
            supports_streaming=True,
            caption=f"**✘ Video -** `{title}` \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**« ✘ »** {hell_mention}",
            thumb=thumb_name,
            reply_to=reply,
        )
        await hell.delete()
        os.remove(file_)
        os.remove(thumb_name)
    except Exception as e:
        await eod(hell, str(e))


@hell_cmd(pattern="lyrics(?: |$)(.*)")
async def nope(kraken):
    hell = kraken.text[8:]
    uwu = await eor(kraken, f"Searching lyrics for  `{hell}` ...")
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(uwu, "Give song name to get lyrics...")
            return
    try:
        troll = await event.client.inline_query("iLyricsBot", f"{(deEmojify(hell))}")
        owo = await troll[0].click(Config.LOGGER_ID)
        await asyncio.sleep(3)
        owo_id = owo.id
        lyri = await event.client.get_messages(entity=Config.LOGGER_ID, ids=owo_id)
        await event.client.send_message(kraken.chat_id, lyri)
        await uwu.delete()
        await owo.delete()
    except Exception as e:
        await uwu.edir(f"**ERROR !!** \n\n`{str(e)}`")


@hell_cmd(pattern="lsong(?:\s|$)([\s\S]*)")
async def _(event):
    hell_ = event.text[6:]
    xyz = await client_id(event)
    ForGo10God, hell_mention = xyz[0], xyz[2]
    if hell_ == "":
        return await eor(event, "Give a song name to search")
    hell = await eor(event, f"Searching song `{hell_}`")
    somg = await event.client.inline_query("Lybot", f"{(deEmojify(hell_))}")
    if somg:
        fak = await somg[0].click(Config.LOGGER_ID)
        if fak:
            await event.client.send_file(
                event.chat_id,
                file=fak,
                caption=f"**Song by :** {hell_mention}",
            )
        await hell.delete()
        await fak.delete()
    else:
        await hell.edit("**ERROR 404 :** __NOT FOUND__")


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
    audio = f"**Song Name : **{fifth.text.splitlines()[0]}\n\n**Details : **__{fifth.text.splitlines()[2]}__"
    await hell.edit(audio)
    await event.client.delete_messages(
        conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id]
    )


@hell_cmd(pattern="spotify(?:\s|$)([\s\S]*)")
async def _(event):
    text = event.text[9:]
    chat = "@spotifysavebot"
    if text == "":
        return await eod(event, "Give something to download from Spotify.")
    hell = await eor(event, f"**Trying to download** `{text}` **from Spotify...**")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            somg = await event.client.inline_query(
                "spotifysavebot", f"str: {(deEmojify(text))}"
            )
            if somg:
                third = await somg[0].click(chat)
            else:
                return await eod(hell, "**ERROR !!** __404 : NOT FOUND__")
            fourth = await conv.get_response()
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await eod(hell, f"Please unblock {chat} to use Spotify module.")
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n{e}")
        await event.client.send_file(event.chat_id, file=fourth, caption="")
        await hell.delete()
        await event.client.delete_messages(
            conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id]
        )


CmdHelp("songs").add_command(
    "song", "<song name>", "Downloads the song from YouTube."
).add_command(
    "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
    "lsong", "<song name>", "Sends the searched song in current chat.", "lsong Alone"
).add_command(
    "wsong", "<reply to a song file>", "Searches for the details of replied mp3 song file and uploads it's details."
).add_command(
    "lyrics", "<song name>", "Gives the lyrics of that song.."
).add_command(
    "spotify", "<song name>", "Downloads the song from Spotify."
).add_info(
    "Songs & Lyrics."
).add_warning(
    "✅ Harmless Module."
).add()
