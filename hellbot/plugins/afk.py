import asyncio
import datetime

from telethon import events
from telethon.tl import functions, types

from . import *

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global last_afk_message  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
last_afk_message = {}
afk_start = {}

@bot.on(events.NewMessage(outgoing=True))  # pylint:disable=E0602
async def set_not_afk(event):
    if event.fwd_from:
        return
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    came_back = datetime.datetime.now()
    afk_end = came_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "#" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
        hellbot = await event.client.send_message(
            event.chat_id,
            "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
            + total_afk_time
            + "`", file=hellpic
        )
        try:
            await unsave_gif(event, hellbot)
        except:
            pass
        try:
            await event.client.send_message(  # pylint:disable=E0602
                Config.LOGGER_ID,  # pylint:disable=E0602
                "#AFKFALSE \n\nAFK mode = **False**\n"
                + "__**Back to Virtual World!**__\nNo Longer afk.\n⏱️ Was afk for: "
                + total_afk_time
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await bot.send_message(  # pylint:disable=E0602
                event.chat_id,
                "Please set `LOGGER_ID` "
                + "for the proper functioning of afk."
                + f" Ask in {hell_grp} to get help!",
                reply_to=event.message.id,
                link_preview=False,
                silent=True,
            )
        await asyncio.sleep(5)
        await hellbot.delete()
        USER_AFK = {}  # pylint:disable=E0602
        afk_time = None  # pylint:disable=E0602


@bot.on(
    events.NewMessage(  # pylint:disable=E0602
        incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
    )
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    cum_back = datetime.datetime.now()
    afk_end = cum_back.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_AFK and not (await event.get_sender()).bot:
        msg = None
        message_to_reply = (
            f"**I'm currently AFK!** \n\n**⏰ AFK Since :**  `{total_afk_time}`\n"
            + f"\n**💬 Reason :** {reason}"
            )
        msg = await event.reply(message_to_reply, file=hellpic)
        try:
            await unsave_gif(event, msg)
        except:
            pass
        await asyncio.sleep(2)
        if event.chat_id in last_afk_message:  # pylint:disable=E0602
            await last_afk_message[event.chat_id].delete()  # pylint:disable=E0602
        last_afk_message[event.chat_id] = msg  # pylint:disable=E0602


@bot.on(hell_cmd(pattern=r"afk (.*)", outgoing=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    krakenop = await event.get_reply_message()
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global last_afk_message  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    global hellpic
    USER_AFK = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.datetime.now()
    afk_start = start_1.replace(microsecond=0)
    owo = event.text[5:]
    if owo == "":
        reason = "Not Mentioned."
    else:
        reason = owo
    hellpic = await event.client.download_media(krakenop)
    if not USER_AFK:  # pylint:disable=E0602
        last_seen_status = await bot(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()  # pylint:disable=E0602
        USER_AFK = f"yes: {reason} {hellpic}"  # pylint:disable=E0602
        x = await bot.send_message(
            event.chat_id, f"**I'm going afk🚶** \n\n**Because :** {reason}", file=hellpic
        )
        try:
            await unsave_gif(event, x)
        except:
            pass
        await asyncio.sleep(0.001)
        await event.delete()
        try:
            xy = await bot.send_message(
                Config.LOGGER_ID,
                f"#AFKTRUE \nAFK mode = **True**\nReason  `{reason}`",file=hellpic
                )
            try:
                await unsave_gif(event, xy)
            except:
                pass
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E06

CmdHelp("afk").add_command(
  'afk', '<reply to media>/<reason>', 'Marks you AFK with reason also shows afk time. Media also supported.\nUse # in message to chat without breaking AFK mode.', "afk <reason>`\n📍 **Exception :** `Use # in a msg to stay in afk mode while chatting."
).add_info(
  "Away From Keyboard"
).add_warning(
  "✅ Harmless Module."
).add()


global USER_night
global night_time 
global last_night_message
USER_night = {}
night_time = None
last_night_message = {}


@bot.on(events.NewMessage(outgoing=True))
async def set_not_night(event):
    global USER_night 
    global night_time 
    global last_night_message
    current_message = event.message.message
    if ".night" not in current_message and "yes" in USER_night:
        try:
            await bot.send_message(
                Config.LOGGER_ID,
                f"#NIGHT \n\nNight Mode :  **TRUE**",
            )
        except Exception as e:
            await bot.send_message(
                event.chat_id,
                "Please set `LOGGER_ID` "
                + "for the proper functioning of night functionality "
                + "report in {}\n\n `{}`".format(hell_grp, str(e)),
                reply_to=event.message.id,
                silent=True,
            )
        USER_night = {}
        night_time = None


@bot.on(hell_cmd(pattern=r"night ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    global USER_night
    global night_time
    global last_night_message
    global reason
    USER_night = {}
    night_time = None
    last_night_message = {}
    reason = event.pattern_match.group(1)
    if not USER_night:
        last_seen_status = await bot(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            night_time = datetime.datetime.now()
        USER_night = f"yes: {reason}"
        if reason:
            await event.edit(f"**Bye Fellas!!** \n\nTime to sleep 😴")
        else:
            await event.edit(f"**Bye Fellas!!** \n\nTime to sleep 😴")
        await asyncio.sleep(5)
        await event.delete()
        try:
            await bot.send_message(
                Config.LOGGER_ID, f"Time to sleep 😴"
            )
        except Exception as e:
            logger.warn(str(e))


@bot.on(
    events.NewMessage(
        incoming=True, func=lambda e: bool(e.mentioned or e.is_private)
    )
)
async def on_night(event):
    if event.fwd_from:
        return
    global USER_night
    global night_time
    global last_night_message
    night_since = "**a while ago**"
    current_message_text = event.message.message.lower()
    if "night" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USER_night and not (await event.get_sender()).bot:
        if night_time:
            now = datetime.datetime.now()
            datime_since_night = now - night_time
            time = float(datime_since_night.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                night_since = "**Yesterday**"
            elif days > 1:
                if days > 6:
                    date = now + datetime.timedelta(
                        days=-days, hours=-hours, minutes=-minutes
                    )
                    night_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    night_since = wday.strftime("%A")
            elif hours > 1:
                night_since = f"`{int(hours)}h{int(minutes)}m` **ago**"
            elif minutes > 0:
                night_since = f"`{int(minutes)}m{int(seconds)}s` **ago**"
            else:
                night_since = f"`{int(seconds)}s` **ago**"
        msg = None
        message_to_reply = (
            f"My Master Has Been Gone For {night_since}\nWhere He Is: **On Bed Sleeping** "
            if reason
            else f"I'm sleeping right now!!"
        )
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(5)
        if event.chat_id in last_night_message:
            await last_night_message[event.chat_id].delete()
        last_night_message[event.chat_id] = msg

CmdHelp("night").add_command(
  "night", None, "Same like AFK. But fixed reason and for sleeping purpose only. Sed ;_;"
).add_info(
  "Good Night 🌃"
).add_warning(
  "✅ Harmless Module."
).add()
