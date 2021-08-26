import os
from pathlib import Path

from telethon.tl.types import InputMessagesFilterDocument

from . import *


@bot.on(hell_cmd(pattern="extdl$", outgoing=True))
@bot.on(sudo_cmd(pattern="extdl$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    chat = Config.PLUGIN_CHANNEL
    documentss = await bot.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(0, total)
    await event.delete()
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(
            await bot.get_messages(chat, ids=mxo), "hellbot/plugins/"
        )
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            await bot.send_message(
                event.chat_id,
                "Installed Plugin `{}` successfully.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )
        else:
            await bot.send_message(
                event.chat_id,
                "Plugin `{}` has been pre-installed and cannot be installed.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )


@bot.on(hell_cmd(pattern=r"installall (.*)"))
@bot.on(sudo_cmd(pattern=r"installall (.*)", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    chat = event.pattern_match.group(1)
    hell = await eor(event, f"Starting To Install Plugins From {chat} !!"
    )
    documentss = await bot.get_messages(chat, None, filter=InputMessagesFilterDocument)
    total = int(documentss.total)
    total_doxx = range(0, total)
    for ixo in total_doxx:
        mxo = documentss[ixo].id
        downloaded_file_name = await event.client.download_media(
            await bot.get_messages(chat, ids=mxo), "hellbot/plugins/"
        )
        if "(" not in downloaded_file_name:
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            load_module(shortname.replace(".py", ""))
            sed = f"Installing Plugins From {chat}"
            logger.info(sed)
            await bot.send_message(
                event.chat_id,
                "Installed Plugin `{}` successfully.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )
        else:
            await bot.send_message(
                event.chat_id,
                "Plugin `{}` has been pre-installed and cannot be installed.".format(
                    os.path.basename(downloaded_file_name)
                ),
            )


if Config.PLUGIN_CHANNEL:
    async def extdl():
        docs = await bot.get_messages(
            Config.PLUGIN_CHANNEL, None, filter=InputMessagesFilterDocument
        )
        total = int(docs.total)
        for module in range(total):
            plug_ = docs[module].id
            plug_name = docs[module].file.name
            if os.path.exists(f"hellbot/plugins/{plug_name}"):
                return
            downloaded_file_name = await bot.download_media(
                await bot.get_messages(Config.PLUGIN_CHANNEL, ids=plug_),
                "hellbot/plugins/",
            )
            path1 = Path(downloaded_file_name)
            shortname = path1.stem
            loop = True
            while loop:
                try:
                    load_module(shortname.replace(".py", ""))
                    break
                except Exception as e:
                    await bot.send_message(Config.LOGGER_ID, f"Failed to install `{shortname}` \n\n`{e}`")
            if BOTLOG:
                await bot.send_message(Config.LOGGER_ID,
                    f"**Installed** `{os.path.basename(downloaded_file_name)}` **successfully.**",
                )

    bot.loop.create_task(install())


CmdHelp("extra_py").add_command(
  "extdl", None, "Installs all plugins from the channal which id is in PLUGIN_CHANNEL Configiable"
).add_command(
  "installall", "<channel/grp username>", "Installs all the plugins in provided channel / group. (May get floodwait error)"
).add_info(
  "Extra Plugins."
).add_warning(
  "✅ Harmless Module."
).add()
