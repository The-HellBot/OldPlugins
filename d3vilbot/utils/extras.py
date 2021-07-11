import asyncio
import datetime
import importlib
import inspect
import logging
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from time import gmtime, strftime

from telethon import events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator

from d3vilbot import *
from d3vilbot.helpers import *
from d3vilbot.config import Config


# either edit or reply that msg
async def edit_or_reply(
    event,
    text,
    parse_mode=None,
    link_preview=None,
    file_name=None,
    aslink=False,
    deflink=False,
    noformat=False,
    linktext=None,
    caption=None,
):
    link_preview = link_preview or False
    reply_to = await event.get_reply_message()
    if len(text) < 4096 and not deflink:
        parse_mode = parse_mode or "md"
        if event.sender_id in Config.SUDO_USERS:
            if reply_to:
                return await reply_to.reply(
                    text, parse_mode=parse_mode, link_preview=link_preview
                )
            return await event.reply(
                text, parse_mode=parse_mode, link_preview=link_preview
            )
        await event.edit(text, parse_mode=parse_mode, link_preview=link_preview)
        return event
    if not noformat:
        asciich = ["**", "`", "__"]
        for i in asciich:
            text = re.sub(rf"\{i}", "", text)
    if aslink or deflink:
        linktext = linktext or "Message was to big so pasted to bin"
        try:
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": text}
                )
                .json()
                .get("result")
                .get("key")
            )
            text = linktext + f" [here](https://nekobin.com/{key})"
        except Exception:
            text = re.sub(r"•", ">>", text)
            kresult = requests.post(
                "https://del.dog/documents", data=text.encode("UTF-8")
            ).json()
            text = linktext + f" [here](https://del.dog/{kresult['key']})"
        if event.sender_id in Config.SUDO_USERS:
            if reply_to:
                return await reply_to.reply(text, link_preview=link_preview)
            return await event.reply(text, link_preview=link_preview)
        await event.edit(text, link_preview=link_preview)
        return event
    file_name = file_name or "output.txt"
    caption = caption or None
    with open(file_name, "w+") as output:
        output.write(text)
    if reply_to:
        await reply_to.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    if event.sender_id in Config.SUDO_USERS:
        await event.reply(caption, file=file_name)
        await event.delete()
        return os.remove(file_name)
    await event.client.send_file(event.chat_id, file_name, caption=caption)
    await event.delete()
    os.remove(file_name)


# delete timeout
async def delete_d3vil(event, text, time=None, parse_mode=None, link_preview=None):
    parse_mode = parse_mode or "md"
    link_preview = link_preview or False
    time = time or 10
    if event.sender_id in Config.SUDO_USERS:
        reply_to = await event.get_reply_message()
        d3vilevent = (
            await reply_to.reply(text, link_preview=link_preview, parse_mode=parse_mode)
            if reply_to
            else await event.reply(
                text, link_preview=link_preview, parse_mode=parse_mode
            )
        )
    else:
        d3vilevent = await event.edit(
            text, link_preview=link_preview, parse_mode=parse_mode
        )
    await asyncio.sleep(time)
    return await d3vilevent.delete()

# d3vilbot
