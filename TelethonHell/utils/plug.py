import importlib
import logging
import os
import sys
from pathlib import Path

from HellConfig import Config
from telethon.tl.types import InputMessagesFilterDocument
from TelethonHell.clients.client_list import client_id
from TelethonHell.clients.decs import hell_cmd
from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.clients.session import H2, H3, H4, H5, Hell, HellBot
from TelethonHell.utils.cmds import CmdHelp
from TelethonHell.utils.decorators import admin_cmd, command, sudo_cmd
from TelethonHell.utils.extras import delete_hell, edit_or_reply
from TelethonHell.utils.globals import LOAD_PLUG


# load plugins
def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import TelethonHell.utils

        path = Path(f"TelethonHell/plugins/{shortname}.py")
        name = "TelethonHell.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("HellBot - Successfully imported " + shortname)
    else:
        import TelethonHell.utils

        path = Path(f"TelethonHell/plugins/{shortname}.py")
        name = "TelethonHell.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = Hell
        mod.H1 = Hell
        mod.H2 = H2
        mod.H3 = H3
        mod.H4 = H4
        mod.H5 = H5
        mod.Hell = Hell
        mod.HellBot = HellBot
        mod.tbot = HellBot
        mod.tgbot = Hell.tgbot
        mod.command = command
        mod.CmdHelp = CmdHelp
        mod.client_id = client_id
        mod.logger = logging.getLogger(shortname)
        mod.Config = Config
        mod.borg = Hell
        mod.hellbot = Hell
        mod.edit_or_reply = edit_or_reply
        mod.eor = edit_or_reply
        mod.delete_hell = delete_hell
        mod.eod = delete_hell
        mod.Var = Config
        mod.admin_cmd = admin_cmd
        mod.hell_cmd = hell_cmd
        mod.sudo_cmd = sudo_cmd
        sys.modules["userbot.utils"] = TelethonHell
        sys.modules["userbot"] = TelethonHell
        sys.modules["userbot.events"] = TelethonHell
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["TelethonHell.plugins." + shortname] = mod
        LOGS.info("⚡ Hêllẞø† ⚡ - Successfully Imported " + shortname)


# remove plugins
def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                Hell.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"TelethonHell.plugins.{shortname}"

            for i in reversed(range(len(Hell._event_builders))):
                ev, cb = Hell._event_builders[i]
                if cb.__module__ == name:
                    del Hell._event_builders[i]
    except BaseException:
        raise ValueError


async def plug_channel(client, channel):
    if channel != 0:
        LOGS.info("⚡ Hêllẞø† ⚡ - PLUGIN CHANNEL DETECTED.")
        LOGS.info("⚡ Hêllẞø† ⚡ - Starting to load extra plugins.")
        plugs = await client.get_messages(channel, None, filter=InputMessagesFilterDocument)
        total = int(plugs.total)
        for plugins in range(total):
            plug_id = plugs[plugins].id
            plug_name = plugs[plugins].file.name
            if os.path.exists(f"TelethonHell/plugins/{plug_name}"):
                return
            downloaded_file_name = await client.download_media(
                await client.get_messages(channel, ids=plug_id),
                "TelethonHell/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            try:
                load_module(shortname.replace(".py", ""))
            except Exception as e:
                LOGS.error(str(e))


# hellbot
