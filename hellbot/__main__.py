import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from hellbot import LOGS, bot, tbot
from hellbot.clients.session import Hell, H2, H3, H4, H5
from hellbot.config import Config
from hellbot.utils import load_module
from hellbot.version import __hell__ as hellver
hl = Config.HANDLER
HELL_PIC = "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"

# let's get the bot ready
async def h1(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"HELLBOT_SESSION - {str(e)}")
        sys.exit()


# Multi-Client helper
async def hell_client(client):
    client.me = await client.get_me()
    client.uid = telethon.utils.get_peer_id(client.me)


# Multi-Client Starter
def hells():
    failed = 0
    if Config.SESSION_2:
        LOGS.info("SESSION_2 detected! Starting 2nd Client.")
        try:
            H2.start()
            H2.loop.run_until_complete(hell_client(H2))
        except:
            LOGS.info("SESSION_2 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_3:
        LOGS.info("SESSION_3 detected! Starting 3rd Client.")
        try:
            H3.start()
            H3.loop.run_until_complete(hell_client(H3))
        except:
            LOGS.info("SESSION_3 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_4:
        LOGS.info("SESSION_4 detected! Starting 4th Client.")
        try:
            H4.start()
            H4.loop.run_until_complete(hell_client(H4))
        except:
            LOGS.info("SESSION_4 failed. Please Check Your String session.")
            failed += 1

    if Config.SESSION_5:
        LOGS.info("SESSION_5 detected! Starting 5th Client.")
        try:
            H5.start()
            H5.loop.run_until_complete(hell_client(H5))
        except:
            LOGS.info("SESSION_5 failed. Please Check Your String session.")
            failed += 1

    if not Config.SESSION_2:
        failed += 1
    if not Config.SESSION_3:
        failed += 1
    if not Config.SESSION_4:
        failed += 1
    if not Config.SESSION_5:
        failed += 1
    return failed


# hellbot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = tbot
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("🔰 Starting HellBot 🔰")
            bot.loop.run_until_complete(h1(Config.BOT_USERNAME))
            failed_client = hells()
            global total
            total = 5 - failed_client
            LOGS.info("🔥 HellBot Startup Completed 🔥")
            LOGS.info(f"» Total Clients = {total} «")
        else:
            bot.start()
            failed_client = hells()
            total = 5 - failed_client
            LOGS.info(f"» Total Clients = {total} «")
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()


# imports plugins...
path = "hellbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))


# let the party begin...
LOGS.info("Starting Bot Mode !")
tbot.start()
LOGS.info("⚡ Your HellBot Is Now Working ⚡")
LOGS.info("Head to @Its_HellBot for Updates. Also join chat group to get help regarding to HellBot.")
LOGS.info(f"» Total Clients = {total} «")

# that's life...
async def hell_is_on():
    try:
        x = await bot.get_me()
        xid = telethon.utils.get_peer_id(x)
        send_to = Config.LOGGER_ID if Config.LOGGER_ID != 0 else xid
        await bot.send_file(
            send_to,
            HELL_PIC,
            caption=f"#START \n\n<b><i>Version :</b></i> <code>{hellver}</code> \n<b><i>Clients :</b></i> <code>{total}</code> \n\n<b><i>»» <u><a href='https://t.me/Its_HellBot'>†hê Hêllẞø†</a></u> ««</i></b>",
            parse_mode="HTML",
        )
    except Exception as e:
        LOGS.info(str(e))

# Join HellBot Channel after deploying 🤐😅
    try:
        await bot(JoinChannelRequest("@Its_HellBot"))
    except BaseException:
        pass

# Why not come here and chat??
    try:
        await bot(JoinChannelRequest("@HellBot_Chat"))
    except BaseException:
        pass


bot.loop.create_task(hell_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# hellbot
