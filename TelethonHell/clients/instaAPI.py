import os

from instagrapi import Client, exceptions

from HellConfig import Config


InstaGram = Client()
settings = "settings.json" if os.path.exists("insta/settings.json") else None


if settings:
    InstaGram.load_settings(settings)
    InstaGram.login(Config.IG_USERNAME, Config.IG_PASSWORD)
else:
    InstaGram.login(Config.IG_USERNAME, Config.IG_PASSWORD)
    InstaGram.dump_settings("insta/settings.json")


class LoginError(Exception):
    pass

# hellbot
