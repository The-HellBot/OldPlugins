import asyncio
import os
import re

from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *



@bot.on(hell_cmd(pattern="insta (.*)"))
@bot.on(sudo_cmd(pattern="insta (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    bot = "@instasavegrambot"
    input_str = event.pattern_match.group(1)
    if "www.instagram.com" not in input_str:
        await eor(event, "Well... this is not instagram link... Mind giving a proper instagram link?")
    else:
        kraken = await eor(event, "Trying to download.... please wait!")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(input_str)
            output_op = await conv.get_response()
            last = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kraken.edit("User Blocked!! Please Unblock @instasavegrambot and try again...")
            return
        await kraken.delete()
        final = await event.client.send_file(
            event.chat_id,
            output_op,
        )
        await final.edit(
            f"📥 InstaGram Video Downloaded By :- {hell_mention}")
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, output_op.id, last.id]
    )


CmdHelp("instagram").add_command(
  "insta", "<link>", "Downloads the provided instagram video/pic from link.", "insta www.instagram.com/yeuehiwnwiqo"
).add_info(
  "Insta Downloader."
).add_warning(
  "✅ Harmless Module"
).add()
