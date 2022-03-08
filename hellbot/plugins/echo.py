import asyncio
import base64
import requests

from telethon import events
from telethon.utils import get_peer_id

from hellbot.sql.echo_sql import addecho, get_all_echos, is_echo, remove_echo
from hellbot.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *


@hell_cmd(pattern="echo$")
async def echo(event):
    if event.reply_to_msg_id is not None:
        ForGo10God, HELL_USER, hell_mention = await client_id(event)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = event.chat_id
        if is_echo(user_id, chat_id):
            if gvarstat(f"ECHO_{ForGo10God}") == "True":
                return await eod(event, "The user is already enabled with echo !")
        addecho(user_id, chat_id)
        addgvar(f"ECHO_{ForGo10God}", "True")
        await eor(event, "**Hello 👋**")
    else:
        await eod(event, "Reply to a User's message to echo his messages")


@hell_cmd(pattern="rmecho$")
async def echo(event):
    if event.reply_to_msg_id is not None:
        ForGo10God, HELL_USER, hell_mention = await client_id(event)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
        chat_id = event.chat_id
        if is_echo(user_id, chat_id):
            if gvarstat(f"ECHO_{ForGo10God}") == "True":
                remove_echo(user_id, chat_id)
                await eod(event, "Echo has been stopped for the user")
        else:
            await eod(event, "The user is not activated with echo")
    else:
        await eod(event, "Reply to a User's message to echo his messages")


@hell_cmd(pattern="listecho$")
async def echo(event):
    lsts = get_all_echos()
    if len(lsts) > 0:
        output_str = "Echo enabled users:\n\n"
        for echos in lsts:
            output_str += (
                f"[User](tg://user?id={echos.user_id}) in chat `{echos.chat_id}`\n"
            )
    else:
        output_str = "No echo enabled users "
    await eor(event, output_str)


@H1.on(events.NewMessage(incoming=True))
async def samereply(event):
    if event.chat_id in Config.BL_CHAT:
        return
    id_ = await H1.get_me()
    uid = get_peer_id(id_)
    if is_echo(event.sender_id, event.chat_id):
        if gvarstat(f"ECHO_{uid}") == "True":
            await asyncio.sleep(1)
            if event.message.text or event.message.sticker:
                await event.reply(event.message)


if H2:
    @H2.on(events.NewMessage(incoming=True))
    async def samereply(event):
        if event.chat_id in Config.BL_CHAT:
            return
        id_ = await H2.get_me()
        uid = get_peer_id(id_)
        if is_echo(event.sender_id, event.chat_id):
            if gvarstat(f"ECHO_{uid}") == "True":
                await asyncio.sleep(1)
                if event.message.text or event.message.sticker:
                    await event.reply(event.message)


if H3:
    @H3.on(events.NewMessage(incoming=True))
    async def samereply(event):
        if event.chat_id in Config.BL_CHAT:
            return
        id_ = await H3.get_me()
        uid = get_peer_id(id_)
        if is_echo(event.sender_id, event.chat_id):
            if gvarstat(f"ECHO_{uid}") == "True":
                await asyncio.sleep(1)
                if event.message.text or event.message.sticker:
                    await event.reply(event.message)


if H4:
    @H4.on(events.NewMessage(incoming=True))
    async def samereply(event):
        if event.chat_id in Config.BL_CHAT:
            return
        id_ = await H4.get_me()
        uid = get_peer_id(id_)
        if is_echo(event.sender_id, event.chat_id):
            if gvarstat(f"ECHO_{uid}") == "True":
                await asyncio.sleep(1)
                if event.message.text or event.message.sticker:
                    await event.reply(event.message)


if H5:
    @H5.on(events.NewMessage(incoming=True))
    async def samereply(event):
        if event.chat_id in Config.BL_CHAT:
            return
        id_ = await H5.get_me()
        uid = get_peer_id(id_)
        if is_echo(event.sender_id, event.chat_id):
            if gvarstat(f"ECHO_{uid}") == "True":
                await asyncio.sleep(1)
                if event.message.text or event.message.sticker:
                    await event.reply(event.message)


CmdHelp("echo").add_command(
  "echo", "Reply to a user", "Replays every message from whom you enabled echo"
).add_command(
  "rmecho", "reply to a user", "Stop replayings targeted user message"
).add_command(
  "listecho", None, "Shows the list of users for whom you enabled echo"
).add_info(
  "Message Echoer."
).add_warning(
  "✅ Harmless Module."
).add()
