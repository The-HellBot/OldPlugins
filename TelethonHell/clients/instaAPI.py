import asyncio
import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

from HellConfig import Config
from TelethonHell import bot, tbot, LOGS
from .client_list import client_id

settings = "insta/settings.json" if os.path.exists("insta/settings.json") else {}


async def InstaGram(event):
    if Config.IG_USERNAME and Config.IG_PASSWORD:
        cl = Client(settings)
        cl.challenge_code_handler = await challenge_code()
        try:
            cl.login(Config.IG_USERNAME, Config.IG_PASSWORD)
        # except ChallengeRequired:
            # await event.edit(f"Need to configure instagram! Go to @{Config.BOT_USERNAME}'s dm and finish the process!")
            # cl.challenge_code_handler = challenge_code_handler
        except LoginRequired:
            return await InstaGram(event)
        # except Exception as e:
            # LOGS.info(e)
            # return False
        cl.dump_settings("insta/settings.json")
        return cl
    else:
        await event.edit("Fillup `INSTAGRAM_USERNAME` and `INSTAGRAM_PASSWORD` for functioning of IG API.")
        return


async def challenge_code():
    _id = (await bot.get_me()).id
    async with tbot.conversation(_id, timeout=60*2) as conv:
        await conv.send_message(f"2-Factor Authentication is enabled in the account `{Config.IG_USERNAME}`.\n\nSend the OTP received on your registered Email/Phone. \n\n Send /cancel to stop verification.")
        otp = await conv.get_response()
        while not otp.text.isdigit():
            if otp.message == "/cancel":
                return await conv.send_message("Instagram Verification Canceled!")
            await conv.send_message("Only 6 digit integer value is accepted! Try sending OTP again:")
            otp = conv.get_response()
        return otp.text


# hellbot
