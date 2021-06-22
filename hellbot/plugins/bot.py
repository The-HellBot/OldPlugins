import asyncio
import os
import re
import time

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import LeaveChannelRequest

from . import *


@bot.on(hell_cmd("kickme", outgoing=True))
async def leave(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("😪 **KThnxBye** See u all in hell!!")
        time.sleep(1)
        if "-" in str(e.chat_id):
            await bot(LeaveChannelRequest(e.chat_id))
        else:
            await eod(e, "**Iz this even a grp?😑**")

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
    await eor("Config Saved In You Heroku Logs.")


@bot.on(hell_cmd(pattern="schd ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="schd ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    ttl = 0
    message = f"SYNTAX: `{hl}schd <time_in_seconds> - <message to send>`"
    if input_str:
        await event.delete()
        if "-" in input_str:
            ttl, message = input_str.split("-")
        elif event.reply_to_msg_id:
            await event.delete()
            ttl = int(input_str)
            message = await event.get_reply_message()
        await asyncio.sleep(int(ttl))
        await event.respond(message)
    else:
        await event.edit(message)


@bot.on(hell_cmd(pattern="dm ?(.*)"))
@bot.on(sudo_cmd(pattern="dm ?(.*)", allow_sudo=True))
async def _(event):
    if len(event.text) > 3:
        if not event.text[3] == " ":
            return
    d = event.pattern_match.group(1)
    c = d.split(" ")
    try:
        chat_id = await get_user_id(c[0])
    except Exception as e:
        return await eod(event, f"`{e}`")
    msg = ""
    hunter = await event.get_reply_message()
    if event.reply_to_msg_id:
        await bot.send_message(chat_id, hunter)
        await eod(event, "**[Done]**")
    for i in c[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await bot.send_message(chat_id, msg)
        await eod(event, "**[Done]**")
    except BaseException:
        await eod(f"**Invalid Syntax !!**\n\n`{hl}dm <Username or UserID> <message>`")
    

CmdHelp("bot").add_command(
    "dc", None, "Gets the DataCenter Number"
).add_command(
    "config", None, "😒"
).add_command(
    "kickme", None, "Kicks Yourself from the group."
).add_command(
    "schd", "<secs> - <message>", "Sends your message in given secs", "schd 10 - Hello"
).add_command(
    "dm", "<username or user id> <message>", "Sends a DM to given username with required msg"
).add_info(
    "Haa vai? Kya hua?"
).add_warning(
    "✅ Harmless Module."
).add()
