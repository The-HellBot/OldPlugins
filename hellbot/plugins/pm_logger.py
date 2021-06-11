import asyncio
import logging
import os
import sys
from asyncio import sleep

from telethon import events

from . import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)

NO_PM_LOG_USERS = []

lg_id = Config.PM_LOG_ID


@bot.on(hell_cmd(pattern=r"save(?: |$)([\s\S]*)", outgoing=True))
async def log(log_text):
    if lg_id is not None:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(lg_id)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(lg_id, textx)
        else:
            await eod(log_text, "`What am I supposed to save?`")
            return
        await eod(log_text, "`Saved Successfully`")
    else:
        await eod(log_text, "`This feature requires Logging to be enabled!`")


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    if lg_id is None:
        return
    sender = await event.get_sender()
    if lg_id and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id != bot.uid:
            try:
                e = await bot.get_entity(int(Config.PM_LOG_ID))
                fwd_message = await bot.forward_messages(e, event.message, silent=True)
            except Exception as e:
                # logger.warn(str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)


@bot.on(hell_cmd(pattern="elog ?(.*)"))
async def set_no_log_p_m(event):
    if Config.PM_LOG_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.remove(chat.id)
                await event.edit("Will Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()


@bot.on(hell_cmd(pattern="nlog ?(.*)"))
async def set_no_log_p_m(event):
    if Config.PM_LOG_ID is not None:
        event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id not in NO_PM_LOG_USERS:
                NO_PM_LOG_USERS.append(chat.id)
                await event.edit("Won't Log Messages from this chat")
                await asyncio.sleep(3)
                await event.delete()


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
