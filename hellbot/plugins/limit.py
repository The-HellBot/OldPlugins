import asyncio
import os
import re

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events


@hell_cmd(pattern="limits(?:\s|$)([\s\S]*)")
async def is_limited(event):
    chat = "@SpamBot"
    msg = await eor(event, "Checking wheather your are restricted or not.......")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response_op = await conv.get_response()
            await event.client.send_read_acknowledge(chat)
            if 'Good news, no limits' in response_op:
                await msg.edit('Wallah wallah tum to free hoti.....tum dhyan rakhti jyada spam or non contacts ko message kar ne se tum restricted ho jati......Info fetched by hell bot')
                await conv.send_message('Cool, thanks')
                await event.client.send_read_acknowledge(chat)
            else:
                await msg.edit('Kya kand keya tha ki restrict hogaya tu 😏😏.....')
                await msg.edit(response_op)
                await conv.send_message('OK')
                await event.client.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit('Kindly unblock @SpamBot to further use this plugin.....')

            return
        except Exception as e:
            await msg.edit('Kya kar ra hai bhai tu......ye sab doglapan hai.....ache se use kar na')


