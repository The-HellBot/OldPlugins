import cv2
import os
import io
import random
import shutil
import re
import textwrap
import lottie
import asyncio

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from . import *


path = "./hellmify/"
if not os.path.isdir(path):
    os.makedirs(path)


@bot.on(hell_cmd(pattern="mmf ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mmf ?(.*)", allow_sudo=True))
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        hel_ = await eod(event, "`Can't memify this 🥴`")
        return
    hell = await _reply.download_media()
    if hell.endswith((".tgs")):
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell.endswith((".webp", ".png")):
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        pics = Image.open(hell)
        pics.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    else:
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    output = await draw_meme_text(file, msg)
    await bot.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
        os.remove(output)
    except BaseException:
        pass


@bot.on(hell_cmd(pattern="mms ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mms ?(.*)", allow_sudo=True))
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        hel_ = await eod(event, "`Can't memify this 🥴`")
        return
    hell = await _reply.download_media()
    if hell.endswith((".tgs")):
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell.endswith((".webp", ".png")):
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        pic = Image.open(hell)
        pic.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    else:
        hel_ = await eor(event, "**Memifying 🌚🌝**")
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    output = await draw_meme(file, msg)
    await bot.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
    except BaseException:
        pass
    os.remove(pic)

    
@bot.on(hell_cmd(pattern="doge(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="doge(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.pattern_match.group(1)
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(kraken, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(kraken, "Doge need some text to make sticker.")

    troll = await bot.inline_query("DogeStickerBot", f"{(deEmojify(hell))}")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(kraken, "Error 404:  Not Found")


@bot.on(hell_cmd(pattern="gg(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="gg(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.pattern_match.group(1)
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(kraken, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(kraken, "Googlax need some text to make sticker.")

    troll = await bot.inline_query("GooglaxBot", f"{(deEmojify(hell))}")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(kraken, "Error 404:  Not Found")


@bot.on(hell_cmd(pattern="honk(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="honk(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.pattern_match.group(1)
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(kraken, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(kraken, "Honka need some text to make sticker.")

    troll = await bot.inline_query("honka_says_bot", f"{(deEmojify(hell))}.")
    if troll:
        await kraken.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await bot.send_file(
                kraken.chat_id,
                hel_,
                caption="",
            )
        await hel_.delete()
    else:
     await eod(kraken, "Error 404:  Not Found")

    
CmdHelp("memify").add_command(
  "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mmf <reply to a img/stcr/gif> hii ; hello"
).add_command(
  "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mms <reply to a img/stcr/gif> hii ; hello"
).add_command(
  "doge", "<text>", "Makes A Sticker of Doge with given text.", "doge Hello"
).add_command(
  "gg", "<text>", "Makes google search sticker.", "gg Hello"
).add_command(
  "honk", "<text>", "Makes a sticker with honka revealing given text.", "honk Hello"
).add_info(
  "Make Memes on telegram 😉"
).add_warning(
  "✅ Harmless Module."
).add()
