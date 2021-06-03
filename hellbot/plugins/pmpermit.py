import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

from hellbot.plugins.sql import pmpermit_sql as pmpermit_sql
from . import *

hell_pic = Config.PMPERMIT_PIC
cstm_pmp = Config.CUSTOM_PMPERMIT

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**🚫 Blocked and Reported**"
USER_BOT_NO_WARN = (
    "**🔥 Hêllẞø† Prîvã†é Sêçürïty Prø†öçõl 🔥**\n\nThis is to inform you that"
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**You have** `{}/{}` **Warnings...**"
)


@bot.on(hell_cmd(pattern="(a|allow|approve)(?: |$)(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id in PM_WARNS:
                del PM_WARNS[chat.id]
            if chat.id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat.id].delete()
                del PREV_REPLY_MESSAGE[chat.id]
            pmpermit_sql.approve(chat.id, reason)
            await event.edit(
                "🔰 **Approved** [{}](tg://user?id={}) **to PM you!!**".format(firstname, chat.id)
            )
            await asyncio.sleep(3)
            await event.delete()


# Approve outgoing


@bot.on(events.NewMessage(outgoing=True))
async def you_dm_niqq(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            if chat.id not in PM_WARNS:
                pmpermit_sql.approve(chat.id, "outgoing")
                logit = "#Auto_Approved\n\n**User -**  [{}](tg://user?id={})".format(
                    chat.first_name, chat.id
                )
                try:
                    await bot.send_message(Config.LOGGER_ID, logit)
                except BaseException:
                    pass


@bot.on(hell_cmd(pattern="block ?(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1432756163:
            await event.edit("😤 **You Tried to Block My Owner!!!!\n\n😪 Ok then! Good bye fro 100secs.**")
            await asyncio.sleep(100)
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "🤧 Go get some sleep retard!! \n\n**Blocked**  [{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))


@bot.on(hell_cmd(pattern="(da|disallow|disapprove)(?: |$)(.*)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    replied_user = await event.client(GetFullUserRequest(event.chat_id))
    firstname = replied_user.user.first_name
    event.pattern_match.group(1)
    chat = await event.get_chat()
    if event.is_private:
        if chat.id == 1432756163:
            await event.edit("I Can't Disapprove My Master 😐")
        else:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "[{}](tg://user?id={}) disapproved to PM.".format(
                        firstname, chat.id
                    )
                )


@bot.on(hell_cmd(pattern="(la|listallowed|listapproved)"))
async def approve_p_m(event):
    if event.fwd_from:
        return
    approved_users = pmpermit_sql.get_all_approved()
    APPROVED_PMs = "Currently Approved Users In Hêllẞø† DataBase\n\n"
    if len(approved_users) > 0:
        for a_user in approved_users:
            if a_user.reason:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
    else:
        APPROVED_PMs = "No Approved Users Yet!!"
    if len(APPROVED_PMs) > 4095:
        with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
            out_file.name = "approved.pms.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Approved Users In DataBase.",
                thumb=hell_logo,
                reply_to=event,
            )
            await event.delete()
    else:
        await event.edit(APPROVED_PMs)


@bot.on(events.NewMessage(incoming=True))
async def on_new_private_message(event):
    if event.sender_id == bot.uid:
        return

    if Config.LOGGER_ID is None:
        return

    if not event.is_private:
        return

    message_text = event.message.message
    chat_id = event.sender_id

    message_text.lower()
    if USER_BOT_NO_WARN == message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return
    sender = await bot.get_entity(chat_id)

    if chat_id == bot.uid:

        # don't log Saved Messages

        return

    if sender.bot:

        # don't log bots

        return

    if sender.verified:

        # don't log verified accounts

        return

    if not pmpermit_sql.is_approved(chat_id):
        # pm permit
        await do_pm_permit_action(chat_id, event)


async def do_pm_permit_action(chat_id, event):
    if Config.PM_PERMIT == "DISABLE":
        return
    if chat_id not in PM_WARNS:
        PM_WARNS.update({chat_id: 0})
    if PM_WARNS[chat_id] == Config.MAX_SPAM:
        r = await event.reply(USER_BOT_WARN_ZERO)
        await asyncio.sleep(3)
        await event.client(functions.contacts.BlockRequest(chat_id))
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r
        the_message = ""
        the_message += "#BLOCKED_PMs\n\n"
        the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
        the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
        # the_message += f"Media: {message_media}"
        try:
            await event.client.send_message(
                entity=Config.LOGGER_ID,
                message=the_message,
                # reply_to=,
                # parse_mode="html",
                link_preview=False,
                # file=message_media,
                silent=True,
            )
            return
        except BaseException:
            return
    # inline pmpermit menu
    mybot = Config.BOT_USERNAME
    MSG = USER_BOT_NO_WARN.format(
        hell_mention, mssge, PM_WARNS[chat_id] + 1, Config.MAX_SPAM
    )
    hell_ = await bot.inline_query(mybot, MSG)
    r = await hell_[0].click(event.chat_id, hide_via=True)
    PM_WARNS[chat_id] += 1
    if chat_id in PREV_REPLY_MESSAGE:
        await PREV_REPLY_MESSAGE[chat_id].delete()
    PREV_REPLY_MESSAGE[chat_id] = r


# Do not touch the below codes!


@bot.on(
    events.NewMessage(
        incoming=True, from_users=(1432756163)
    )
)
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "Dad Iz Here 🔥")
            await bot.send_message(chat, "😎 **Here Comes My God!! 😆 Consider Yourself Lucky**")


# instant block
NEEDIT = Config.INSTANT_BLOCK
if NEEDIT == "ENABLE":

    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        event.message.message
        event.message.media
        event.message.id
        event.message.to_id
        chat_id = event.chat_id
        sender = await bot.get_entity(chat_id)
        if chat_id == bot.uid:
            return
        if chat_id == 1432756163:
            return
        if sender.bot:
            return
        if sender.verified:
            return
        if not pmpermit_sql.is_approved(chat_id):
            await bot(functions.contacts.BlockRequest(chat_id))


CmdHelp("pm_permit").add_command(
  "allow", "<in pm>", "Approves the user in which pm cmd is used."
).add_command(
  "disallow", "<in pm>", "Disapprove User to PM you."
).add_command(
  "block", "<in pm>", "Blocks the user"
).add_command(
  "listapproved", None, "Sends the list of all users approved by Hêllẞø†"
).add_info(
  "PM SECURITY"
).add_warning(
  "✅ Harmless Module."
).add()
