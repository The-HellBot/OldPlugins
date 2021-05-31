import asyncio
import os
import re

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@bot.on(hell_cmd(pattern=r"dc"))
@bot.on(sudo_cmd(pattern=r"dc", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())
    await eor(event, result.stringify())


@bot.on(hell_cmd(pattern=r"config"))
@bot.on(sudo_cmd(pattern=r"config", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())
    result = result.stringify()
    logger.info(result)
    await eor(event, result)


@bot.on(hell_cmd(pattern="dm ?(.*)"))
@bot.on(sudo_cmd(pattern="dm ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = event.pattern_match.group(1)
    kraken = hell.split(" ")
    chat_id = kraken[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    patra = ""
    letter = await event.get_reply_message()
    if event.reply_to_msg_id:
        await bot.send_message(chat_id, letter)
        await eor(event, "**[ ✓ Done ]**")
    for i in kraken[1:]:
        patra += i + " "
    if patra == "":
        return
    try:
        await bot.send_message(chat_id, patra)
        await eor(event, "**[ ✓ Done ]**")
    except BaseException:
        await eor(event, f"**Syntax :-** `{hl}dm <username> <message>")


CmdHelp("bot").add_command(
  "dc", None, "Gets the DataCenter Number"
).add_command(
  "config", None, "😒"
).add_command(
  "dm", "<username> <message>", "Sends a DM to given username with required msg", "dm @SupRemE_AnanD Sar U pro"
).add_info(
  "Haa vai? Kya hua?"
).add_warning(
  "✅ Harmless Module."
).add()
