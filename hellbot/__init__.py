import heroku3
import os
import sys
import time

from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger

from hellbot.clients.session import H2, H3, H4, H5, Hell, HellBot 
from hellbot.config import Config


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

bot = Hell
tbot = HellBot


if not Config.API_HASH:
    LOGS.warning("Please fill var API HASH to continue.")
    quit(1)


if not Config.APP_ID:
    LOGS.warning("Please fill var APP ID to continue.")
    quit(1)


if not Config.BOT_TOKEN:
    LOGS.warning("Please fill var BOT TOKEN to continue.")
    quit(1)


if not Config.BOT_USERNAME:
    LOGS.warning("Please fill var BOT USERNAME to continue.")
    quit(1)


if not Config.DB_URI:    
    LOGS.warning("Please fill var DATABASE URL to continue.")
    quit(1)


if not Config.HELLBOT_SESSION:
    LOGS.warning("Please fill var HELLBOT SESSION to continue.")
    quit(1)


if not Config.LOGGER_ID:
    LOGS.warning("Please fill var LOGGER ID to continue.")
    quit(1)


try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


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


# hellbot
