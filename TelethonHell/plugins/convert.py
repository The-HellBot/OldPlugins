import asyncio
import os
import time
from datetime import datetime
from io import BytesIO

from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest
from TelethonHell.plugins import *


@hell_cmd(pattern="stog(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await parse_error(event, "Reply to animated sticker to make gif.")
    hell = await eor(event, "Converting...")
    if event.pattern_match.group(1):
        quality = event.pattern_match.group(1)
    else:
        quality = 512
    rply = await event.get_reply_message()
    type_ = media_type(rply)
    if type_ == 'Sticker':
        hell_ = await event.client.download_media(rply.media)
        gifs = await tgs_to_gif(hell_, True)
        unsave =  await event.client.send_file(event.chat_id, file=gifs, force_document=False)
        await unsave_gif(event, unsave)
        await hell.delete()
        os.remove(hell_)
        os.remove("hellbot.gif")
    else:
        await parse_error(hell, "Only animated stickers are supported.")


@hell_cmd(pattern="stoi$")
async def _(hell):
    reply_to_id = hell.message.id
    if hell.reply_to_msg_id:
        reply_to_id = hell.reply_to_msg_id
    event = await eor(hell, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await hell.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            await hell.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await parse_error(event, "Can't Convert")
    else:
        await eod(event, f"Syntax : `{hl}stoi` reply to a Telegram normal sticker")


@hell_cmd(pattern="itos$")
async def _(hell):
    reply_to_id = hell.message.id
    if hell.reply_to_msg_id:
        reply_to_id = hell.reply_to_msg_id
    event = await eor(hell, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await hell.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            await hell.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await parse_error(event, "Can't Convert")
    else:
        await eod(event, f"Syntax : `{hl}itos` reply to a Telegram normal sticker")


@hell_cmd(pattern="ttf(?:\s|$)([\s\S]*)")
async def get(event):
    name = event.text[5:]
    if name is None:
        await eod(event, f"Reply to text message as `{hl}ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await eod(event, f"Reply to text message as `{hl}ttf <file name>`")


@hell_cmd(pattern="ftoi$")
async def on_file_to_photo(event):
    target = await event.get_reply_message()
    hbot = await eor(event, "Converting.....")
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith("image/"):
        return
    if image.mime_type == "image/webp":
        return
    if image.size > 10 * 1024 * 1024:
        return
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await hbot.delete()


@hell_cmd(pattern="itof$")
async def _(hell):
    reply_to_id = hell.message.id
    if hell.reply_to_msg_id:
        reply_to_id = hell.reply_to_msg_id
    event = await eor(hell, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hellbot.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await hell.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            await hell.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await parse_error(event, "Can't Convert")
    else:
        await eod(event, f"Syntax : `{hl}itof` reply to a sticker/image")


@hell_cmd(pattern="nfc(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await parse_error(event, "Reply to any media file.")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await parse_error(event, "Reply to any media file.")
    input_str = event.pattern_match.group(1)
    if input_str is None:
        return await eod(event, f"Try `{hl}nfc voice` or `{hl}nfc mp3`")
    if input_str in ["mp3", "voice"]:
        hell = await eor(event, "Converting ...")
    else:
        return await eod(event, f"Try `{hl}nfc voice` or `{hl}nfc mp3`")
    try:
        start = datetime.datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, hell, c_time, "Downloading ...")
            ),
        )
    except Exception as e:
        await parse_error(hell, e)
    else:
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await hell.edit(f"__Downloaded:__ `{downloaded_file_name}` \n__Time taken:__ `{ms} seconds`")
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await parse_error(hell, "Not supported")
            os.remove(downloaded_file_name)
            return
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Uploading ...")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()


CmdHelp("convert").add_command(
    "stoi", "<reply to a sticker", "Converts the replied sticker into an image"
).add_command(
    "itos", "<reply to a image>", "Converts the replied image to sticker"
).add_command(
    "ftoi", "<reply to a image file", "Converts the replied file image to normal image"
).add_command(
    "itof", "<reply to a image/sticker>", "Converts the replied image or sticker into file."
).add_command(
    "stog", "<reply to a animated sticker>", "Converts the replied animated sticker into gif"
).add_command(
    "ttf", "<reply to text>", "Converts the given text message to required file(given file name)"
).add_command(
    "nfc voice", "<reply to media to extract voice>", "Converts the replied media file to voice"
).add_command(
    "nfc mp3", "<reply to media to extract mp3>", "Converts the replied media file to mp3"
).add_info(
    "Converter."
).add_warning(
    "✅ Harmless Module."
).add()
