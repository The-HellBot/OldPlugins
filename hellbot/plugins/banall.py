import asyncio
from time import sleep

from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest

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

@bot.on(hell_cmd(pattern=r"kickall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"kickall ?(.*)", allow_sudo=True))
async def _(event):
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result.participant.admin_rights.ban_users:
        return await eod(
            event, "No immunity for this action!!"
        )
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
    await hell.edit(
        "**Bleck Magik Done...**"
    )
    await bot.send_message(
        Config.LOGGER_ID,
        f"#KICKALL \n\nKicked Out  `{success}`  of  `{total}`  members"
    )


@bot.on(hell_cmd(pattern=r"banall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"banall ?(.*)", allow_sudo=True))
async def _(event):
    result = await event.client(
        functions.channels.GetParticipantRequest(event.chat_id, event.client.uid)
    )
    if not result:
        return await eod(
            event, "Immunity Low!!"
        )
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
    await hell.edit(
        "**Bleck Magik Completed...**"
    )
    await bot.send_message(
        Config.LOGGER_ID,
        f"#BANALL \n\nSucessfully banned  `{success}`  out of  `{total}`  members!!",
    )
    

@bot.on(hell_cmd(pattern=r"unbanall ?(.*)"))
@bot.on(sudo_cmd(pattern=r"unbanall ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        await edit_or_reply(event, "Searching Participant Lists.")
        p = 0
        async for i in bot.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await bot(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await edit_or_reply(event, str(ex))
            else:
                p += 1
        await edit_or_reply(event, "{}: {} unbanned".format(event.chat_id, p))


@bot.on(hell_cmd(pattern="ikuck ?(.*)"))
@bot.on(sudo_cmd(pattern="ikuck ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await eod(event, "`You aren't an admin here!`")
            return False
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
    hell = await edit_or_reply(event, "Searching Participant Lists.")
    async for i in bot.iter_participants(event.chat_id):
        p = p + 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(hell, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(hell, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusOnline):
            q = q + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if isinstance(i.status, UserStatusRecently):
            r = r + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        if i.bot:
            b = b + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
                else:
                    c = c + 1
        elif i.deleted:
            d = d + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await eod(event, "I need admin priveleges to perform this action!")
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
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


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
