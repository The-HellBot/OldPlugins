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

exclude = Config.EXCLUDE_WAIFU.split(" ")

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
    BASE_URL = "http://images.google.com"
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await bot.download_media(
                previous_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(downloaded_file_name, "rb"),
                ),
                "image_content": "",
            }
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        OUTPUT_STR = """/protecc {prs_text}""".format(
            **locals())
    await hell.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)


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
    if Config.EXCLUDE_WAIFU and event.chat_id == exclude:
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
