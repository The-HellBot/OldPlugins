from telethon.events import InlineQuery, callbackquery
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from hellbot.sql.fsub_sql import *
from . import *


@H1.on(events.ChatAction())
async def forcesub(event):
    if all_fsub() == None:
        return
    if not (event.user_joined or event.user_added):
        return
    if not is_fsub(event.chat_id):
        return
    user = await event.get_user()
    if user.bot:
        return
    xyz = is_fsub(event.chat_id)
    joinchat = xyz.channel
    tgbotusername = Config.BOT_USERNAME
    try:
        await event.client(GetParticipantRequest(int(joinchat), user.id))
    except UserNotParticipantError:
        await event.client.edit_permissions(event.chat_id, user.id, send_messages=False)
        res = await event.client.inline_query(tgbotusername, f"fsub {user.id}+{joinchat}")
        await res[0].click(event.chat_id, reply_to=event.action_message.id)


@hell_cmd(pattern="fsub ?(.*)")
async def _(event):
    if event.is_private:
        await eor(event, "This is meant to be used in groups only!!")
        return
    hunter = event.pattern_match.group(1)
    if not hunter:
        return await eod(event, "Need a Channel Username Or Channel ID 🥴")
    if hunter.startswith("@"):
        ch = hunter
    else:
        try:
            ch = int(hunter)
        except BaseException:
            return await eod(event, "⚠️ **Error !** \n\nChannel ID invalid. Please Recheck It !")
    try:
        hunter = (await event.client.get_entity(ch)).id
    except BaseException:
        return await eod(event, "⚠️ **Error !** \n\nChannel ID invalid. Please Recheck It !")
    if not str(hunter).startswith("-100"):
        hunter = int(f"-100{hunter}")
    add_fsub(event.chat_id, hunter)
    await eor(event, "Implementing **Force Subscribe** In This Channel !!")


@hell_cmd(pattern="rmfsub$")
async def removef(event):
    if is_fsub(event.chat_id):
        rm_fsub(event.chat_id)
        await eor(event, "Deactivated **Force Subscribe** In This Channel !!")
    else:
        return await eod(event, "I don't think force sub was activated here.")
    

@hell_cmd(pattern="chfsub")
async def getfsub(event):
    x = is_fsub(event.chat_id)
    if not x:
        return await eod(event, "Force Subscribe Is Disabled Here..")
    a = x.chat_id
    b = x.channel
    xx = await event.client.get_entity(int(a))
    yy = await event.client.get_entity(int(b))
    uname = f"@{xx.username}" or "No Username"
    usern = f"@{yy.username}" or "No Username"
    await eor(event, f"**ForceSub Enabled !!**\n\n» __Force Subscribe to__ {yy.title} ~ {usern} \n» __For Chat__ {xx.title} ~ {uname}")


@hell_cmd(pattern="lsfsub$")
async def list(event):
    channels = all_fsub()
    CHANNEL_LIST = "**🚀 Fsub Enabled For & In :**\n\n"
    if len(channels) > 0:
        for hunter in channels:
            a = hunter.chat_id
            b = hunter.channel
            xx = await event.client.get_entity(int(a))
            yy = await event.client.get_entity(int(b))
            uname = f"@{xx.username}" or "No Username"
            usern = f"@{yy.username}" or "No Username"
            CHANNEL_LIST += f"»» **FSub to ** [ {yy.title} ~ {usern} ] **in chat** [ {xx.title} {uname} ]\n"
    else:
        CHANNEL_LIST = "No Chat Found With Active Force Subscribe."
    await eor(event, CHANNEL_LIST)


CmdHelp("forcesub").add_command(
  "fsub", "<channel username/id>", "Activates Force Subscribe In The Chat"
).add_command(
  "rmfsub", None, "Removes the chat from Force Subscribe"
).add_command(
  "chfsub", None, "Checks for the Status of Force Subscribe In The Chat."
).add_command(
  "lsfsub", None, "Gives the list of all chats with force subscribe enabled."
).add_warning(
  "✅ Harmless Module."
).add_info(
  "Force Them To Join. \n**📌 Note :** You need to be admin jn both the chat to use this module."
).add()
