import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient

from hellbot import LOGS, bot
from hellbot.config import Config
from hellbot.utils import load_module

HELL_PIC = Config.ALIVE_PIC or "https://telegra.ph/  " #soon

# let's get the bot ready
async def hell_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


# hellbot starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("🔰 Starting HellBot 🔰")
            bot.loop.run_until_complete(hell_bot(Config.BOT_USERNAME))
            LOGS.info("🔥 HellBot Startup Completed 🔥")
        else:
            bot.start()
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
LOGS.info("⚡ Your HellBot Is Now Working ⚡")
LOGS.info(
    "Head to @The_HellBot for Updates. Also join chat group to get help regarding to HellBot."
)

# that's life...
async def hell_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                HELL_PIC,
                caption="Deployed Hêllẞø† Successfully\n\nType `.ping` or `.alive` to check! \n\nJoin [Hêllẞø† Channel](t.me/The_HellBot) for Updates & [Hêllẞø† Chat](t.me/its_fuckin_hell) for any query regarding Hêllẞø†",
            )
    except Exception as e:
        LOGS.info(str(e))


bot.loop.create_task(hell_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# hellbot
