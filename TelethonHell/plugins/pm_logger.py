from TelethonHell.DB.pmlogger_sql import (add_nolog, del_nolog, get_all_nolog,
                                          is_nolog)
from TelethonHell.plugins import *


@hell_cmd(pattern="save(?:\s|$)([\s\S]*)")
async def _(event):
    if f"{hl}savewelcome" in event.text:
        return
    ForGo10God, _, _ = await client_id(event)
    if Config.PM_LOGGER != 0:
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            await reply_msg.forward_to(Config.PM_LOGGER)
        elif event.pattern_match.group(1):
            user = f"#LOG | Chat ID: `{event.chat_id}`\n\n"
            textx = user + event.pattern_match.group(1)
            await event.client.send_message(Config.PM_LOGGER, textx)
        else:
            await parse_error(event, "Nothing given to save !")
            return
        await eod(event, "`Saved Successfully`")
    else:
        if event.reply_to_msg_id:
            reply_msg = await event.get_reply_message()
            await reply_msg.forward_to(ForGo10God)
        elif event.pattern_match.group(1):
            user = f"#LOG | Chat ID: `{event.chat_id}`\n\n"
            textx = user + event.pattern_match.group(1)
            await event.client.send_message(ForGo10God, textx)
        else:
            await parse_error(event, "Nothing given to save !")
            return
        await eod(event, "`Saved Successfully`")


@hell_handler(func=lambda e: e.is_private, incoming=True)
async def _(event):
    if Config.PM_LOGGER == 0:
        return
    ForGo10God, _, _ = await client_id(event)
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if Config.PM_LOGGER:
            if is_nolog(str(chat.id)):
                return
            if chat.id != ForGo10God:
                try:
                    await event.client.forward_messages(
                        Config.PM_LOGGER, event.message, silent=True
                    )
                except Exception as e:
                    LOGS.info(str(e))


@hell_cmd(pattern="elog$")
async def _(event):
    if Config.PM_LOGGER != 0:
        chat = await event.get_chat()
        if event.is_private:
            try:
                del_nolog(str(chat.id))
                await eod(event, "Will Log Messages from this chat")
            except Exception as e:
                await parse_error(event, e)
        else:
            await parse_error(event, "Chat is not a PM.")
    else:
        await parse_error(event, "`PM_LOGGER` is not configured.", False)


@hell_cmd(pattern="nlog$")
async def _(event):
    if Config.PM_LOGGER != 0:
        chat = await event.get_chat()
        if event.is_private:
            if is_nolog(str(chat.id)):
                return await eod(event, "Already logging is disabled for this chat.")
            add_nolog(str(chat.id))
            await eod(event, "Won't Log Messages from this chat")
        else:
            await parse_error(event, "Chat is not a PM.")
    else:
        await parse_error(event, "`PM_LOGGER` is not configured.", False)


@hell_cmd(pattern="allnolog$")
async def _(event):
    text = "**Not logging messages from:**\n"
    all_nolog = get_all_nolog()
    for i in all_nolog:
        chat = i.chat_id
        text += f"\n•  `{chat}`"
    await eor(event, text)


CmdHelp("pm_logger").add_command(
    "save", "<reply>", "Saves the replied message to your pm logger group/channel"
).add_command(
    "elog", None, "Enables logging pm messages from the selected chat."
).add_command(
    "nlog", None, f"Disables logging pm messages from the selected chat. Use {hl}elog to enable it again."
).add_command(
    "allnolog", None, "Get the list of all groups with pm logging disabled."
).add_info(
    "PM logging."
).add_warning(
    "✅ Harmless Module."
).add()
