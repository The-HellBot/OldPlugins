import os
from telethon.tl.functions.users import GetFullUserRequest

from . import *
from .sql import sudo_sql as s_ql

@bot.on(hell_cmd(pattern="sudo$", outgoing=True))
async def sudo(event):
    if Config.SUDO_USERS == "True":  
        users = list(s_ql.all_sudo())
        sudo_users = list(s_ql.all_sudo())
        if len(sudo) > 0:
            SUDO_LIST = "**🚀 Sudo Users :**\n"
            for user in sudo_users:
                SUDO_LIST += f"📍 [{user.chat_id}](tg://user?id={user.chat_id})\t{users}\n"
        else:
            SUDO_LIST = "**No User Added To Sudo !**"
        await eor(event, SUDO_LIST)
    else:
        await eod(event, f"📍 **Sudo :**  `Disabled`")
       

@bot.on(hell_cmd(pattern="addsudo(?: |$)"))
async def add(event):
    hell = await eor(event, "**Adding To Sudo...**")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(hell, "**To Add user in SUDO i need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(hell, "**Can't Add Myself In Sudo**")
    if s_ql.in_sudo(userid):
        return await eod(hell, "**User Is Already In Sudo**")
    s_ql.add_sudo(userid)
    await hell.edit(f"Added [{name}](tg://user?id={userid}) To Sudo Users !")


@bot.on(hell_cmd(pattern="rmsudo(?: |$)"))
async def _(event):
    hell = await eor(event, "**Removing From Sudo...**")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(hell, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not s_ql.in_sudo(userid):
        return await eod(hell, "**User Is Not In Sudo List**")
    s_ql.rem_sudo(userid)
    await hell.edit(
        f"**📍 Removed** [{name}](tg://user?id={userid}) **From Sudo !**",
    )

async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    target = replied_user.user.id
    return target


CmdHelp("sudo").add_command(
  "sudo", None, "Check If Your Bot Has Sudo Enabled!!"
).add_command(
  "addsudo", "<reply to user>", "Adds replied user to sudo list."
).add_command(
  "rmsudo", "<reply to user>", "Removes the replied user from your sudo list if already added."
).add_info(
  "Manage Sudo."
).add_warning(
  "⚠️ Grant Sudo Access to someone you trust!"
).add()
