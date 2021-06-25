from telethon.events import InlineQuery, callbackquery
from telethon.tl.custom import Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from hellbot.sql.fsub_sql import *
from . import *
"""
@tgbot.on(InlineQuery)
async def fsub_in(event):
        builder = event.builder
        query = event.text
        if event.query.user_id == bot.uid and query == "fsub":
            hunter = event.pattern_match.group(1)
            hell = hunter.split("+")
            user = await bot.get_entity(int(hell[0]))
            channel = await bot.get_entity(int(hell[1]))
            msg = f"**👋 Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**📍 You need to Join** {channel.title} **to chat in this group.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            sub = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [Button.url(text="🔓 Unmute Me", data=unmute)],
                    ],
                )
            ]
            await event.answer(sub)


@tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
async def on_pm_click(event):
    hunter = (event.data_match.group(1)).decode("UTF-8")
    hell = hunter.split("+")
    if not event.sender_id == int(hell[0]):
        return await event.answer("This Ain't For You!!", alert=True)
    try:
        await bot(GetParticipantRequest(int(hell[1]), int(hell[0])))
    except UserNotParticipantError:
        return await event.answer(
            "You need to join the channel first.", alert=True
        )
    await bot.edit_permissions(
        event.chat_id, int(hell[0]), send_message=True, until_date=None
    )
    await event.edit("Yay! You can chat now !!")
"""


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
    joinchat = is_fsub(event.chat_id)
    tgbotusername = Config.BOT_USERNAME
    try:
        await bot(GetParticipantRequest(int(joinchat), user.id))
    except UserNotParticipantError:
        await bot.edit_permissions(event.chat_id, user.id, send_messages=False)
        res = await bot.inline_query(
            tgbotusername, f"fsub {user.id}+{joinchat}"
        )
        await res[0].click(event.chat_id, reply_to=event.action_message.id)


@bot.on(hell_cmd(pattern="fsub ?(.*)"))
@bot.on(sudo_cmd(pattern="fsub ?(.*)", allow_sudo=True))
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
        hunter = (await bot.get_entity(ch)).id
    except BaseException:
        return await eod(event, "⚠️ **Error !** \n\nChannel ID invalid. Please Recheck It !")
    if not str(hunter).startswith("-100"):
        hunter = int("-100" + str(hunter))
    add_fsub(event.chat_id, hunter)
    await eor(event, "Implementing **Force Subscribe** In This Channel !!")


@bot.on(hell_cmd(pattern="rmfsub"))
@bot.on(sudo_cmd(pattern="rmfsub", allow_sudo=True))
async def removef(event):
    hel_ = rem_fsub(event.chat_id)
    if not hel_:
        return await eod(event, "I don't think force sub was activated here.")
    await eor(e, "Deactivated **Force Subscribe** In This Channel !!")


@bot.on(hell_cmd(pattern="chfsub"))
@bot.on(sudo_cmd(pattern="chfsub", allow_sudo=True))
async def getfsub(event):
    all_chat = is_fsub(event.chat_id)
    if not all_chat:
        return await eod(event, "Force Subscribe Is Disabled Here..")
    channel = await bot.get_entity(int(all))
    await eor(event, f"**ForceSub Enabled ** :\n- {channel.title} `({all})`")


@bot.on(hell_cmd(pattern="lsfsub$"))
@bot.on(sudo_cmd(pattern="lsfsub$", allow_sudo=True))
async def list(event):
    channels = all_fsub()
    CHANNEL_LIST = "**🚀 Fsub Enabled In :**\n"
    if len(channels) > 0:
        for hunter in channels:
            CHANNEL_LIST += f"[{hunter.title}](https://t.me/ + {hunter.username})\n"
    else:
        CHANNEL_LIST = "No Chat Found With Active Force Subscribe."
    await edit_or_reply(event, CHANNEL_LIST)

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
