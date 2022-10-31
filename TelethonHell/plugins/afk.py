import asyncio
import datetime

from telethon.events.newmessage import NewMessage
from telethon.tl import functions, types
from TelethonHell.DB.gvar_sql import addgvar, delgvar, gvarstat
from TelethonHell.plugins import *


# afk objects for all clients
afk1 = AFK()
afk2 = AFK()
afk3 = AFK()
afk4 = AFK()
afk5 = AFK()


@bot.on(NewMessage(outgoing=True))
async def set_not_afk1(event):
    came_back = datetime.datetime.now()
    afk1.afk_end = came_back.replace(microsecond=0)
    if afk1.afk_start != {}:
        total_afk_time = str((afk1.afk_end - afk1.afk_start))
    current_message = event.message.message
    if "#" not in current_message and gvarstat("AFK") == "YES":
        hellbot = await event.client.send_message(
            event.chat_id,
            f"__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `{total_afk_time}`",
            file=afk1.afk_pic,
        )
        try:
            await unsave_gif(event, hellbot)
        except:
            pass
        delgvar("AFK")
        await event.client.send_message(
            Config.LOGGER_ID,
            f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`",
        )
        await asyncio.sleep(10)
        await hellbot.delete()
        afk1.afk_time = None


@bot.on(NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk1(event):
    cum_back = datetime.datetime.now()
    afk1.afk_end = cum_back.replace(microsecond=0)
    if afk1.afk_start != {}:
        total_afk_time = str((afk1.afk_end - afk1.afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        return False
    if gvarstat("AFK") == "YES" and not (await event.get_sender()).bot:
        msg = None
        if afk1.reason is None:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**⏰ AFK Since:**  `{total_afk_time}`"
            )
        else:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**⏰ AFK Since:**  `{total_afk_time}`\n"
                + f"\n**💬 Reason:** {afk1.reason}"
            )
        msg = await event.reply(message_to_reply, file=afk1.afk_pic)
        try:
            await unsave_gif(event, msg)
        except:
            pass
        await asyncio.sleep(2)
        if event.chat_id in afk1.last_message:
            await afk1.last_message[event.chat_id].delete()
        afk1.last_message[event.chat_id] = msg


@bot.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
async def start_afk1(event):
    krakenop = await event.get_reply_message()
    start_1 = datetime.datetime.now()
    afk1.afk_start = start_1.replace(microsecond=0)
    afk1.reason = event.text[5:] or None
    afk1.afk_pic = await event.client.download_media(krakenop) or None
    if gvarstat("AFK") != "YES":
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk1.afk_time = datetime.datetime.now()
        if afk1.reason is None:
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id, f"**I'm going afk🚶**", file=afk1.afk_pic
            )
            xy = await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",
                file=afk1.afk_pic,
            )
            try:
                await unsave_gif(event, x)
                await unsave_gif(event, xy)
            except:
                pass
        else:
            addgvar("AFK", "YES")
            x = await event.client.send_message(
                event.chat_id,
                f"**I'm going afk🚶**\n\n**Because:** `{afk1.reason}`",
                file=afk1.afk_pic,
            )
            xy = await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{afk1.reason}`",
                file=afk1.afk_pic,
            )
            try:
                await unsave_gif(event, x)
                await unsave_gif(event, xy)
            except:
                pass
    await event.delete()


if H2:
    @H2.on(NewMessage(outgoing=True))
    async def set_not_afk2(event):
        came_back = datetime.datetime.now()
        afk2.afk_end = came_back.replace(microsecond=0)
        if afk2.afk_start != {}:
            total_afk_time = str((afk1.afk_end - afk2.afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK2") == "YES":
            hellbot = await event.client.send_message(
                event.chat_id,
                f"__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `{total_afk_time}`",
                file=afk2.afk_pic,
            )
            try:
                await unsave_gif(event, hellbot)
            except:
                pass
            delgvar("AFK2")
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer:** `{total_afk_time}`",
            )
            await asyncio.sleep(10)
            await hellbot.delete()
            afk2.afk_time = None

    @H2.on(NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk2(event):
        cum_back = datetime.datetime.now()
        afk2.afk_end = cum_back.replace(microsecond=0)
        if afk2.afk_start != {}:
            total_afk_time = str((afk2.afk_end - afk2.afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK2") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if afk2.reason:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since:**  `{total_afk_time}`"
                )
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since:**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {afk2.reason}"
                )
            msg = await event.reply(message_to_reply, file=afk2.afk_pic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in afk2.last_message:
                await afk2.last_message[event.chat_id].delete()
            afk2.last_message[event.chat_id] = msg

    @H2.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def start_afk2(event):
        krakenop = await event.get_reply_message()
        start_1 = datetime.datetime.now()
        afk2.afk_start = start_1.replace(microsecond=0)
        afk2.reason = event.text[5:] or None
        afk2.afk_pic = await event.client.download_media(krakenop) or None
        if not gvarstat("AFK2"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk2.afk_time = datetime.datetime.now()
            if afk2.reason is None:
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=afk2.afk_pic
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",
                    file=afk2.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
            else:
                addgvar("AFK2", "YES")
                x = await event.client.send_message(
                    event.chat_id,
                    f"**I'm going afk🚶**\n\n**Because :** `{afk2.reason}`",
                    file=afk2.afk_pic,
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{afk2.reason}`",
                    file=afk2.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
        await event.delete()


if H3:
    @H3.on(NewMessage(outgoing=True))
    async def set_not_afk3(event):
        came_back = datetime.datetime.now()
        afk3.afk_end = came_back.replace(microsecond=0)
        if afk3.afk_start != {}:
            total_afk_time = str((afk3.afk_end - afk3.afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK3") == "YES":
            hellbot = await event.client.send_message(
                event.chat_id,
                f"__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `{total_afk_time}`",
                file=afk3.afk_pic,
            )
            await unsave_gif(event, hellbot)
            delgvar("AFK3")
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`",
            )
            await asyncio.sleep(5)
            await hellbot.delete()
            afk3.afk_time = None

    @H3.on(NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk3(event):
        cum_back = datetime.datetime.now()
        afk3.afk_end = cum_back.replace(microsecond=0)
        if afk3.afk_start != {}:
            total_afk_time = str((afk3.afk_end - afk3.afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK3") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if afk3.reason is None:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
                )
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {afk3.reason}"
                )
            msg = await event.reply(message_to_reply, file=afk3.afk_pic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in afk3.last_message:
                await afk3.last_message[event.chat_id].delete()
            afk3.last_message[event.chat_id] = msg

    @H3.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def start_afk3(event):
        krakenop = await event.get_reply_message()
        start_1 = datetime.datetime.now()
        afk3.afk_start = start_1.replace(microsecond=0)
        afk3.reason = event.text[5:] or None
        afk3.afk_pic = await event.client.download_media(krakenop) or None
        if not gvarstat("AFK3"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(
                    types.InputPrivacyKeyStatusTimestamp()
                )
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk3.afk_time = datetime.datetime.now()
            if afk3.reason is None:
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=afk3.afk_pic
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",
                    file=afk3.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
            else:
                addgvar("AFK3", "YES")
                x = await event.client.send_message(
                    event.chat_id,
                    f"**I'm going afk🚶**\n\n**Because :** `{afk3.reason}`",
                    file=afk3.afk_pic,
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{afk3.reason}`",
                    file=afk3.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
        await event.delete()


if H4:
    @H4.on(NewMessage(outgoing=True))
    async def set_not_afk4(event):
        came_back = datetime.datetime.now()
        afk4.afk_end = came_back.replace(microsecond=0)
        if afk4.afk_start != {}:
            total_afk_time = str((afk4.afk_end - afk4.afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK4") == "YES":
            hellbot = await event.client.send_message(
                event.chat_id,
                "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
                + total_afk_time
                + "`",
                file=afk4.afk_pic,
            )
            try:
                await unsave_gif(event, hellbot)
            except:
                pass
            delgvar("AFK4")
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`",
            )
            await asyncio.sleep(10)
            await hellbot.delete()
            afk4.afk_time = None

    @H4.on(NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk4(event):
        cum_back = datetime.datetime.now()
        afk4.afk_end = cum_back.replace(microsecond=0)
        if afk4.afk_start != {}:
            total_afk_time = str((afk4.afk_end - afk4.afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK4") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if afk4.reason is None:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
                )
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {afk4.reason}"
                )
            msg = await event.reply(message_to_reply, file=afk4.afk_pic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in afk4.last_message:
                await afk4.last_message[event.chat_id].delete()
            afk4.last_message[event.chat_id] = msg

    @H4.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def start_afk4(event):
        krakenop = await event.get_reply_message()
        start_1 = datetime.datetime.now()
        afk4.afk_start = start_1.replace(microsecond=0)
        afk4.reason = event.text[5:] or None
        afk4.afk_pic = await event.client.download_media(krakenop) or None
        if not gvarstat("AFK4"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk4.afk_time = datetime.datetime.now()
            if afk4.reason is None:
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=afk4.afk_pic
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",
                    file=afk4.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
            else:
                addgvar("AFK4", "YES")
                x = await event.client.send_message(
                    event.chat_id,
                    f"**I'm going afk🚶**\n\n**Because :** `{afk4.reason}`",
                    file=afk4.afk_pic,
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{afk4.reason}`",
                    file=afk4.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
        await event.delete()


if H5:
    @H5.on(events.NewMessage(outgoing=True))
    async def set_not_afk5(event):
        came_back = datetime.datetime.now()
        afk5.afk_end = came_back.replace(microsecond=0)
        if afk5.afk_start != {}:
            total_afk_time = str((afk5.afk_end - afk5.afk_start))
        current_message = event.message.message
        if "#" not in current_message and gvarstat("AFK5") == "YES":
            hellbot = await event.client.send_message(
                event.chat_id,
                f"__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `{total_afk_time}",
                file=afk5.afk_pic,
            )
            try:
                await unsave_gif(event, hellbot)
            except:
                pass
            delgvar("AFK5")
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#AFKFALSE \n\n**AFK mode** = `False`\n**AFK Timer :** `{total_afk_time}`",
            )
            await asyncio.sleep(5)
            await hellbot.delete()
            afk5.afk_time = None

    @H5.on(NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
    async def on_afk5(event):
        cum_back = datetime.datetime.now()
        afk5.afk_end = cum_back.replace(microsecond=0)
        if afk5.afk_start != {}:
            total_afk_time = str((afk5.afk_end - afk5.afk_start))
        current_message_text = event.message.message.lower()
        if "afk" in current_message_text:
            return False
        if gvarstat("AFK5") == "YES" and not (await event.get_sender()).bot:
            msg = None
            if afk5.reason is None:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`"
                )
            else:
                message_to_reply = (
                    f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
                    + f"\n**💬 Reason :** {afk5.reason}"
                )
            msg = await event.reply(message_to_reply, file=afk5.afk_pic)
            try:
                await unsave_gif(event, msg)
            except:
                pass
            await asyncio.sleep(2)
            if event.chat_id in afk5.last_message:
                await afk5.last_message[event.chat_id].delete()
            afk5.last_message[event.chat_id] = msg

    @H5.on(admin_cmd(pattern="afk(?:\s|$)([\s\S]*)"))
    async def start_afk5(event):
        krakenop = await event.get_reply_message()
        start_1 = datetime.datetime.now()
        afk5.afk_start = start_1.replace(microsecond=0)
        afk5.reason = event.text[5:] or None
        afk5.afk_pic = await event.client.download_media(krakenop) or None
        if not gvarstat("AFK5"):
            last_seen_status = await event.client(
                functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
            )
            if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
                afk5.afk_time = datetime.datetime.now()
            if afk5.reason is None:
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id, f"**I'm going afk🚶**", file=afk5.afk_pic
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `Not Mentioned`",
                    file=afk5.afk_pic,
                )
                try:
                    await unsave_gif(event, x)
                    await unsave_gif(event, xy)
                except:
                    pass
            else:
                addgvar("AFK5", "YES")
                x = await event.client.send_message(
                    event.chat_id,
                    f"**I'm going afk🚶**\n\n**Because :** `{afk5.reason}`",
                    file=afk5.afk_pic,
                )
                xy = await event.client.send_message(
                    Config.LOGGER_ID,
                    f"#AFKTRUE \n**AFK mode** = `True`\n**Reason:** `{afk5.reason}`",
                    file=afk5.afk_pic,
                )
                try:
                    await unsave_gif(event, xy)
                except:
                    pass
        await event.delete()


CmdHelp("afk").add_command(
    "afk", "<reply to media>/<reason>", "Marks you AFK with reason also shows afk time. Media also supported.", "afk <reason>`"
).add_extra(
    "📌 Exception", "Use # in a msg to stay in afk mode while chatting."
).add_info(
    "Away From Keyboard"
).add_warning(
    "✅ Harmless Module."
).add()
