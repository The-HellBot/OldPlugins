from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotInlineDisabledError as noinline
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot
from telethon.errors.rpcerrorlist import YouBlockedUserError
from TelethonHell.plugins import *


msg = f"""
**⚡ ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt ⚡**
  •        [📑 Repo 📑](https://github.com/The-HellBot/HellBot)
  •        [HellBot Network](https://t.me/hellbot_networks)
  •  ©️ {hell_channel} ™
"""


@hell_cmd(pattern="repo$")
async def repo(event):
    ForGo10God, _, _ = await client_id(event)
    try:
        hell = await event.client.inline_query(Config.BOT_USERNAME, "repo")
        await hell[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


@hell_cmd(pattern="help$")
async def _(event):
    if Config.BOT_USERNAME:
        try:
            results = await event.client.inline_query(
                Config.BOT_USERNAME,
                "hellbot_help",
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
            )
            await event.delete()
        except noinline:
            hell = await eor(event, "**Inline Mode is disabled.** \n__Turning it on, please wait for a minute...__")
            async with bot.conversation("@BotFather") as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(Config.BOT_USERNAME)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await parse_error(hell, "__Unblock__ @Botfather __first.__", False)
                await eod(hell, f"**Turned On Inline Mode Successfully.** \n\nDo `{hl}help` again to get the help menu.")
            await bot.delete_messages(
                conv.chat_id,
                [
                    first.id,
                    second.id,
                    third.id,
                    fourth.id,
                    fifth.id,
                    sixth.id,
                ],
            )
    else:
        await parse_error(event, "__Please recheck__ `BOT_TOKEN` __on Heroku.__", False)


@hell_cmd(pattern="plinfo(?:\s|$)([\s\S]*)")
async def hellbott(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await eor(event, str(CMD_HELP[args]))
        else:
            await parse_error(event, "Need a module name to show plugin info.")
    else:
        string = ""
        sayfa = [
            sorted(list(CMD_HELP))[i : i + 5]
            for i in range(0, len(sorted(list(CMD_HELP))), 5)
        ]

        for i in sayfa:
            string += f"`📌 `"
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await eor(event, "Please Specify A Module Name Of Which You Want Info" + "\n\n" + string)


@hell_cmd(pattern="cmdinfo(?:\s|$)([\s\S]*)")
async def cmdinfo(event):
    cmd = str(event.text[9:]).lower()
    try:
        info = CMD_INFO[cmd]["info"]
        file = CMD_INFO[cmd]["plugin"]
        exam = CMD_INFO[cmd]["example"]
    except KeyError:
        return await parse_error(event, f"__• No command named:__ `{cmd}`", False)
    await eor(event, f"**• File:** \n» __{file}__ \n\n**• {cmd}:** \n» __{info}__ \n\n**• Example:** \n» `{str(exam)}`")

