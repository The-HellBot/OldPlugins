import asyncio
from . import *
from telethon.errors import ContactIdInvalidError
from telethon import functions, types
import os 
import random
from telethon.sync import TelegramClient


str = ["I have guts to ban u all fuck off bastards from my ib...",
"It is a matter of time after with u can't see my awsome pfps.....feeling sad for u...",
"I do not care who the hell are u just get vanished from my ib....",
"After few minutes u can only reach me on the grp not in ib.....",
"Phew! Finally going to get some releif.....",
"Sorry! No one from this gc deserves to be in my pm...XD XD",
"I am the real attitude king...Hell Yeah..."
"Less work to do as no one in ib going to disturbe me....",
"No spam and scams in ib....opps sorry u are blocked in my ib....LOL"
]





@hell_cmd(pattern = "blocka(?:\s|$)([\s\S]*)")
async def block_all(event):
    step_op = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid))
    if not step_op:
        return await eod(event, "Failed to fetch all useres")

    hell = await eor(event, f"`{random.choice(str)}`")
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        await hell.edit(f"Total number of members in this chat = {total}......Initialising **KICK ASS PROTOCOL**" )
    try:
       await client(functions.contacts.BlockRequest(id = user.id))
       success += 1
    except ContactIdInvalidError as e:
        LOGS.info(str(e))
        await hell.edit(f"Countered an error while blocking the user error is {e}...")
    await hell.edit(f" **PROTOCOL** is finished.....total number of ass kicked = {success} out of {total} members")



@hell_cmd(pattern = "blockc(?:\s|$)([\s\S]*)")
async def block_contacts(event):
    step_op = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid))
    if not step_op:
        return await eod(event, "Failed to fetch all useres")

    hell = await eor(event, f"`{random.choice(str)}`+ this time I'll block user who is in my contacts....")
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        result_ompho = client(functions.contacts.GetContactsRequest(
        hash=0
    ))
        if user in result_ompho:
            total += 1
            await hell.edit(f"Total number of members in this chat and in your contacts = {total}......Initialising **KICK ASS PROTOCOL**" )
            try:
                await client(functions.contacts.BlockRequest(id = user.id))
                success += 1
            except Exception as e:
                await hell.edit(f"Countered an error while blocking the user error is {e}...")
                LOGS.info(str(e))
        else:
            await hell.edit("There is no member in this chat who is saved in your contacts....")
    await hell.edit(f" **PROTOCOL** is finished.....total number of ass kicked = {success} out of {total} members")



@hell_cmd(pattern="blocknc(?:\s|$)([\s\S]*)")
async def block_noncontacts(event):
    step_op = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid))
    if not step_op:
        return await eod(event, "Failed to fetch all useres")

    hell = await eor(event, f"`{random.choice(str)}`+ this time I'll block user who is not in my contacts....")
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        result_ompho = client(functions.contacts.GetContactsRequest(
        hash=0
    ))
        if user not in result_ompho:
            total += 1
            await hell.edit(f"Total number of members in this chat and in your contacts = {total}......Initialising **KICK ASS PROTOCOL**" )
            try:
                await client(functions.contacts.BlockRequest(id = user.id))
                success += 1
            except Exception as e:
                await hell.edit(f"Countered an error while blocking the user error is {e}...")
                LOGS.info(str(e))
        else:
            await hell.edit("All of the member present in this group is in your contacts (Chapri sala sab ko contact me add kar leya hai bc....If you still want to block all members use blockc or blocka instead of blocknc")
    await hell.edit(f" **PROTOCOL** is finished.....total number of ass kicked = {success} out of {total} members")

@hell_cmd(pattern = "ublock(?:\s|$)([\s\S]*)")
async def ublock_all(event):
    step_op = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid))
    if not step_op:
        return await eod(event, "Failed to fetch all useres")
    hell = await eor(event, "Trying to unblock all users present in the group....Note that if there is no blocked user by you bot will return 0")
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        await hell.edit(f"Total number of members in this chat = {total}......Initialising **KISS PROTOCOL**" )
    try:
       await client(functions.contacts.UnblockRequest(id = user.id))
       success += 1
    except ContactIdInvalidError as e:
        LOGS.info(str(e))
        await hell.edit(f"Countered an error while blocking the user error is {e}...")
    await hell.edit(f" **PROTOCOL** is finished.....total number of kissed users = {success} out of {total} members")


CmdHelp("blocka").add_command(
  "blocka", None, "Block all the members present in the group for you...."
).add_command(
  "blockc", None, "Block all the member who is present in you group and in your contacts."
).add_command(
  "blocknc", None, "Block all the member who is present in you group and not in your contacts."
).add_command(
  "ublock", None, "Un-block all the members present in the group for you...."
).add_info(
  "Only to be used in groups"
).add_warning(
  "✅ Harmless Module."
).add()
