import asyncio
import os
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon import functions, types, events
from . import *

logs_id = Config.FBAN_LOG_GROUP
fbot = "@MissRose_bot"


@bot.on(hell_cmd(pattern="newfed ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="newfed ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    await eor(event, "`Making new fed...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=609517172)
            )
            await event.client.send_message(chat, f"/newfed {hell_input}")
            response = await response
        except YouBlockedUserError:
            await eod(event, "`Please unblock` @MissRose_Bot `and try again`")
            return
        if response.text.startswith("You already have a federation"):
            await eod(event,
                "You already have a federation. Do .renamefed to rename your current fed."
            )
        else:
            await eod(event, f"{response.message.message}", 7)


@bot.on(hell_cmd(pattern="renamefed ?(.*)"))
@bot.on(sudo_cmd(pattern="renamefed ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return 
    hell_input = event.pattern_match.group(1)
    chat = "@MissRose_Bot"
    await event.edit("`Trying to rename your fed...`")
    async with event.client.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=609517172))
              await event.client.send_message(chat, f"/renamefed {hell_input}")
              response = await response 
          except YouBlockedUserError: 
              await event.reply("Please Unblock @MissRose_Bot")
              return
          else: 
             await event.delete()
             await event.client.send_message(event.chat_id, response.message)


@bot.on(hell_cmd(pattern="fstat ?(.*)"))
@bot.on(sudo_cmd(pattern="fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = await eor(event, "`Collecting fstat....`")
    thumb = hell_logo
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        lavde = str(previous_message.sender_id)
        user = f"[user](tg://user?id={lavde})"
    else:
        lavde = event.pattern_match.group(1)
        user = lavde
    if lavde == "":
        await hell.edit(
            "`Need username/id to check fstat`"
        )
        return
    else:
        async with bot.conversation(fbot) as conv:
            try:
                await conv.send_message("/fedstat " + lavde)
                await asyncio.sleep(4)
                response = await conv.get_response()
                await asyncio.sleep(2)
                await bot.send_message(event.chat_id, response)
                await event.delete()
            except YouBlockedUserError:
                await hell.edit("`Please Unblock` @MissRose_Bot")


@bot.on(hell_cmd(pattern="fedinfo ?(.*)"))
@bot.on(sudo_cmd(pattern="fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = await eor(event, "`Fetching fed info.... please wait`")
    lavde = event.pattern_match.group(1)
    async with bot.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + lavde)
            massive = await conv.get_response()
            await hell.edit(massive.text + "\n\n**ʟɛɢɛռɖaʀʏ_ᴀғ_ɦɛʟʟɮօt**")
        except YouBlockedUserError:
            await hell.edit("`Please Unblock` @MissRose_Bot")
            
            
CmdHelp("federation").add_command(
  "newfed", "<newfed name>", "Makes a federation of Rose bot"
).add_command(
  "renamefed", "<new name>", "Renames the fed of Rose Bot"
).add_command(
  "fstat", "<username/id>", "Gets the fban stats of the user from rose bot federation"
).add_command(
  "fedinfo", "<fed id>", "Gives details of the given fed id"
).add_info(
  "Rose Bot Federation."
).add_warning(
  "✅ Harmless Module."
).add()
