import logging
import os
import datetime

import requests
from requests import exceptions, get
from telethon import events

from . import *

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


def progress(current, total):
    logger.info(
        "**Downloaded**  `{}`  **of**  `{}`\n**Completed**  `{}`".format(
            current, total, (current / total) * 100
        )
    )

DOGBIN_URL = "https://del.dog/"

@bot.on(hell_cmd(pattern="paste ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="paste ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = f"**SYNTAX:** `{hl}paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await bot.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = f"**SYNTAX:** `{hl}paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = datetime.datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await eor(event, "**📍 Pasted to Dogbin :** [HERE]({}) **in**  `{} seconds` .\n\n**Go to Original URL:** [link]({})".format(
                url, ms, nurl
            )
        )
    else:
        await eor(event, "**📍 Pasted to Dogbin :** [HERE]({}) **in**  `{} seconds` .".format(url, ms))


@bot.on(hell_cmd(pattern="getpaste(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="getpaste(?: |$)(.*)", allow_sudo=True))
async def get_dogbin_content(dog_url):
    textx = await dog_url.get_reply_message()
    message = dog_url.pattern_match.group(1)
    hell = await eor(dog_url, "`Getting dogbin content...`")

    if textx:
        message = str(textx.message)

    format_normal = f"{DOGBIN_URL}"
    format_view = f"{DOGBIN_URL}v/"

    if message.startswith(format_view):
        message = message[len(format_view) :]
    elif message.startswith(format_normal):
        message = message[len(format_normal) :]
    elif message.startswith("del.dog/"):
        message = message[len("del.dog/") :]
    else:
        await eod(hell, "`Is that even a dogbin url?`")
        return

    resp = get(f"{DOGBIN_URL}raw/{message}")

    try:
        resp.raise_for_status()
    except exceptions.HTTPError as HTTPErr:
        await eod(hell, "Request returned an unsuccessful status code.\n\n" + str(HTTPErr)
        )
        return
    except exceptions.Timeout as TimeoutErr:
        await eod(hell, "Request timed out." + str(TimeoutErr))
        return
    except exceptions.TooManyRedirects as RedirectsErr:
        await eod(hell, "Request exceeded the configured number of maximum redirections."
            + str(RedirectsErr)
        )
        return

    reply_text = "**😏 Fetched dogbin URL content successfully!** \n\n📝** Content:**  " + resp.text

    await eor(dog_url, reply_text)

@bot.on(hell_cmd(pattern="neko ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="neko ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    datetime.datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = f"**SYNTAX:** `{hl}neko <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await bot.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                # message += m.decode("UTF-8") + "\r\n"
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = f"SYNTAX: `{hl}neko <long text to include>`"
    if downloaded_file_name.endswith(".py"):
        py_file = ""
        py_file += ".py"
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}{py_file}"
    else:
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"

    reply_text = f"**📍 Pasted to Nekobin :** [Neko]({url})"
    await eor(event, reply_text)


CmdHelp("paste").add_command(
  "paste", "<text/reply>", "Create a paste or a shortened url using dogbin"
).add_command(
  "getpaste", "dog url", "Gets the content of a paste or shortened url from dogbin"
).add_command(
  "neko", "<reply>", "Create a paste or a shortened url using nekobin"
).add_info(
  "Paste Things to Neko."
).add_warning(
  "✅ Harmless Module."
).add()
