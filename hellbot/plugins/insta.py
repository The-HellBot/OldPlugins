import asyncio
import os
import re

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *



@hell_cmd(pattern="insta(?:\s|$)([\s\S]*)")
async def _(event):
    bot = "@InstagramSaverRobot"
    cid = await client_id(event)
    hell_mention = cid[2]
    input_str = event.text[7:]
    if "www.instagram.com" not in input_str:
        return await eod(event, "Well... this is not instagram link... Mind giving a proper instagram link?")
    kraken = await eor(event, "Trying to download.... please wait!")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(input_str)
            third = await conv.get_response()
            fourth = await conv.get_response()
            output_op = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kraken.edit("User Blocked!! Please Unblock @InstagramSaverRobot and try again...")
            return
    await kraken.delete()
    final = await event.client.send_file(event.chat_id, output_op)
    await final.edit(f"📥 InstaGram Video Downloaded By :- {hell_mention}")
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, third.id, fourth.id, output_op.id]
    )


CmdHelp("instagram").add_command(
  "insta", "<link>", "Downloads the provided instagram video/pic from link.", "insta www.instagram.com/yeuehiwnwiqo"
).add_info(
  "Insta Downloader."
).add_warning(
  "✅ Harmless Module"
).add()
