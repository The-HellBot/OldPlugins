import datetime
import json
import logging
import os
import re
import requests

from requests import exceptions, get
from telethon import events
from telethon.utils import get_extension

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


@hell_cmd(pattern="paste ?(.*)")
async def _(event):
    evnt = await eor(event, "`Pasting ....`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    ext = re.findall(r"-\w+", input_str)
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    text_to_print = ""
    if input_str:
        text_to_print = input_str
    if text_to_print == "" and reply.media:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
            if extension is None:
                extension = get_extension(reply.document)
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if reply.text:
            text_to_print = reply.raw_text
        else:
            return await eod(evnt, "`Reply to a file or msg or give a text to paste...`")
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pasty(text_to_print, extension)
        if "error" in response:
            return await eod(
                evnt,
                f"**Error While Pasting Text !!**",
            )
        result = f"<b><i>📍 Pasted To</i> <a href={response['url']}>Here</a></b>"
        if response["raw"] != "":
            result += f"\n<b><i>📃 Raw link:</i> <a href={response['raw']}>Raw</a></b>"
        await evnt.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await eod(evnt, f"**ERROR !!**\n\n`{str(e)}`")


@hell_cmd(pattern="neko ?(.*)")
async def _(event):
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
            downloaded_file_name = await event.client.download_media(
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
  "paste", "<text/reply>", "Create a paste or a shortened url using pasty.lus.pm"
).add_command(
  "neko", "<reply>", "Create a paste or a shortened url using nekobin"
).add_info(
  "Paste Things to Neko."
).add_warning(
  "✅ Harmless Module."
).add()
