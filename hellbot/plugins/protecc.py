import asyncio
import os
import datetime
import lottie
import urllib
import requests
from asyncio import sleep
from bs4 import BeautifulSoup

from hellbot.sql.waifu_sql import is_harem, add_grp, rm_grp, get_all_grp
from hellbot.sql.husb_sql import is_husb, add_hus_grp, rm_hus_grp, get_all_hus_grp
from . import *

qt = "Add them to your harem by sending"
qt_bots = ["792028928", "1733263647"]
hus_bot = ["1964681186"]

def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )

@hell_cmd(pattern="pt(?:\s|$)([\s\S]*)")
async def _(event):
    BASE_URL = "http://images.google.com"
    if event.reply_to_msg_id:
        hell = await eor(event, "Hmm..")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
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


@hell_handler()
async def _(event):
    if not event.media:
        return
    if not qt in event.text:
        return
    if str(event.sender_id) not in qt_bots:
        return
    all_grp = get_all_grp()
    if len(all_grp) == 0:
        return
    for grps in all_grp:
        if int(grps.chat_id) == event.chat_id:
            try:
                dl = await event.client.download_media(event.media, "resources/")
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
                hell = await event.client.send_message(event.chat_id, f"/protecc {text}")
                await sleep(2)
                await hell.delete()
                os.remove(dl)
            except:
                pass


@hell_handler()
async def _(event):
    if not event.media:
        return
    if not qt in event.text:
        return
    if str(event.sender_id) not in hus_bot:
        return
    all_grp = get_all_hus_grp()
    if len(all_grp) == 0:
        return
    for grps in all_grp:
        if int(grps.chat_id) == event.chat_id:
            try:
                dl = await event.client.download_media(event.media, "resources/")
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
                hell = await event.client.send_message(event.chat_id, f"/protecc {text}")
                await sleep(2)
                await hell.delete()
                os.remove(dl)
            except:
                pass


@hell_cmd(pattern="adwaifu(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.is_group:
        await eod(event, "Autowaifu works in Groups Only !!")
        return
    if is_harem(str(event.chat_id)):
        await eod(event, "This Chat is Already In AutoWaifu Database !!")
        return
    add_grp(str(event.chat_id))
    await eod(event, f"**Added Chat** {event.chat.title} **With Id** `{event.chat_id}` **To Autowaifu Database.**")


@hell_cmd(pattern="adhusb(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.is_group:
        await eod(event, "Autohusbando works in Groups Only !!")
        return
    if is_husb(str(event.chat_id)):
        await eod(event, "This Chat is Already In AutoHusbando Database !!")
        return
    add_hus_grp(str(event.chat_id))
    await eod(event, f"**Added Chat** {event.chat.title} **With Id** `{event.chat_id}` **To AutoHusbando Database.**")


@hell_cmd(pattern="rmwaifu(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.is_group:
        await eod(event, "Autowaifu works in groups only !!")
        return
    if not is_harem(str(event.chat_id)):
        await eod(event, "Autowaifu was already disabled here.")
        return
    rm_grp(str(event.chat_id))
    await eod(event, f"**Removed Chat** {event.chat.title} **With Id** `{event.chat_id}` **From AutoWaifu Database.**")


@hell_cmd(pattern="rmhusb(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.is_group:
        await eod(event, "Autohusbando works in groups only !!")
        return
    if not is_husb(str(event.chat_id)):
        await eod(event, "AutoHusbando was already disabled here.")
        return
    rm_hus_grp(str(event.chat_id))
    await eod(event, f"**Removed Chat** {event.chat.title} **With Id** `{event.chat_id}` **From AutoHusbando Database.**")


@hell_cmd(pattern="aw$")
async def _(event):
    hell = await eor(event, "Fetching Autowaifu chats...")
    all_grp = get_all_grp()
    x = "**Autowaifu enabled chats :** \n\n"
    for i in all_grp:
        ch = i.chat_id
        cht = int(ch)
        x += f"• `{cht}`\n"
    await hell.edit(x)


@hell_cmd(pattern="ah$")
async def _(event):
    hell = await eor(event, "Fetching Autohusbando chats...")
    all_grp = get_all_hus_grp()
    x = "**Autohusbando enabled chats :** \n\n"
    for i in all_grp:
        ch = i.chat_id
        cht = int(ch)
        x += f"• `{cht}`\n"
    await hell.edit(x)


CmdHelp("protecc").add_command(
  "pt", "<reply>", "Auto Protecc the waifu."
).add_command(
  "adwaifu", None, "Adds the current group to AutoWaifu Database."
).add_command(
  "rmwaifu", None, "Removes the group from AutoWaifu Database."
).add_command(
  "aw", None, "Gives the list of all chats with Autowaifu enabled."
).add_command(
  "adhusb", None, "Adds the current group to AutoHusbando Database."
).add_command(
  "rmhusb", None, "Removes the group from AutoHusbando Database."
).add_command(
  "ah", None, "Gives the list of all chats with AutoHusbando enabled."
).add_info(
  "Waifu & Husbando Protecc."
).add_warning(
  "✅ Harmless Module."
).add()
