import os
import sys
import time
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger

import heroku3
from dotenv import load_dotenv
from requests import get
from telethon import TelegramClient
from telethon.sessions import StringSession

from d3vilbot.config import Config

StartTime = time.time()

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


if Config.D3VILBOT_SESSION:
    session_name = str(Config.D3VILBOT_SESSION)
    try:
        if session_name.endswith("="):
            bot = TelegramClient(
                StringSession(session_name), Config.APP_ID, Config.API_HASH
            )
        else:
            bot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.D3VILBOT_SESSION)
    except Exception as e:
        LOGS.warn(f"D3VILBOT_SESSION - {str(e)}")
        sys.exit()
else:
    session_name = "startup"
    bot = TelegramClient(session_name, Config.APP_ID, Config.API_HASH)

tbot = TelegramClient('d3vilbot', api_id=Config.APP_ID, api_hash=Config.API_HASH).start(bot_token=Config.BOT_TOKEN)


# global variables
CMD_LIST = {}
CMD_HELP = {}
CMD_HELP_BOT = {}
BRAIN_CHECKER = []
INT_PLUG = ""
LOAD_PLUG = {}
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ISAFK = False
AFKREASON = None
SUDO_LIST = {}



