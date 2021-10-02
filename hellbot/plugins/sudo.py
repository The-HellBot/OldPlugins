import os
import heroku3

from telethon.tl.functions.users import GetFullUserRequest

from . import *

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
sudousers = os.environ.get("SUDO_USERS") or ""


@hell_cmd(pattern="sudo$")
async def sudo(event):
    sudo = "True" if Config.SUDO_USERS else "False"
    users = sudousers
    if sudo == "True":
        await eor(event, f"📍 **Sudo :**  `Enabled`\n\n📝 **Sudo users :**  `{users}`")
    else:
        await eod(event, f"📍 **Sudo :**  `Disabled`")


@hell_cmd(pattern="addsudo ?(.*)")
async def add(event):
    suu = event.text[9:]
    if f"{hl}add " in event.text:
        return
    ok = await eor(event, "**🚀 Adding Sudo User...**")
    bot = "SUDO_USERS"
    rply = await event.get_reply_message()
    if not suu and not rply:
        return await ok.edit("Either reply to a user or give user ids to add them to your sudo users list.")
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        await eod(ok, "**Please Set-Up**  `HEROKU_APP_NAME` **to add sudo users!!**")
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu:
        target = suu
    elif rply:
        target = await get_user(event)
    suudo = f"{sudousers} {target}"
    newsudo = suudo.replace("{", "")
    newsudo = newsudo.replace("}", "")
    await ok.edit(f"✅** Added**  `{target}`  **in Sudo User.**\n\n __Restarting Heroku to Apply Changes. Wait for a minute.__")
    heroku_Config[bot] = newsudo


@hell_cmd(pattern="rmsudo ?(.*)")
async def _(event):
    suu = event.text[8:]
    ok = await eor(event, "**🚫 Removing Sudo User...**")
    bot = "SUDO_USERS"
    rply = await event.get_reply_message()
    if not suu and not rply:
        return await ok.edit("Either reply to a user or give user ids to remove them from your sudo users list.")
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        await eod(ok, "**Please Set-Up**  HEROKU_APP_NAME to remove sudo users!!")
        return
    heroku_Config = app.config()
    if event is None:
        return
    if suu != "" and suu.isnumeric():
        target = suu
    elif rply:
        target = await get_user(event)
    gett = str(target)
    if gett in sudousers:
        newsudo = sudousers.replace(gett, "")
        await ok.edit(f"❌** Removed**  `{target}`  from Sudo User.\n\n Restarting Heroku to Apply Changes. Wait for a minute.")
        heroku_Config[bot] = newsudo
    else:
        await ok.edit("**😑This user is not in your Sudo Users List.**")

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
