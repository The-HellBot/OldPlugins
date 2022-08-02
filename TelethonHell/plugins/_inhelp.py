import html
import random
from math import ceil
from re import compile

from telethon import Button, custom, functions
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.tl.functions.users import GetFullUserRequest

from TelethonHell.DB.gvar_sql import gvarstat

from . import *

hell_row = Config.BUTTONS_IN_HELP
hell_emoji = Config.EMOJI_IN_HELP

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"

LOG_GP = Config.LOGGER_ID

alive_txt = """{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>Hêllẞø† ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""


def button(page, modules):
    Row = hell_row

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(
                    f"{hell_emoji} " + pair + f" {hell_emoji}",
                    data=f"Information[{page}]({pair})",
                )
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
                f"◀️ Back {hell_emoji}",
                data=f"page({(max_pages - 1) if page == 0 else (page - 1)})",
            ),
            custom.Button.inline(f"• ❌ •", data="close"),
            custom.Button.inline(
                f"{hell_emoji} Next ▶️",
                data=f"page({0 if page == (max_pages - 1) else page + 1})",
            ),
        ]
    )
    return [max_pages, buttons]

    modules = CMD_HELP


if Config.BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(InlineQuery)
    async def inline_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        builder = event.builder
        result = None
        query = event.text
        auth = await clients_list()
        if event.query.user_id in auth and query == "hellbot_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = "https://telegra.ph/file/3a48c5756d2a9763eafaf.jpg"
            help_msg = f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}"
            if help_pic == "DISABLE":
                result = builder.article(
                    f"Hey! Only use {hl}help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="HellBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id in auth and query == "alive":
            uptime = await get_time((time.time() - StartTime))
            alive_msg = gvarstat("ALIVE_MSG") or "»»» <b>нєℓℓвσт ιѕ σиℓιиє</b> «««"
            alive_name = gvarstat("ALIVE_NAME") or HELL_USER
            he_ll = alive_txt.format(
                alive_msg, tel_ver, hell_ver, uptime, abuse_m, is_sudo
            )
            alv_btn = [
                [Button.url(f"{alive_name}", f"tg://openmessage?user_id={ForGo10God}")],
                [
                    Button.url("My Channel", f"https://t.me/{my_channel}"),
                    Button.url("My Group", f"https://t.me/{my_group}"),
                ],
            ]
            a = gvarstat("ALIVE_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            elif PIC:
                result = builder.document(
                    PIC,
                    text=he_ll,
                    title="HellBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="HellBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )

        elif event.query.user_id in auth and query == "pm_warn":
            CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or None
            HELL_FIRST = f"🔥 𝙃𝙚𝙡𝙡𝘽𝙤𝙩 𝙋𝙈 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 🔥\n\nHello!! This is an automated message on behalf of {hell_mention}."
            if CSTM_PMP:
                HELL_FIRST += f"\n\n{CSTM_PMP}"
            a = gvarstat("PMPERMIT_PIC")
            pic_list = []
            if a and a == "DISABLE":
                PIC = None
            elif a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/58df4d86400922aa32acd.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    file=PIC,
                    text=HELL_FIRST,
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            elif PIC:
                result = builder.document(
                    file=PIC,
                    text=HELL_FIRST,
                    title="Hellbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=HELL_FIRST,
                    title="Hellbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )

        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚡ ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt ⚡**",
                buttons=[
                    [Button.url("📑 Repo 📑", "https://github.com/The-HellBot/HellBot")],
                    [Button.url("HellBot Network", "https://t.me/hellbot_network")],
                ],
            )

        else:
            result = builder.article(
                "@Its_HellBot",
                text="""**Hey! This is [Hêllẞø†](https://t.me/its_hellbot) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 CHANNEL 🔥", "https://t.me/Its_HellBot"),
                        custom.Button.url("⚡ GROUP ⚡", "https://t.me/hellbot_chat"),
                    ],
                    [
                        custom.Button.url(
                            "✨ REPO ✨", "https://github.com/The-HellBot/HellBot"
                        ),
                        custom.Button.url(
                            "🔰 TUTORIAL 🔰", "https://youtu.be/M2FQJq_sHp4"
                        ),
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for Other Users..."
        else:
            reply_pop_up_alert = "🔰 This is Hêllẞø† PM Security to keep away unwanted retards from spamming PM !!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                "✅ **Request Registered** \n\nMy master will now decide to look for your request or not.\n😐 Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(
                LOG_GP,
                f"#PM_REQUEST \n\n⚜️ You got a PM request from [{first_name}](tg://user?id={event.query.user_id}) !",
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(f"As you wish. **BLOCKED !!**")
            if H1:
                await H1(functions.contacts.BlockRequest(event.query.user_id))
            if H2:
                await H2(functions.contacts.BlockRequest(event.query.user_id))
            if H3:
                await H3(functions.contacts.BlockRequest(event.query.user_id))
            if H4:
                await H4(functions.contacts.BlockRequest(event.query.user_id))
            if H5:
                await H5(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(
                LOG_GP,
                f"#BLOCK \n\n**Blocked** [{first_name}](tg://user?id={event.query.user_id}) \nReason:- PM Self Block",
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            current_page_number = 0
            simp = button(current_page_number, CMD_HELP)
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = "https://telegra.ph/file/3a48c5756d2a9763eafaf.jpg"

            if help_pic == "DISABLE":
                await event.edit(
                    text=f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                    file=None,
                )
            else:
                await event.edit(
                    text=f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                    file=help_pic,
                )
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© Hêllẞø† ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            veriler = custom.Button.inline(
                f"{hell_emoji} Re-Open Menu {hell_emoji}", data="reopen"
            )
            await event.edit(
                f"**⚜️ Hêllẞø† Mêñû Prõvîdêr ìs ñôw Çlösëd ⚜️**\n\n**Bot Of :**  {hell_mention}\n\n        [©️ Hêllẞø† ™️]({chnl_link})",
                buttons=veriler,
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© Hêllẞø† ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"send\((.+?)\)")))
    async def send(event):
        plugin = event.data_match.group(1).decode("UTF-8")
        ForGo10God, HELL_USER, hell_mention = await client_id(event, event.query.user_id)
        thumb = hell_logo
        omk = f"**• Plugin name ≈** `{plugin}`\n**• Uploaded by ≈** {hell_mention}\n\n⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt]({chnl_link})** ⚡"
        the_plugin_file = "./TelethonHell/plugins/{}.py".format(plugin.lower())
        butt = custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data="reopen")
        if os.path.exists(the_plugin_file):
            await event.edit(
                file=the_plugin_file,
                thumb=thumb,
                text=omk,
                buttons=butt,
            )
        else:
            await event.answer("Unable to access file!", cache_time=0, alert=True)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id in auth:
            await event.edit(
                f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}`\n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© Hêllẞø† ™",
                cache_time=0,
                alert=True,
            )

    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "⚡ " + cmd[0] + " ⚡", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"📎 Send Plugin 📎", data=f"send({commands})")])
        buttons.append([custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**📗 File :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© Hêllẞø† ™",
                cache_time=0,
                alert=True,
            )

    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
        sextraa = CMD_HELP_BOT[cmd]["extra"]
        if sextraa:
            a = sorted(sextraa.keys())
            for b in a:
                c = b
                d = sextraa[c]["content"]
                result += f"**{c} :**  `{d}`\n"
        result += "\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 Explanation :**  `{command['usage']}`\n"
            result += f"**⌨️ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(
                        f"{hell_emoji} Return {hell_emoji}",
                        data=f"Information[{page}]({cmd})",
                    )
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© Hêllẞø† ™",
                cache_time=0,
                alert=True,
            )


# hellbot
