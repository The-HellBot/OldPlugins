import asyncio
import datetime
import os
import re
import time

from random import choice
from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import LeaveChannelRequest

from ..sql.gvar_sql import gvarstat
from . import *

ping_txt = """
<b><i>╰•★★  ℘ơŋɠ ★★•╯</b></i>

    ⚘  <i>ʂ℘ɛɛɖ :</i> <code>{}</code>
    ⚘  <i>ų℘ɬıɱɛ :</i> <code>{}</code>
    ⚘  <i>ơῳŋɛཞ :</i> {}
"""


@hell_cmd(pattern="ping$")
async def pong(hell):
    start = datetime.datetime.now()
    a = gvarstat("PING_PIC")
    pic_list = []
    if a:
        b = a.split(" ")
        if len(b) >= 1:
            for c in b:
                pic_list.append(c)
        PIC = choice(pic_list)
    else:
        PIC = None
    event = await eor(hell, "`·.·★ ℘ıŋɠ ★·.·´")
    cid = await client_id(event)
    ForGo10God, HELL_USER = cid[0], cid[1]
    hell_mention = f"<a href='tg://user?id={ForGo10God}'>{HELL_USER}</a>"
    uptime = await get_time((time.time() - StartTime))
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    if PIC:
        await event.client.send_file(event.chat_id,
                                     file=PIC,
                                     caption=ping_txt.format(ms, uptime, hell_mention),
                                     parse_mode="HTML",
                                 )
        await event.delete()
    else:
        await event.edit(ping_txt.format(ms, uptime, hell_mention), parse_mode="HTML")


@hell_cmd(pattern="limits$")
async def is_limited(event):
    chat = "@SpamBot"
    msg = await eor(event, "Checking your account limit...")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await msg.edit('User Blocked!! Please Unblock @Spambot and try again...')
            return
        await msg.edit(response.text)
        await event.client.delete_messages(conv.chat_id, [first.id, response.id])

        
@hell_cmd(pattern="kickme$")
async def leave(e):
        await e.edit("😪 **KThnxBye** See u all in hell!!")
        time.sleep(1)
        if "-" in str(e.chat_id):
            await event.client(LeaveChannelRequest(e.chat_id))
        else:
            await eod(e, "**Iz this even a grp?😑**")


@hell_cmd(pattern="dc$")
async def _(event):
    result = await event.client(functions.help.GetNearestDcRequest())
    await eor(event, result.stringify())


@hell_cmd(pattern="config$")
async def _(event):
    result = await event.client(functions.help.GetConfigRequest())
    result = result.stringify()
    logger.info(result)
    await eor(event, "Config Saved In You Heroku Logs.")


@hell_cmd(pattern="vars(?:\s|$)([\s\S]*)")
async def lst(event):
    flag = (event.text[6:9]).lower()
    if flag and flag == "-db":
        hell = await eor(event, "Getting DB variables..")
        dbx = "**• List of DB Variables:** \n\n"
        for data in db_config:
            dbx += f"» `{data}`\n"
        await hell.edit(dbx)
    else:
        hell = await eor(event, "Getting configs list...")
        osx = "**• List of OS Configs:** \n\n"
        for data in os_config:
            osx += f"» `{data}`\n"
        await hell.edit(osx)


@hell_cmd(pattern="schd(?:\s|$)([\s\S]*)")
async def _(event):
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
        await eor(event, message)


@hell_cmd(pattern="dm(?:\s|$)([\s\S]*)")
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
        await event.client.send_message(chat_id, hunter)
        await eod(event, "**[Done]**")
    for i in c[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await event.client.send_message(chat_id, msg)
        await eod(event, "**[Done]**")
    except BaseException:
        await eod(f"**Invalid Syntax !!**\n\n`{hl}dm <Username or UserID> <message>`")


CmdHelp("bot").add_command(
    "dc", None, "Gets the DataCenter Number"
).add_command(
    "config", None, "😒"
).add_command(
    "vars", None, "Gets the list of all available OS Config Variables."
).add_command(
    "vars -db", None, "Gets the list of all available DB Config Variables."
).add_command(
    "kickme", None, "Kicks Yourself from the group."
).add_command(
    "ping", None, "Checks the ping speed of your Hêllẞø†"
).add_command(
    "schd", "<secs> - <message>", "Sends your message in given secs", "schd 10 - Hello"
).add_command(
    "dm", "<username or user id> <message>", "Sends a DM to given username with required msg"
).add_command(
    "limits", None, "Checks your telegram account limitations or restrictions via @SpamBot."
).add_info(
    "Haa vai? Kya hua?"
).add_warning(
    "✅ Harmless Module."
).add()
