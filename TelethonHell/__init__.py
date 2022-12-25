import time

import heroku3
from HellConfig import Config

from TelethonHell.clients.logger import LOGGER as LOGS

StartTime = time.time()


if not Config.API_HASH:
    LOGS.warning("Please fill var API_HASH to continue.")
    quit(1)

if not Config.APP_ID:
    LOGS.warning("Please fill var APP_ID to continue.")
    quit(1)

if not Config.BOT_TOKEN:
    LOGS.warning("Please fill var BOT_TOKEN to continue.")
    quit(1)

if not Config.DATABASE_URL:
    LOGS.warning("Please fill var DATABASE_URL to continue.")
    quit(1)

if not Config.HELLBOT_SESSION:
    LOGS.warning("Please fill var HELLBOT_SESSION to continue.")
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


# hellbot
