import asyncio
import json
import os

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

from HellConfig import Config
from TelethonHell import bot, tbot, LOGS
from .client_list import client_id

settings = "insta/settings.json" if os.path.exists("insta/settings.json") else None


class INSTAGRAM:
	def __init__(self):
		self.username = Config.IG_USERNAME
		self.password = Config.IG_PASSWORD

		if settings:
			self.session = json.load(open("insta/settings.json", "r"))
			LOGS.info("Instagram Account Setting Loaded !!")
		else:
			self.session = {}

		self.client = Client(settings=self.session)
		self.client.challenge_code_handler = self.CodeChallenge
		self.client.login(self.username, self.password)

		with open('insta/settings.json', 'w') as f:
			json.dump(self.client.get_settings(), f)

		self.session = json.load(open("insta/settings.json", "r"))
		LOGS.info("Logged in to Instagram Account")

	async def CodeChallenge(self, username, choice):
		LOGS.info("Starting OTP verification !!")
		_id = (await bot.get_me()).id
        async with tbot.conversation(_id, timeout=60*2) as conv:
            await conv.send_message(f"2-Factor Authentication is anabled in the account `{Config.IG_USERNAME}`.\n\nSend the OTP received on your registered Email/Phone. \n\n Send /cancel to stop verification.")
            otp = await conv.get_response()
            while not otp.text.isdigit():
                if otp.message == "/cancel":
                    return await conv.send_message("Instagram Verification Canceled!")
                await conv.send_message("Only 6 digit integer value is accepted! Try sending OTP again:")
                otp = await conv.get_response()
		    return otp


InstaGram = INSTAGRAM()

# hellbot
