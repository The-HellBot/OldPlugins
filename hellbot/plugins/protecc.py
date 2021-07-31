import asyncio
import os
import datetime
import lottie
import urllib
import requests
from asyncio import sleep
from bs4 import BeautifulSoup

from . import *

qt = "A qt waifu appeared!"

def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )

@bot.on(hell_cmd(pattern="pt ?(.*)"))
@bot.on(sudo_cmd(pattern="pt ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = await eor(event, "Hmm..")
    dl = await bot.download_media(event.media, "resources/")
    file = {"encoded_image": (dl, open(dl, "rb"))}
    grs = requests.post(
        "https://www.google.com/searchbyimage/upload", files=file, allow_redirects=False
    )
    loc = grs.headers.get("Location")
    response = requests.get(
        loc,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        },
    )
    qtt = BeautifulSoup(response.text, "html.parser")
    div = qtt.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    text = alls.text
    try:
        if "cg" in text:
            return
        if "fictional character" in text:
            return
    except:
        pass
    await hell.edit(f"/protecc@loli_harem_bot {text}")
    await sleep(2)
    os.remove(dl)


@bot.on(events.NewMessage(incoming=True))
async def reverse(event):
    if not event.media:
        return
    if not qt in event.text:
        return
    if not event.sender_id == 792028928:
        return
    if Config.WAIFU_CATCHER != "TRUE":
        return
    dl = await bot.download_media(event.media, "resources/")
    file = {"encoded_image": (dl, open(dl, "rb"))}
    grs = requests.post(
        "https://www.google.com/searchbyimage/upload", files=file, allow_redirects=False
    )
    loc = grs.headers.get("Location")
    response = requests.get(
        loc,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        },
    )
    qtt = BeautifulSoup(response.text, "html.parser")
    div = qtt.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    text = alls.text
    try:
        if "cg" in text:
            return
        if "fictional character" in text:
            return
    except:
        pass
    await bot.send_message(event.chat_id, f"/protecc@loli_harem_bot {text}")
    await sleep(2)
    os.remove(dl)


CmdHelp("protecc").add_command(
  "pt", "<reply>", "Auto Protecc the waifu."
).add_info(
  "Waifu Protecc."
).add_warning(
  "✅ Harmless Module."
).add()
