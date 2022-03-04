import asyncio

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events

from . import *


@hell_cmd(pattern="limits$")
async def is_limited(event):
    chat = "@SpamBot"
    cid = await client_id(event)
    hell_mention = cid[2]
    msg = await eor(event, "")
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
