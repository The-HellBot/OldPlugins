import asyncio
import os
import cv2
import io
import lottie
import random
import re
import shutil
import textwrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from . import *


path = "./hellmify/"
if not os.path.isdir(path):
    os.makedirs(path)


@hell_cmd(pattern="mmf ?(.*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "**Memifying 🌚🌝**")
    hell = await _reply.download_media()
    if hell.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell.endswith((".webp", ".png")):
        pics = Image.open(hell)
        pics.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    else:
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    output = await draw_meme_text(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
        os.remove(output)
    except BaseException:
        pass


@hell_cmd(pattern="mms ?(.*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "**Memifying 🌚🌝**")
    hell = await _reply.download_media()
    if hell.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell.endswith((".webp", ".png")):
        pic = Image.open(hell)
        pic.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    else:
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    output = await draw_meme(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
    except BaseException:
        pass
    os.remove(pic)


@hell_cmd(pattern="doge ?(.*)")
async def nope(event):
    hell = event.text[6:]
    if not hell:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Doge need some text to make sticker.")

    troll = await event.client.inline_query("DogeStickerBot", f"{(deEmojify(hell))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@hell_cmd(pattern="gg ?(.*)")
async def nope(event):
    hell = event.text[4:]
    if not hell:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Googlax need some text to make sticker.")

    troll = await event.client.inline_query("GooglaxBot", f"{(deEmojify(hell))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@hell_cmd(pattern="honk ?(.*)")
async def nope(event):
    hell = event.text[6:]
    if not hell:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Honka need some text to make sticker.")

    troll = await event.client.inline_query("honka_says_bot", f"{(deEmojify(hell))}.")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


@hell_cmd(pattern="gogl ?(.*)")
async def nope(event):
    hell = event.text[6:]
    if not hell:
        if event.is_reply:
            (await event.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(event, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(event, "Need some text...")

    troll = await event.client.inline_query("stickerizerbot", f"#12{(deEmojify(hell))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(event, "Error 404:  Not Found")


CmdHelp("memify").add_command(
  "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mmf <reply to a img/stcr/gif> hii ; hello"
).add_command(
  "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mms <reply to a img/stcr/gif> hii ; hello"
).add_command(
  "doge", "<text>", "Makes A Sticker of Doge with given text.", "doge Hello"
).add_command(
  "gogl", "<text>", "Makes google search sticker.", "gogl Hello"
).add_command(
  "gg", "<text>", "Makes google search sticker.", "gg Hello"
).add_command(
  "honk", "<text>", "Makes a sticker with honka revealing given text.", "honk Hello"
).add_info(
  "Make Memes on telegram 😉"
).add_warning(
  "✅ Harmless Module."
).add()
