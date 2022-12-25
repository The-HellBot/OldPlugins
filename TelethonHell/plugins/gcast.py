from TelethonHell.plugins import *


@hell_cmd(pattern="gcast(?:\s|$)([\s\S]*)")
async def _(event):
    reply_msg = await event.get_reply_message()
    flag = str(event.text.split(" ", 2)[1])
    file = None
    if reply_msg:
        OwO = reply_msg.text
        file = reply_msg.media
    else:
        OwO = str(event.text.split(" ", 2)[2])
        file = None
    if not OwO:
        return await parse_error(event, "Nothing given to Gcast.")
    hell = await eor(event, "`Gcasting message...`")
    sed = 0
    owo = 0
    async for chats in event.client.iter_dialogs():
        if flag.lower() == "-all":
            chat = chats.id
            try:
                await event.client.send_message(chat, message=OwO, file=file)
                owo += 1
            except Exception as e:
                LOGS.info(str(e))
                sed += 1
        elif flag.lower() == "-pvt":
            if chats.is_user and not chats.entity.bot:
                chat = chats.id
                try:
                    await event.client.send_message(chat, message=OwO, file=file)
                    owo += 1
                except Exception as e:
                    LOGS.info(str(e))
                    sed += 1
        elif flag.lower() == "-grp":
            if chats.is_group:
                chat = chats.id
                try:
                    await event.client.send_message(chat, message=OwO, file=file)
                    owo += 1
                except Exception as e:
                    LOGS.info(str(e))
                    sed += 1
        else:
            return await hell.edit(
                "Please give a flag to Gcast message. \n\n**Available flags are:** \n• -all : To Gcast in all chats. \n• -pvt : To Gcast in private chats. \n• -grp : To Gcast in groups."
            )
    UwU = sed + owo
    if flag.lower() == "-all":
        omk = "Chats"
    elif flag.lower() == "-pvt":
        omk = "PM"
    elif flag.lower() == "-grp":
        omk = "Groups"
        
    text_to_send = f"**📍 Sent in :** `{owo} {omk}`\n**📍 Failed in :** `{sed} {omk}`\n**📍 Total :** `{UwU} {omk}`"
    await hell.edit(f"**Gcast Executed Successfully !!** \n\n{text_to_send}")
    await event.client.send_message(Config.LOGGER_ID, f"#GCAST #{flag[1:].upper()} \n\n{text_to_send}")


CmdHelp("gcast").add_command(
    "gcast", "<flag> <text/reply>", "Globally Broadcast the replied or given message based on flag given.", f"gcast -all Hello / {hl}gcast -grp Hello / {hl}gcast -pvt Hello"
).add_info(
    "Global Broadcast."
).add_extra(
    "🚩 Flags", "-all, -pvt, -grp"
).add_warning(
    "✅ Harmless Module."
).add()
