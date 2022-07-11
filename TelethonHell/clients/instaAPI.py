import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired

from HellConfig import Config
from TelethonHell import LOGS

settings = "insta/settings.json" if os.path.exists("insta/settings.json") else {}


async def InstaGram(event):
    if Config.IG_SESSION:
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
