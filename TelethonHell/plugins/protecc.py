import asyncio
import os

import requests
from bs4 import BeautifulSoup
from TelethonHell.DB.husb_sql import (add_hus_grp, get_all_hus_grp, is_husb,
                                      rm_hus_grp)
from TelethonHell.DB.waifu_sql import add_grp, get_all_grp, is_harem, rm_grp
from TelethonHell.plugins import *

qt = "Add them to your harem by sending"
qt_bots = ["792028928", "1733263647"]
hus_bot = ["1964681186"]


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
        await hell.edit(f"/protecc {prs_text}", parse_mode="HTML", link_preview=False)
    else:
        await parse_error(event, "Reply to an waifu/husbando image to protecc them.")


@hell_handler(incoming=True)
async def _(event):
    if not event.media:
        return
    if not qt in event.text:
        return
    if str(event.sender_id) not in qt_bots:
        return
    if is_harem(str(event.chat_id)):
        try:
            dl = await event.client.download_media(event.media, "resources/")
            file = {"encoded_image": (dl, open(dl, "rb"))}
            grs = requests.post(
                "https://www.google.com/searchbyimage/upload",
                files=file,
                allow_redirects=False,
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
            hell = await event.client.send_message(
                event.chat_id,
                f"/protecc {text}",
                reply_to=event,
            )
            await asyncio.sleep(2)
            await hell.delete()
            os.remove(dl)
        except Exception as e:
            LOGS.info(str(e))


@hell_handler(incoming=True)
async def _(event):
    if not event.media:
        return
    if not qt in event.text:
        return
    if str(event.sender_id) not in hus_bot:
        return
    if is_husb(str(event.chat_id)):
        try:
            dl = await event.client.download_media(event.media, "resources/")
            file = {"encoded_image": (dl, open(dl, "rb"))}
            grs = requests.post(
                "https://www.google.com/searchbyimage/upload",
                files=file,
                allow_redirects=False,
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
            hell = await event.client.send_message(
                event.chat_id,
                f"/protecc {text}",
                reply_to=event,
            )
            await asyncio.sleep(2)
            await hell.delete()
            os.remove(dl)
        except Exception as e:
            LOGS.info(str(e))


@hell_cmd(pattern="adwaifu(?:\s|$)([\s\S]*)")
async def _(event):
    _, _, hell_mention = await client_id(event)
    if not event.is_group:
        return await parse_error(event, "Autowaifu works in Groups Only !!")
    if is_harem(str(event.chat_id)):
        return await eod(event, "This Chat is Already In AutoWaifu Database !!")
    add_grp(str(event.chat_id))
    await eod(event, f"**✅ Autowaifu Started !!** \n\n__• Chat:__ {event.chat.title} \n__• Chat ID:__ `{event.chat_id}` \n__• Client:__ {hell_mention}")


@hell_cmd(pattern="adhusb(?:\s|$)([\s\S]*)")
async def _(event):
    _, _, hell_mention = await client_id(event)
    if not event.is_group:
        return await parse_error(event, "Autohusbando works in Groups Only !!")
    if is_husb(str(event.chat_id)):
        return await eod(event, "This Chat is Already In AutoHusbando Database !!")
    add_hus_grp(str(event.chat_id))
    await eod(event, f"**✅ Autohusbando Started !!** \n\n__• Chat:__ {event.chat.title} \n__• Chat ID:__ `{event.chat_id}` \n__• Client:__ {hell_mention}")


@hell_cmd(pattern="rmwaifu(?:\s|$)([\s\S]*)")
async def _(event):
    _, _, hell_mention = await client_id(event)
    if not event.is_group:
        return await parse_error(event, "Autowaifu works in groups only !!")
    if not is_harem(str(event.chat_id)):
        return await eod(event, "Autowaifu was already disabled here.")
    rm_grp(str(event.chat_id))
    await eod(event, f"**🗑️ Removed Autowaifu !!** \n\n__• Chat:__ {event.chat.title} \n__• Chat ID:__ `{event.chat_id}` \n__• Client:__ {hell_mention}")


@hell_cmd(pattern="rmhusb(?:\s|$)([\s\S]*)")
async def _(event):
    _, _, hell_mention = await client_id(event)
    if not event.is_group:
        return await parse_error(event, "Autohusbando works in groups only !!")
    if not is_husb(str(event.chat_id)):
        return await eod(event, "AutoHusbando was already disabled here.")
    rm_hus_grp(str(event.chat_id))
    await eod(event, f"**🗑️ Removed Autohusbando !!** \n\n__• Chat:__ {event.chat.title} \n__• Chat ID:__ `{event.chat_id}` \n__• Client:__ {hell_mention}")


@hell_cmd(pattern="autowaifu$")
async def _(event):
    hell = await eor(event, "Fetching Autowaifu chats...")
    all_grp = get_all_grp()
    x = "**Autowaifu enabled chats :** \n\n"
    for i in all_grp:
        ch = i.chat_id
        x += f"• `{ch}`\n"
    await hell.edit(x)


@hell_cmd(pattern="autohusbando$")
async def _(event):
    hell = await eor(event, "Fetching Autohusbando chats...")
    all_grp = get_all_hus_grp()
    x = "**Autohusbando enabled chats :** \n\n"
    for i in all_grp:
        ch = i.chat_id
        x += f"• `{ch}`\n"
    await hell.edit(x)


CmdHelp("protecc").add_command(
    "pt", "<reply>", "Auto Protecc the waifu."
).add_command(
    "adwaifu", None, "Adds the current group to AutoWaifu Database."
).add_command(
    "rmwaifu", None, "Removes the group from AutoWaifu Database."
).add_command(
    "autowaifu", None, "Gives the list of all chats with Autowaifu enabled."
).add_command(
    "adhusb", None, "Adds the current group to AutoHusbando Database."
).add_command(
    "rmhusb", None, "Removes the group from AutoHusbando Database."
).add_command(
    "autohusbando", None, "Gives the list of all chats with AutoHusbando enabled."
).add_info(
    "Waifu & Husbando Protecc."
).add_warning(
    "✅ Harmless Module."
).add()
