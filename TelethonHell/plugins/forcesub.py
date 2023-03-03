from telethon import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from TelethonHell.DB.fsub_sql import *
from TelethonHell.plugins import *


@bot.on(events.ChatAction())
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
    try:
        await event.client(GetParticipantRequest(int(joinchat), user.id))
    except UserNotParticipantError:
        await event.client.edit_permissions(event.chat_id, user.id, send_messages=False)
        channel = await event.client.get_entity(int(joinchat))
        user = await event.client.get_entity(int(user.id))
        if not channel.username:
            channel_link = (await event.client(ExportChatInviteRequest(channel))).link
        else:
            channel_link = "https://t.me/" + channel.username
        capt = f"**👋 Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**📍 You need to Join** {channel.title} **to chat in this group.**"
        btns = [
            Button.url("Channel", url=channel_link),
            Button.inline("Unmute Me", data=f"unmute_{user.id}"),
        ]
        await tbot.send_message(event.chat_id, capt, buttons=btns)


@hell_cmd(pattern="fsub(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        await parse_error(event, "This is meant to be used in groups only!!")
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
            return await parse_error(event, "Channel ID invalid.")
    try:
        hunter = (await event.client.get_entity(ch)).id
    except BaseException:
        return await parse_error(event, "Channel ID invalid.")
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


@hell_cmd(pattern="chfsub$")
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
    await eor(
        event,
        f"**ForceSub Enabled !!**\n\n» __Force Subscribe to__ {yy.title} ~ {usern} \n» __For Chat__ {xx.title} ~ {uname}",
    )


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


@tbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"unmute_(.*)")))
async def _(event):
    uid = int(event.data_match.group(1).decode("UTF-8"))
    fsub = is_fsub(event.chat_id)
    joinchat = fsub.channel
    if uid == event.sender_id:
        nm = (await event.client(GetFullUserRequest(uid))).users[0].first_name
        try:
            await event.client(GetParticipantRequest(int(joinchat), uid))
        except UserNotParticipantError:
            await event.answer("You need to join the channel first.", alert=True)
            return
        except Exception as e:
            return LOGS.info(str(e))
        try:
            await event.client.edit_permissions(
                event.chat.id, uid, until_date=None, send_messages=True
            )
        except Exception as e:
            return LOGS.info(str(e))
        msg = f"**Hello {nm} !! Welcome to {(await event.get_chat()).title} ✨**"
        await event.edit(msg)
    else:
        await event.answer(
            "This isn't for you!",
            cache_time=0,
            alert=True,
        )


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
    "Force Them To Join."
).add_extra(
    "📌 Note", "You need to be admin in both the chat to use this module."
).add()
