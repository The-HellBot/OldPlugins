import asyncio
from time import sleep
import os 
import random

from telethon.tl import functions
from telethon.tl.errors import ContactIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (ChannelParticipantsAdmins,
                               ChannelParticipantsKicked, ChatBannedRights,
                               UserStatusEmpty, UserStatusLastMonth,
                               UserStatusLastWeek, UserStatusOffline,
                               UserStatusOnline, UserStatusRecently)

from . import *

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


@hell_cmd(pattern="kickall$", allow_sudo=False)
async def _(event):
    ForGo10God, _, _ = await client_id(event)
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, ForGo10God)
    )
    if not result.participant.admin_rights.ban_users:
        return await parse_error(event, "Need ban rights to do this.")
    hell = await eor(event, "**Bleck Magik Started...**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await asyncio.sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await asyncio.sleep(0.5)
    await hell.edit("**Bleck Magik Done...**")
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#KICKALL \n\nKicked Out  `{success}`  of  `{total}`  members",
    )


@hell_cmd(pattern="banall$", allow_sudo=False)
async def _(event):
    ForGo10God, _, _ = await client_id(event)
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, ForGo10God)
    )
    if not result.participant.admin_rights.ban_users:
        return await parse_error(event, "Need ban rights to do this.")
    hell = await eor(event, "**Bleck Magik Begins..**")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await asyncio.sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await asyncio.sleep(0.5)
    await hell.edit("**Bleck Magik Completed...**")
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#BANALL \n\nSucessfully banned  `{success}`  out of  `{total}`  members!!",
    )


@hell_cmd(pattern="unbanall$")
async def _(event):
    if event.is_private:
        return
    xyz = await eor(event, "Searching Participant Lists.")
    p = 0
    async for i in event.client.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(
                functions.channels.EditBannedRequest(event.chat_id, i, rights)
            )
        except FloodWaitError as ex:
            logger.warn("sleeping for {} seconds".format(ex.seconds))
            sleep(ex.seconds)
        except Exception as ex:
            await xyz.edit(str(ex))
        else:
            p += 1
    await xyz.edit("{}: {} unbanned".format(event.chat_id, p))


@hell_cmd(pattern="ikuck(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await parse_error(event, "`You aren't an admin here!`")
            return
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    hell = await eor(event, "Searching Participant Lists.")
    async for i in event.client.iter_participants(event.chat_id):
        p = p + 1
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(hell, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(hell, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            q = q + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            r = r + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            b = b + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            d = d + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await parse_error(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                else:
                    c = c + 1
        elif i.status is None:
            n = n + 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await hell.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await hell.edit(
        """Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


async def ban_user(chat_id, i, rights):
    try:
        await event.client(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)

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


CmdHelp("banall").add_command(
    "ikuck", None, "Gives the data of group. Deleted accounts, Last seen, Offline, Online, Recently, Bots, Etc."
).add_command(
    "unbanall", None, "Unbans all the user in the chat."
).add_command(
    "banall", None, "Bans all the user in the chat.."
).add_command(
    "kickall", None, "Kicks all the users in the chat..."
).add_info(
    "⚠️ Group Destroyer"
).add_warning(
    "✅ Harmless Module."
).add()
