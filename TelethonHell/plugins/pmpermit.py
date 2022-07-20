import asyncio
import io

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

from TelethonHell.DB import pmpermit_sql as pm_sql

from . import *

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
PM_ON_OFF = Config.PM_PERMIT or "True"
PM_PARAMS = ['DISABLE', 'Disable', 'disable', 'OFF', 'Off', 'off', 'NO', 'No', 'no', 'FALSE', 'False', 'false']

@hell_cmd(pattern="block$")
async def block(event):
    if event.is_private:
        getuser = await event.client(
            GetFullUserRequest(await event.get_input_chat())
        )
        firstname = getuser.user.first_name
        if str(event.chat_id) in DEVLIST:
            return await eod(event, "**I can't block my creator !!**")
        if pm_sql.is_approved(event.chat_id):
            pm_sql.disapprove(event.chat_id)
        await eor(event, f"**Blocked:** [{firstname}](tg://user?id={event.chat_id})")
        await event.client(functions.contacts.BlockRequest(event.chat_id))
    elif event.is_group:
        reply = await event.get_reply_message()
        if not reply:
            return await eod(event, "Reply to someone to block them.")
        getuser = await event.client(GetFullUserRequest(reply.sender_id))
        firstname = getuser.user.first_name
        if str(reply.sender_id) in DEVLIST:
            return await eod(event, "**I can't block my creator !!**")
        if pm_sql.is_approved(event.chat_id):
            pm_sql.disapprove(event.chat_id)
        await eor(event, f"**Blocked:** [{firstname}](tg://user?id={reply.sender_id})")
        await event.client(functions.contacts.BlockRequest(reply_s.sender_id))
    else:
        return await parse_error(event, "Only groups and PMs supported.")


@hell_cmd(pattern="unblock$")
async def unblock(event):
    if event.is_private:
        getuser = await event.client(
            GetFullUserRequest(await event.get_input_chat())
        )
        firstname = getuser.user.first_name
        await eor(event, f"**Unblocked:** [{firstname}](tg://user?id={event.chat_id})")
        await event.client(functions.contacts.UnblockRequest(event.chat_id))
    elif event.is_group:
        reply = await event.get_reply_message()
        if not reply:
            return await eod(event, "Reply to someone to unblock them.")
        getuser = await event.client(GetFullUserRequest(reply.sender_id))
        firstname = getuser.user.first_name
        await eor(event, f"**Unblocked:** [{firstname}](tg://user?id={reply.sender_id})")
        await event.client(functions.contacts.UnblockRequest(reply.sender_id))
    else:
        return await parse_error(event, "Only groups and PMs supported.")


if PM_ON_OFF and PM_ON_OFF not in PM_PARAMS:
    @hell_handler(outgoing=True)
    async def _(event):
        if not event.is_private:
            return
        ForGo10God, _, _ = await client_id(event)
        sender = await event.client(GetFullUserRequest(await event.get_input_chat()))
        if str(event.chat_id) == str(ForGo10God):
            return
        if sender.user.bot:
            return
        if sender.user.verified:
            return
        if str(event.chat_id) in DEVLIST:
            return
        if not pm_sql.is_approved(event.chat_id):
            if not event.chat_id in PM_WARNS:
                pm_sql.approve(event.chat_id, "outgoing")
                x = await event.client.send_message(
                    event.chat_id,
                    "**Auto Approved because outgoing message.**",
                )
                await asyncio.sleep(5)
                await x.delete()

    @hell_cmd(pattern="(a|approve|allow)$")
    async def approve(event):
        if event.is_private:
            getuser = await event.client(
                GetFullUserRequest(await event.get_input_chat())
            )
            firstname = getuser.user.first_name
            if not pm_sql.is_approved(event.chat_id):
                if event.chat_id in PM_WARNS:
                    del PM_WARNS[event.chat_id]
                if event.chat_id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[event.chat_id].delete()
                    del PREV_REPLY_MESSAGE[event.chat_id]
                pm_sql.approve(event.chat_id, "Approved")
                await eod(event, f"**Approved:** [{firstname}](tg://user?id={event.chat_id})")
            elif pm_sql.is_approved(event.chat_id):
                await eod(event, "Already in approved list.")
        elif event.is_group:
            reply = await event.get_reply_message()
            if not reply:
                return await eod(event, "Reply to someone to approve them !!")
            if not pm_sql.is_approved(reply.sender_id):
                getuser = await event.client(GetFullUserRequest(reply.sender_id))
                firstname = getuser.user.first_name
                pm_sql.approve(reply.sender_id, "Approved")
                await eod(event, f"**Approved:** [{firstname}](tg://user?id={reply.sender_id})")
            elif pm_sql.is_approved(reply.sender_id):
                await eod(event, "User already approved !")
        else:
            return await parse_error(event, "Only groups and PMs supported.")

    @hell_cmd(pattern="(da|disapprove|disallow)$")
    async def disapprove(event):
        if event.is_private:
            getuser = await event.client(
                GetFullUserRequest(await event.get_input_chat())
            )
            firstname = getuser.user.first_name
            if str(event.chat_id) in DEVLIST:
                return await eod(event, "Can't disapprove my developer!")
            if pm_sql.is_approved(event.chat_id):
                pm_sql.disapprove(event.chat_id)
                await eod(event, f"**Disapproved:** [{firstname}](tg://user?id={event.chat_id})")
            elif not pm_sql.is_approved(event.chat_id):
                await eod(event, "User was not approved.")
        elif event.is_group:
            reply = await event.get_reply_message()
            if not reply:
                return await eod(event, "Reply to someone to disapprove them !!")
            if str(reply.sender_id) in DEVLIST:
                return await eod(event, "Can't disapprove my developer!")
            if pm_sql.is_approved(reply.sender_id):
                getuser = await event.client(GetFullUserRequest(reply.sender_id))
                firstname = getuser.user.first_name
                pm_sql.disapprove(reply.sender_id)
                await eod(event, f"**Disapproved:** [{firstname}](tg://user?id={reply.sender_id})")
            elif not pm_sql.is_approved(reply.sender_id):
                await eod(event, "User was not approved.")
        else:
            return await parse_error(event, "Only groups and PMs supported.")

    @hell_cmd(pattern="listapproved$")
    async def allapproved(event):
        approved_users = pm_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for user in approved_users:
                if user.reason:
                    APPROVED_PMs += f"👉 [{user.chat_id}](tg://user?id={user.chat_id}) :: `{user.reason}`\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{user.chat_id}](tg://user?id={user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "No PM approved yet."
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved_pms.txt"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await eor(event, APPROVED_PMs)

    @hell_handler(incoming=True)
    async def new_pm(event):
        if not event.is_private:
            return
        ForGo10God, _, hell_mention = await client_id(event)
        CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or None
        HELL_FIRST = f"🔥 𝙃𝙚𝙡𝙡𝘽𝙤𝙩 𝙋𝙈 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 🔥\n\nHello!! This is an automated message on behalf of {hell_mention}."
        if CSTM_PMP:
             HELL_FIRST += f"\n\n{CSTM_PMP}"
        if event.sender_id == ForGo10God:
            return
        if str(event.sender_id) in DEVLIST:
            return
        message_text = event.message.raw_text
        if HELL_FIRST == message_text:
            return
        sender = await event.client.get_entity(await event.get_input_chat())
        if str(event.chat_id) == str(ForGo10God):
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if PM_ON_OFF in PM_PARAMS:
            return
        if pm_sql.is_approved(event.chat_id):
            return
        if not pm_sql.is_approved(event.chat_id):
            await do_pm_permit_action(event.chat_id, event)

    async def do_pm_permit_action(chat_ids, event):
        if chat_ids not in PM_WARNS:
            PM_WARNS.update({chat_ids: 0})
        if PM_WARNS[chat_ids] == Config.MAX_SPAM:
            r = await event.reply("Enough of your spamming PM. \n\n**Blocked !!**")
            await event.client(functions.contacts.BlockRequest(chat_ids))
            if chat_ids in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_ids].delete()
            PREV_REPLY_MESSAGE[chat_ids] = r
            the_message = f"#BLOCK \n\n[User](tg://user?id={chat_ids}): `{chat_ids}` \n__Message Counts:__ `{PM_WARNS[chat_ids]}`\n"
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    the_message,
                    link_preview=False,
                    silent=True,
                )
                return
            except:
                pass
        tap = await event.client.inline_query(Config.BOT_USERNAME, "pm_warn")
        hell = await tap[0].click(event.chat_id)
        PM_WARNS[chat_ids] += 1
        if chat_ids in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_ids].delete()
        PREV_REPLY_MESSAGE[chat_ids] = hell


if Config.INSTANT_BLOCK == "ENABLE":
    @hell_handler(incoming=True)
    async def instant(event):
        sender = await event.client.get_entity(event.chat_id)
        ForGo10God, _, _ = await client_id(event)
        if event.chat_id == ForGo10God:
            return
        if str(event.chat_id) in DEVLIST:
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if pm_sql.is_approved(event.chat_id):
            return
        await event.client(functions.contacts.BlockRequest(event.chat_id))


CmdHelp("pm_permit").add_command(
    "allow", "<in pm>", "Approves the user in which pm cmd is used."
).add_command(
    "disallow", "<in pm>", "Disapprove User to PM you."
).add_command(
    "block", "<in pm>/<reply>", "Blocks the user"
).add_command(
    "unblock", "<in pm>/<reply>", "Unblocks the mentioned user."
).add_command(
    "listapproved", None, "Sends the list of all users approved by Hêllẞø†"
).add_info(
    "PM SECURITY"
).add_warning(
    "✅ Harmless Module."
).add()
