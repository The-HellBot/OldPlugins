import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ManualInputRequired
from telethon import Button
from telethon.events import callbackquery

from HellConfig import Config
from TelethonHell import tbot
from .client_list import client_id

settings = "insta/settings.json" if os.path.exists("insta/settings.json") else None


async def InstaGram(event):
    if Config.IG_USERNAME and Config.IG_PASSWORD:
        cl = Client()
        try:
            if settings:
                cl.load_settings(settings)
            cl.challenge_code_handler = challenge_code_handler
            cl.login(Config.IG_USERNAME, Config.IG_PASSWORD)
        except ManualInputRequired:
            await event.edit(f"Need to configure instagram! Go to @{BOT_USERNAME}'s dm and finish the process!")
            await challenge_code_handler(event, Config.IG_USERNAME)
        except LoginRequired:
            return await InstaGram(event)
        except Exception as e:
            LOGS.info(e)
            return False
        cl.dump_settings("insta/settings.json")
        return cl
    else:
        await event.edit("Fillup `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` for functioning of IG API.")
        return
    

async def challenge_code_handler(event, username):
    ForGo10God, _, hell_mention = await client_id(event)
    async with tbot.conversation(ForGo10God, timeout=60) as conv:
        await conv.send_message(f"2-Factor Authentication is anabled in the account `{username}`.\n\nSend the OTP received on your registered Email/Phone. \n\n Send /cancel to stop verification.")
        otp = await conv.get_response()
        while not otp.text.isdigit():
            if otp.message == "/cancel":
                return await conv.send_message("EInstagram Verification Canceled!")
            await conv.send_message("Only 6 digit integer value is accepted! Try sending OTP again:")
            otp = await conv.get_response()
        return otp.text


# hellbot
