import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

from hellbot.sql import pmpermit_sql as pm_sql
from . import *

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
PM_ON_OFF = Config.PM_PERMIT
HELL_ZERO = "Go get some sleep retard. \n\n**Blocked !!**"


@hell_cmd(pattern="unblock$")
async def unb(event):
    if event.is_private:
        replied_user = await event.client(GetFullUserRequest (await event.get_input_chat()))
        firstname = replied_user.user.first_name
        await eor(event, f"**Unblocked [{firstname}](tg://user?id={event.chat_id}) !!**")
        await event.client(functions.contacts.UnblockRequest(event.chat_id))
    elif event.is_group:
        reply_s = await event.get_reply_message()
        if not reply_s:
            await eod(event, "Reply to someone to unblock them..")
            return
        replied_user = await event.client(GetFullUserRequest(reply_s.sender_id))
        firstname = replied_user.user.first_name
        await eor(event, f"**Unblocked [{firstname}](tg://user?id={reply_s.sender_id}) !!**")
        await event.client(functions.contacts.UnblockRequest(reply_s.sender_id))


@hell_cmd(pattern="block$")
async def approve_p_m(event):
    if event.is_private:
        replied_user = await event.client(GetFullUserRequest(await event.get_input_chat()))
        firstname = replied_user.user.first_name
        if str(event.chat_id) in DEVLIST:
            await eod(event, "**I can't block my creator !!**")
            return
        if pm_sql.is_approved(event.chat_id):
            pm_sql.disapprove(event.chat_id)
        await eor(event, "Go Get Some Sleep Retard !! \n\n**Blocked** [{}](tg://user?id={})".format(firstname, event.chat_id))
        await event.client(functions.contacts.BlockRequest(event.chat_id))
    elif event.is_group:
        reply_s = await event.get_reply_message()
        if not reply_s:
            await eod(event, "Reply to someone to block them..")
            return
        replied_user = await event.client(GetFullUserRequest(reply_s.sender_id))
        firstname = replied_user.user.first_name
        if str(reply_s.sender_id) in DEVLIST:
            await eod(event, "**I can't Block My Creator !!**")
            return
        if pm_sql.is_approved(event.chat_id):
            pm_sql.disapprove(event.chat_id)
        await eor(event, "Go fuck yourself !! \n\n**Blocked** [{}](tg://user?id={})".format(firstname, reply_s.sender_id))
        await event.client(functions.contacts.BlockRequest(reply_s.sender_id))


if PM_ON_OFF != "DISABLE":
    @H1.on(events.NewMessage(outgoing=True))
    async def _(event):
        if not event.is_private:
            return
        cid = await client_id(event)
        ForGo10God = cid[0]
        chat_ids = event.chat_id
        sender = await event.client(GetFullUserRequest(await event.get_input_chat()))
        first_name = sender.user.first_name
        if chat_ids == ForGo10God:
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
                x = await event.client.send_message(event.chat_id, "**Auto Approved because outgoing message.**")
                await asyncio.sleep(4)
                await x.delete()


    @H1.on(admin_cmd(pattern="(a|approve|allow)$"))
    async def approve(event):
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(await event.get_input_chat()))
            firstname = replied_user.user.first_name
            if not pm_sql.is_approved(event.chat_id):
                if event.chat_id in PM_WARNS:
                    del PM_WARNS[event.chat_id]
                if event.chat_id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[event.chat_id].delete()
                    del PREV_REPLY_MESSAGE[event.chat_id]
                pm_sql.approve(event.chat_id, "Approved")
                await eod(event,
                    "Approved to pm [{}](tg://user?id={})".format(firstname, event.chat_id)
                )
            elif pm_sql.is_approved(event.chat_id):
                await eod(event, 'Already In Approved List!!')
        elif event.is_group:
            reply_s = await event.get_reply_message()
            if not reply_s:
                await eod(event, 'Reply to someone to approve them !!')
                return
            if not pm_sql.is_approved(reply_s.sender_id):
                replied_user = await event.client(GetFullUserRequest(reply_s.sender_id))
                firstname = replied_user.user.first_name
                pm_sql.approve(reply_s.sender_id, "Approved")
                await eod(event,
                        "Approved to pm [{}](tg://user?id={})".format(firstname, reply_s.sender_id)
                    )
            elif pm_sql.is_approved(reply_s.sender_id):
                await eod(event, 'User Already Approved !')

    @H1.on(admin_cmd(pattern="(da|disapprove|disallow)$"))
    async def dapprove(event):
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(await event.get_input_chat()))
            firstname = replied_user.user.first_name
            if str(event.chat_id) in DEVLIST:
                await eod(event, "**Unable to disapprove this user. Seems like God !!**")
                return
            if pm_sql.is_approved(event.chat_id):
                pm_sql.disapprove(event.chat_id)
                await eod(event,
                    "Disapproved User [{}](tg://user?id={})".format(firstname, event.chat_id)
                )
            elif not pm_sql.is_approved(event.chat_id):
                await eod(event, "I don't think he was approved !!")
        elif event.is_group:
            reply_s = await event.get_reply_message()
            if not reply_s:
                await eod(event, "Reply to someone to Disapprove them !!")
                return
            if str(reply_s.sender_id) in DEVLIST:
                await eod(event, "**Unable to disapprove this user. Seems like God !!**")
                return
            if pm_sql.is_approved(reply_s.sender_id):
                replied_user = await event.client(GetFullUserRequest(reply_s.sender_id))
                firstname = replied_user.user.first_name
                pm_sql.disapprove(reply_s.sender_id)
                await eod(event,
                    "Disapproved User [{}](tg://user?id={})".format(firstname, reply_s.sender_id)
                )
            elif not pm_sql.is_approved(reply_s.sender_id):
                await eod(event, 'Not even in my approved list.')

    @H1.on(admin_cmd(pattern="listapproved$"))
    async def approve_p_m(event):
        approved_users = pm_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.txt"
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

    @H1.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if not event.is_private:
            return
        cid = await client_id(event)
        ForGo10God, hell_mention = cid[0], cid[2]
        CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
        HELL_FIRST = "**🔥 Hêllẞø† Prîvã†é Sêçürïty Prø†öçõl 🔥**\n\nHello!! Welcome to {}'s PM. This is an automated message.\n\n{}".format(hell_mention, CSTM_PMP)
        if event.sender_id == ForGo10God:
            return
        if str(event.sender_id) in DEVLIST:
            return
        if Config.LOGGER_ID is None:
            await event.client.send_message(ForGo10God, "Please Set `LOGGER_ID` For Working Of Pm Permit")
            return
        message_text = event.message.raw_text
        chat_ids = event.sender_id
        if HELL_FIRST == message_text:
            return
        sender = await event.client.get_entity(await event.get_input_chat())
        if chat_ids == ForGo10God:
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if PM_ON_OFF == "DISABLE":
            return
        if pm_sql.is_approved(chat_ids):
            return
        if not pm_sql.is_approved(chat_ids):
            await do_pm_permit_action(chat_ids, event)


    async def do_pm_permit_action(chat_ids, event):
        if chat_ids not in PM_WARNS:
            PM_WARNS.update({chat_ids: 0})
        if PM_WARNS[chat_ids] == Config.MAX_SPAM:
            r = await event.reply(HELL_ZERO)
            await event.client(functions.contacts.BlockRequest(chat_ids))
            if chat_ids in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_ids].delete()
            PREV_REPLY_MESSAGE[chat_ids] = r
            the_message = ""
            the_message += "#BLOCK\n\n"
            the_message += f"[User](tg://user?id={chat_ids}): {chat_ids}\n"
            the_message += f"Message Counts: {PM_WARNS[chat_ids]}\n"
            try:
                await event.client.send_message(
                    Config.LOGGER_ID,
                    the_message,
                    link_preview=False,
                    silent=True,
                )
                return
            except BaseException:
                pass

        tap = await event.client.inline_query(Config.BOT_USERNAME, "pm_warn")
        hel_ = await tap[0].click(event.chat_id)
        PM_WARNS[chat_ids] += 1
        if chat_ids in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_ids].delete()
        PREV_REPLY_MESSAGE[chat_ids] = hel_


if Config.INSTANT_BLOCK == "ENABLE":
    @H1.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        chat_id = event.chat_id
        sender = await event.client.get_entity(chat_id)
        cid = await client_id(event)
        ForGo10God = cid[0]
        if chat_id == ForGo10God:
            return
        if str(chat_id) in DEVLIST:
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if not pmpermit_sql.is_approved(chat_id):
            await event.client(functions.contacts.BlockRequest(chat_id))


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
