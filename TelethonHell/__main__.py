import glob
import os
import sys
from pathlib import Path

from HellConfig import Config

from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.clients.session import H2, H3, H4, H5, Hell, HellBot
from TelethonHell.utils.plug import load_module, plug_channel
from TelethonHell.utils.startup import (join_it, logger_check, start_msg,
                                        update_sudo)
from TelethonHell.version import __hellver__

# Global Variables #
HELL_PIC = "https://te.legra.ph/file/cb0bd62632a3a2b6b2726.jpg"


# Client Starter
async def hells(session=None, client=None, session_name="Main"):
    num = 0
    if session:
        LOGS.info(f"••• Starting Client [{session_name}] •••")
        try:
            await client.start()
            num = 1
        except:
            LOGS.error(f"Error in {session_name}!! Check & try again!")
    return num


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as hell:
            path1 = Path(hell.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"TelethonHell/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))


# Final checks after startup
async def hell_is_on(total):
    await update_sudo()
    await logger_check(Hell)
    await start_msg(HellBot, HELL_PIC, __hellver__, total)
    await join_it(Hell)
    await join_it(H2)
    await join_it(H3)
    await join_it(H4)
    await join_it(H5)


# Hellbot starter...
async def start_hellbot():
    try:
        tbot_id = await HellBot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        Hell.tgbot = HellBot
        LOGS.info("••• Starting HellBot (TELETHON) •••")
        C1 = await hells(Config.HELLBOT_SESSION, Hell, "HELLBOT_SESSION")
        C2 = await hells(Config.SESSION_2, H2, "SESSION_2")
        C3 = await hells(Config.SESSION_3, H3, "SESSION_3")
        C4 = await hells(Config.SESSION_4, H4, "SESSION_4")
        C5 = await hells(Config.SESSION_5, H5, "SESSION_5")
        await HellBot.start()
        total = C1 + C2 + C3 + C4 + C5
        LOGS.info("••• HellBot Startup Completed •••")
        LOGS.info("••• Starting to load Plugins •••")
        await plug_load("TelethonHell/plugins/*.py")
        await plug_channel(Hell, Config.PLUGIN_CHANNEL)
        LOGS.info("⚡ Your HellBot Is Now Working ⚡")
        LOGS.info("Head to @Its_HellBot for Updates. Also join chat group to get help regarding HellBot.")
        LOGS.info(f"» Total Clients = {str(total)} «")
        await hell_is_on(total)
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


Hell.loop.run_until_complete(start_hellbot())

if len(sys.argv) not in (1, 3, 4):
    Hell.disconnect()
else:
    try:
        Hell.run_until_disconnected()
    except ConnectionError:
        pass


# hellbot
