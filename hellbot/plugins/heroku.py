import os
import sys
import asyncio
from os import execl
from time import sleep

from . import *


@bot.on(hell_cmd(pattern="restart$"))
@bot.on(sudo_cmd(pattern="restart$", allow_sudo=True))
async def re(hell):
    if hell.fwd_from:
        return
    event = await eor(hell, "Restarting Dynos ...")
    await event.edit("✅ **Restarted Dynos** \n**Type** `.ping` **after 1 minute to check if I am working!**")
    await bot.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@bot.on(hell_cmd(pattern="shutdown$"))
@bot.on(sudo_cmd(pattern="shutdown$", allow_sudo=True))
async def down(hell):
    if hell.fwd_from:
        return
    await hell.edit("**[ ! ]** Turning off Hêllẞø† Dynos... Manually turn me on later ಠ_ಠ")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["userbot"].scale(0)
    else:
        sys.exit(0)


CmdHelp("power").add_command(
  "restart", None, "Restarts your userbot. Redtarting Bot may result in better functioning of bot when its laggy"
).add_command(
  "shutdown", None, "Turns off Dynos of Userbot. Userbot will stop working unless you manually turn it on from heroku"
).add_info(
  "Power Switch For Bot"
).add()
