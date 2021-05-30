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
    if ".afk" not in current_message and "yes" in USER_AFK:  # pylint:disable=E0602
        hellbot = await event.client.send_message(
            event.chat_id,
            "__**Back to Virtual World!**__\nNo Longer AFK.\n⏱️ Was afk for: `"
            + total_afk_time
            + "`", file=hellpic
        )
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
                + f"Ask in {hell_grp} to get help!",
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
        if reason:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**Total AFK time :**  `{total_afk_time}`\n"
                + f"\n__Reason__ :  `{reason}`"
                )
        else:
            message_to_reply = (
                f"**I'm currently AFK!** \n\n**AFK Timer :**  `{total_afk_time}`\n"
                )
        msg = await event.reply(message_to_reply, file=hellpic)
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
    reason = event.pattern_match.group(1)
    hellpic = await event.client.download_media(krakenop)
    if not USER_AFK:  # pylint:disable=E0602
        last_seen_status = await bot(  # pylint:disable=E0602
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.datetime.now()  # pylint:disable=E0602
        USER_AFK = f"yes: {reason} {hellpic}"  # pylint:disable=E0602
        if reason:
            await bot.send_message(
                event.chat_id, f"**I'm going afk🚶** \n\nBecause  `{reason}`", file=hellpic
            )
        else:
            await bot.send_message(
                event.chat_id, f"**I am Going afk!**🚶", file=hellpic)
        await asyncio.sleep(0.001)
        await event.delete()
        try:
            if reason:
                await bot.send_message(
                  Config.LOGGER_ID,
                  f"#AFKTRUE \nAFK mode = **True**\nReason  `{reason}`",file=hellpic
                 )
            else:
                await bot.send_message(
                  Config.LOGGER_ID,
                  f"#AFKTRUE \nAFK mode = **True**",file=hellpic
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            logger.warn(str(e))  # pylint:disable=E06

CmdHelp("afk").add_command(
  'afk', '<reply to media>/<reason>', 'Marks you AFK with reason also shows afk time. Media also supported.'
).add_info(
  "Away From Keyboard"
).add_warning(
  "✅ Harmless Module."
).add()
