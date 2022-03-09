import os

from telethon.tl.functions.users import GetFullUserRequest

from hellbot.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *


@hell_cmd(pattern="sudo$")
async def sudo(event):
    if Config.SUDO_USERS:
        if gvarstat("SUDO_USERS"):
            sudousers = gvarstat("SUDO_USERS")
            await eor(event, f"📍 **Sudo :**  `Enabled`\n\n📝 **Sudo users :**  `{sudousers}`")
    else:
        await eod(event, f"📍 **Sudo :**  `Disabled`")


@hell_cmd(pattern="addsudo(?:\s|$)([\s\S]*)")
async def add(event):
    suu = event.text[9:]
    suu = suu.split(" ")[0]
    if f"{hl}add " in event.text:
        return
    ok = await eor(event, "**🚀 Adding Sudo User...**")
    rply = await event.get_reply_message()
    if not suu and not rply:
        return await eod(ok, "Either reply to a user or give user id to add them to your sudo users list.")
    if suu:
        if not suu.isnumeric():
            return await eod(ok, "Give user id only.")
    user = await get_user(event) if rply else suu
    user = str(user)
    if gvarstat("SUDO_USERS"):
        exist = gvarstat("SUDO_USERS")
        int_list = await make_int(exist)
        if int(user) in int_list:
            return await eod(ok, "User is already in sudo list")
        final = f"{str(exist)} {str(user)}"
    else:
        final = user
    addgvar("SUDO_USERS", final)
    await eod(ok, f"**Successfully Added New Sudo User.** \n\n__Reload your bot to apply changes. Do__ `{hl}reload`")


@hell_cmd(pattern="rmsudo(?:\s|$)([\s\S]*)")
async def _(event):
    suu = event.text[8:]
    suu = suu.split(" ")[0]
    ok = await eor(event, "**🚫 Removing Sudo User...**")
    rply = await event.get_reply_message()
    if not suu and not rply:
        return await eod(ok, "Either reply to a user or give user id to remove them from your sudo users list.")
    if suu:
        if not suu.isnumeric():
            return await eod(ok, "Give user id only.")
    user = await get_user(event) if rply else suu
    user = str(user)
    
    if gvarstat("SUDO_USERS"):
        x = gvarstat("SUDO_USERS")
        int_list = await make_int(x)
        if int(user) in int_list:
            int_list.remove(int(user))
            str_list = [str(xyz) for xyz in int_list]
            final = " ".join(str_list)
            delgvar("SUDO_USERS")
            addgvar("SUDO_USERS", final)
            await eod(ok, f"❌** Removed**  `{str(user)}`  **from Sudo User.**\n\n__Reload your bot to apply changes. Do__ `{hl}reload`")
        else:
            return await eod(ok, "This user is not in your sudo users list.")
    else:
        await eod(ok, "**Sudo Is Disabled !!**")


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
