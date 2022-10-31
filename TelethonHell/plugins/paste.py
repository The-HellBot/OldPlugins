import os
import re

import requests
from telethon.utils import get_extension
from TelethonHell.plugins import *


@hell_cmd(pattern="paste(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "`Pasting ....`")
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    if not reply and not len(lists) == 2:
        return await parse_error(hell, "Nothing given to paste.")
    if len(lists) == 2:
        ext = re.findall(r"~\w+", lists[1])
        input_str = lists[1]
        try:
            extension = ext[0].replace("~", "")
            input_str = lists[1].replace(ext[0], "").strip()
        except IndexError:
            extension = None
    else:
        input_str = None
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
        else:
            return await parse_error(hell, "Reply to a document only.")
    if text_to_print == "":
        if reply.text:
            text_to_print = reply.raw_text
        else:
            return await parse_error(hell, "Nothing to paste.")
    if extension and extension.startswith("."):
        extension = extension[1:]
    try:
        response = await pasty(event, text_to_print, extension)
        if "error" in response:
            return await parse_error(hell, "Error while pasting text.")
        result = f"<b><i>📍 Pasted To</i> <a href={response['url']}>Here</a></b>"
        if response["raw"] != "":
            result += f"\n<b><i>📃 Raw link:</i> <a href={response['raw']}>Raw</a></b>"
        await hell.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="neko(?:\s|$)([\s\S]*)")
async def _(event):
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    if not reply and not len(lists) == 2:
        return await parse_error(event, "Nothing given to paste.")
    hell = await eor(event, "Pasting to nekobin...")
    if len(lists) == 2:
        message = lists[1]
    elif reply:
        if reply.media:
            downloaded_file_name = await event.client.download_media(
                reply,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8")
            os.remove(downloaded_file_name)
        else:
            message = reply.message
    else:
        return await parse_error(hell, "Nothing given to paste.")
    if downloaded_file_name.endswith(".py"):
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}.py"
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
    await eor(hell, reply_text, link_preview=False)


CmdHelp("paste").add_command(
    "paste", "<reply> or <text ~txt>", "Create a paste or a shortened url using pasty.lus.pm"
).add_command(
    "neko", "<reply> or <text>", "Create a paste or a shortened url using nekobin"
).add_info(
    "Paste contents to a pastebin."
).add_warning(
    "✅ Harmless Module."
).add()
