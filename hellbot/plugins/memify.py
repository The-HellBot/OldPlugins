import cv2
import os
import io
import random
import shutil
import re
import textwrap
import lottie

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from . import *


path = "./d3vilmify/"
if not os.path.isdir(path):
    os.makedirs(path)


@bot.on(d3vil_cmd(pattern="mmf ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mmf ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "You need to reply to an image with .mmf` 'text on top' ; 'text on bottom'")
        return
    await eor(event, "🤪 **Memifying...**")
    reply = await event.get_reply_message()
    imgs = await bot.download_media(reply.media, path)
    img = cv2.VideoCapture(imgs) 
    tal, semx = img.read()
    cv2.imwrite("d3vilkrish.webp", semx)
    text = event.pattern_match.group(1)
    webp_file = await draw_meme_text("d3vilkrish.webp", text)
    await event.client.send_file(
        event.chat_id, webp_file, reply_to=event.reply_to_msg_id
    )
    await event.delete()
    shutil.rmtree(path)
    os.remove("d3vilkrish.webp")
    os.remove(webp_file)


@bot.on(d3vil_cmd(pattern="mms ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mms ?(.*)", allow_sudo=True))
async def sed(d3vilboy):
    if d3vilboy.fwd_from:
        return
    if not d3vilboy.reply_to_msg_id:
        await eod(d3vilboy, "You need to reply to an image with .mms` 'text on top' ; 'text on bottom'")
        return
    await eor(d3vilboy, "🤪 **Memifying...**")
    reply = await d3vilboy.get_reply_message()
    imgs = await bot.download_media(reply.media, path)
    img = cv2.VideoCapture(imgs) 
    tal, semx = img.read()
    cv2.imwrite("d3vilkrish.webp", semx)
    text = d3vilboy.pattern_match.group(1)
    photo = await draw_meme("d3vilkrish.webp", text)
    await d3vilboy.client.send_file(
        d3vilboy.chat_id, photo, reply_to=d3vilboy.reply_to_msg_id
    )
    await d3vilboy.delete()
    shutil.rmtree(path)
    os.remove("d3vilkrish.webp")
    os.remove(photo)
    
@bot.on(d3vil_cmd(pattern="doge(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="doge(?: |$)(.*)", allow_sudo=True))
async def nope(d3vilkrish):
    d3vil = d3vilkrish.pattern_match.group(1)
    if not d3vil:
        if d3vilkrish.is_reply:
            (await d3vilkrish.get_reply_message()).message
        else:
            if Config.ABUSE == "ON":
                return await eor(d3vilkrish, "Abe chumtiye kuch likhne ke liye de")
            else:
                return await eor(d3vilkrish, "Doge need some text to make sticker.")

    troll = await bot.inline_query("DogeStickerBot", f"{(deEmojify(d3vil))}")
    if troll:
        await d3vilkrish.delete()
        d3vl_ = await troll[0].click(Config.LOGGER_ID)
        if d3vl_:
            await bot.send_file(
                d3vilkrish.chat_id,
                d3vl_,
                caption="",
            )
        await d3vl_.delete()
    else:
     await eod(d3vilkrish, "Error 404:  Not Found")
     
    
CmdHelp("memify").add_command(
  "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mmf <reply to a img/stcr/gif> hii ; d3vilo"
).add_command(
  "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mms <reply to a img/stcr/gif> hii ; d3vilo"
).add_command(
  "doge", "<text>", "Makes A Sticker of Doge with given text."
).add_info(
  "Make Memes on telegram 😉"
).add_warning(
  "✅ Harmless Module."
).add()
