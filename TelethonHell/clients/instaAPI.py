import os

from HellConfig import Config
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from TelethonHell.clients.logger import LOGGER as LOGS

settings = "insta/settings.json" if os.path.exists("insta/settings.json") else {}


async def InstaGram(event):
    if Config.IG_SESSION:
        settings_path = os.path.join("insta", "settings.json")
        if not os.path.exists("insta"):
            os.makedirs("insta")

        cl = Client(settings)
        try:
            cl.login_by_sessionid(Config.IG_SESSION)
        except LoginRequired:
            return await InstaGram(event)
        except Exception as e:
            LOGS.info(f"ERROR: {e}")
            return None
        cl.dump_settings("insta/settings.json")
        return cl
    else:
        return None


# hellbot
