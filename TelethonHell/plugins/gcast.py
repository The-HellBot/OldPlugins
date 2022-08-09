from . import *


@hell_cmd(pattern="gcast(?:\s|$)([\s\S]*)")
async def _(event):
    reply_msg = await event.get_reply_message()
    flag = str(event.text.split(" ", 2)[1])
    if reply_msg:
        OwO = reply_msg.text
        file = reply_msg.media
    else:
        OwO = str(event.text.split(" ", 2)[2])
        file = None
    if not OwO:
        return await parse_error(event, "Nothing given to Gcast.")
    hel_ = await eor(event, "`Gcasting message...`")
    sed = 0
    owo = 0
    if flag.lower() == "-all":
        async for allhell in event.client.iter_dialogs():
            chat = allhell.id
            try:
                if chat != -1001496036895:
                    await event.client.send_message(chat, text=OwO, file=file)
                    owo += 1
                elif chat == -1001496036895:
                    pass
            except BaseException:
                sed += 1
    elif flag.lower() == "-pvt":
        async for pvthell in event.client.iter_dialogs():
            if pvthell.is_user and not pvthell.entity.bot:
                chat = pvthell.id
                try:
                    await event.client.send_message(chat, text=OwO, file=file)
                    owo += 1
                except BaseException:
                    sed += 1
    elif flag.lower() == "-grp":
        async for ghell in event.client.iter_dialogs():
            if ghell.is_group:
                chat = ghell.id
                try:
                    if chat != -1001496036895:
                        await event.client.send_message(chat, text=OwO, file=file)
                        owo += 1
                    elif chat == -1001496036895:
                        pass
                except BaseException:
                    sed += 1
    else:
        return await hel_.edit(
            "Please give a flag to Gcast message. \n\n**Available flags are :** \n• -all : To Gcast in all chats. \n• -pvt : To Gcast in private chats. \n• -grp : To Gcast in groups."
        )
    UwU = sed + owo
    if flag.lower() == "-all":
        omk = "Chats"
    elif flag.lower() == "-pvt":
        omk = "PM"
    elif flag.lower() == "-grp":
        omk = "Groups"
        
    text_to_send = f"**📍 Sent in :** `{owo} {omk}`\n**📍 Failed in :** `{sed} {omk}`\n**📍 Total :** `{UwU} {omk}`"
    await hel_.edit(f"**Gcast Executed Successfully !!** \n\n{text_to_send}")
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
