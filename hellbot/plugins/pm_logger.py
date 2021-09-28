import logging
import os
import sys

from telethon.events import NewMessage
from . import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)
NO_PM_LOG_USERS = []
lg_id = Config.PM_LOG_ID


@hell_cmd(pattern="save ?(.*)")
async def log(log_text):
    if lg_id is not None:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(lg_id)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await event.client.send_message(lg_id, textx)
        else:
            await eod(log_text, "`What am I supposed to save?`")
            return
        await eod(log_text, "`Saved Successfully`")
    else:
        await eod(log_text, "`This feature requires Logging to be enabled!`")


@hell_handler(func=lambda e: e.is_private)
async def monito_p_m_s(event):
    if lg_id is None:
        return
    sender = await event.get_sender()
    x = await event.client.get_entity(sender.id)
    cid = await client_id(event)
    ForGo10God = cid[0]
    if lg_id:
        if x.bot:
            return
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != ForGo10God:
            try:
                fwd_message = await event.client.forward_messages(lg_id, event.message, silent=True)
            except Exception as e:
                print(e)


@hell_cmd(pattern="elog ?(.*)")
async def set_no_log_p_m(event):
    if Config.PM_LOG_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.remove(chat.id)
                await eod(event, "Will Log Messages from this chat")


@hell_cmd(pattern="nlog ?(.*)")
async def set_no_log_p_m(event):
    if Config.PM_LOG_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await eod(event, "Won't Log Messages from this chat")


CmdHelp("pm_logger").add_command(
  "save", "<reply>", "Saves the replied message to your pm logger group/channel"
).add_command(
  "elog", "<chat>", "Enables logging pm messages from the selected chat."
).add_command(
  "nlog", "<chat>", "Disables logging pm messages from the selected chat. Use .elog to enable it again."
).add_info(
  "PM logging."
).add_warning(
  "✅ Harmless Module."
).add()
