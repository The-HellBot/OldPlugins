import asyncio
import datetime
import time
from random import choice

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import SaveDraftRequest
from TelethonHell.DB.gvar_sql import gvarstat
from TelethonHell.clients.client_list import get_user_id
from TelethonHell.plugins import *

ping_txt = """
<b><i>╰•★★  ℘ơŋɠ ★★•╯</b></i>

    ⚘  <i>ʂ℘ɛɛɖ :</i> <code>{}</code>
    ⚘  <i>ų℘ɬıɱɛ :</i> <code>{}</code>
    ⚘  <i>ơῳŋɛཞ :</i> {}
"""


@hell_cmd(pattern="ping$")
async def pong(event):
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
    hell = await eor(event, "`·.·★ ℘ıŋɠ ★·.·´")
    ForGo10God, HELL_USER, hell_mention = await client_id(event, is_html=True)
    uptime = await get_time((time.time() - StartTime))
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    if PIC:
        await event.client.send_file(
            event.chat_id,
            file=PIC,
            caption=ping_txt.format(ms, uptime, hell_mention),
            parse_mode="HTML",
        )
        await hell.delete()
    else:
        await hell.edit(ping_txt.format(ms, uptime, hell_mention), parse_mode="HTML")


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
            await parse_error(msg, "`__Unblock__ @Spambot __and try again.__", False)
            return
        await msg.edit(response.text)
        await event.client.delete_messages(conv.chat_id, [first.id, response.id])


@hell_cmd(pattern="kickme$")
async def leave(event):
    hell = await eor(event, "😪 **KThnxBye** See u all in hell!!")
    time.sleep(1)
    if "-" in str(event.chat_id):
        await event.client(LeaveChannelRequest(event.chat_id))
    else:
        await eod(hell, "**Is this even a group?😑**")


@hell_cmd(pattern="dc$")
async def _(event):
    result = await event.client(functions.help.GetNearestDcRequest())
    await eor(event, result.stringify())


@hell_cmd(pattern="config$")
async def _(event):
    result = await event.client(functions.help.GetConfigRequest())
    result = result.stringify()
    LOGS.info(result)
    await eor(event, "Config Saved In You Heroku Logs.")


@hell_cmd(pattern="vars(?:\s|$)([\s\S]*)")
async def lst(event):
    flag = str(event.text[6:9]).lower()
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
        await eod(event, message)


@hell_cmd(pattern="dm(?:\s|$)([\s\S]*)")
async def _(event):
    lists = event.text.split(" ", 2)
    reply = await event.get_reply_message()
    if reply and len(lists) >= 2:
        try:
            chat_id = await get_user_id(event, lists[1])
            to_send = reply
            await event.client.send_message(chat_id, to_send)
            await eod(event, "**[Done]**")
        except Exception as e:
            return await parse_error(event, e)
    
    elif len(lists) == 3:
        try:
            chat_id = await get_user_id(event, lists[1])
            to_send = lists[2]
            await event.client.send_message(chat_id, to_send)
            await eod(event, "**[Done]**")
        except Exception as e:
            return await parse_error(event, e)
    
    else:
        await eod(event, f"**SYNTAX EXAMPLE**\n\n~ `{hl}dm @ForGo10God Hey Hell!` \n~ `{hl}dm @ForGo10God <reply to a msg>`")


@hell_cmd(pattern="chain$")
async def _(event):
    hell = await eor(event, "Counting...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await hell.edit(f"⛓️ **Chain length :**  `{count}`")


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
).add_command(
    "chain", "Reply to a message", "Reply this command to any msg so that it finds chain length of that msg"
).add_info(
    "Some bot level commands."
).add_warning(
    "✅ Harmless Module."
).add()
