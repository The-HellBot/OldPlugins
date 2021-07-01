import asyncio
import time

from telethon.errors import FloodWaitError
from telethon.tl import functions
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest

from . import *

DEFAULTUSERBIO = Config.BIO_MSG
DEL_TIME_OUT = 60


@bot.on(hell_cmd(pattern="autoname"))
async def _(event):
    if event.fwd_from:
        return
    hell = await edit_or_reply(event, "`Starting AutoName Please Wait`")
    if event.fwd_from:
        return
    while True:
        HB = time.strftime("%d-%m-%y")
        HE = time.strftime("%H:%M")
        name = f"🕒{HE} ⚡{HELL_USER}⚡ 📅{HB}"
        logger.info(name)
        try:
            await bot(
                functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    first_name=name
                )
            )
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)
        await hell.edit(f"Auto Name has been started my Master")
        await bot.send_message(Config.LOGGER_ID, "#AUTONAME \n\nAutoname Started!!")


@bot.on(hell_cmd(pattern="autobio"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting AutoBio...")
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await bot(
                functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=bio
                )
            )
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
        # logger.info(r.stringify())
        # await bot.send_message(  # pylint:disable=E0602
        # Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
        # "Successfully Changed Profile Bio"
        # )
        await asyncio.sleep(DEL_TIME_OUT)
        await event.edit("AutoBio Activated...")
        await bot.send_message(Config.LOGGER_ID, "#AUTOBIO \n\nAutoBio Started!!")


@bot.on(hell_cmd(pattern="reserved", outgoing=True))
@bot.on(sudo_cmd(pattern="reserved", allow_sudo=True))
async def mine(event):
    if event.fwd_from:
        return
    """ For .reserved command, get a list of your reserved usernames. """
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"{channel_obj.title}\n@{channel_obj.username}\n\n"
    await edit_or_reply(event, output_str)


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
