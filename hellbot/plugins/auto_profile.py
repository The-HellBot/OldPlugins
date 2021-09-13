import asyncio
import time

from telethon.errors import FloodWaitError
from telethon.tl import functions
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

from . import *

DEFAULTUSERBIO = Config.BIO_MSG
DEL_TIME_OUT = 60


@hell_cmd(pattern="autoname")
async def _(event):
    hell = await eor(event, "`Starting AutoName Please Wait`")
    while True:
        HB = time.strftime("%d-%m-%y")
        HE = time.strftime("%H:%M")
        name = f"🕒{HE} ⚡{HELL_USER}⚡ 📅{HB}"
        logger.info(name)
        try:
            await event.client(
                functions.account.UpdateProfileRequest(
                    first_name=name
                )
            )
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)
        await hell.edit(f"Auto Name has been started my Master")
        await event.client.send_message(Config.LOGGER_ID, "#AUTONAME \n\nAutoname Started!!")


@hell_cmd(pattern="autobio")
async def _(event):
    hell = await eor(event, "Starting AutoBio...")
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await event.client(
                functions.account.UpdateProfileRequest(
                    about=bio
                )
            )
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)
        await hell.edit("AutoBio Activated...")
        await event.client.send_message(Config.LOGGER_ID, "#AUTOBIO \n\nAutoBio Started!!")


@hell_cmd(pattern="reserved")
async def mine(event):
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await eor(event, output_str)


CmdHelp("auto_profile").add_command(
  'autobio', None, 'Changes your bio with time. Need to set BIO_MSG in heroku vars(optional)'
).add_command(
  'autoname', None, 'Changes your name with time according to your ALIVE_NAME in heroku var'
).add_command(
  'reserved', None, 'Gives the list of usernames reserved by you. In short gives the list of public groups or channels that you are owner in.'
).add_info(
  "Manage Profiles"
).add_warning(
  "🚫 Potentially Harmful"
).add()
