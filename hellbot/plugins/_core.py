import asyncio
from datetime import datetime
import io
import os
from pathlib import Path

from telethon import events, functions, types
from telethon.tl.types import InputMessagesFilterDocument

from . import *


@bot.on(hell_cmd(pattern=r"cmds"))
@bot.on(sudo_cmd(pattern=r"cmds", allow_sudo=True))
async def kk(event):
    if event.fwd_from:
        return
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    cmd = "ls hellbot/plugins"
    thumb = hell_logo
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"List of Plugins in bot :- \n\n{o}\n\n<><><><><><><><><><><><><><><><><><><><><><><><>\nHELP:- If you want to know the commands for a plugin, do :- \n.plinfo <plugin name> without the < > brackets. \nJoin {hell_grp} for help."
    if len(OUTPUT) > 69:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "cmd_list.text"
            hell_file = await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                thumb=thumb,
                reply_to=reply_to_id,
            )
            await edit_or_reply(hell_file, f"Output Too Large. This is the file for the list of plugins in bot.\n\n**BY :-** {HELL_USER}")
            await event.delete()


@bot.on(hell_cmd(pattern=r"send (?P<shortname>\w+)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"send (?P<shortname>\w+)", allow_sudo=True))
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    thumb = hell_logo
    input_str = event.pattern_match.group(1)
    omk = f"**• Plugin name ≈** `{input_str}`\n**• Uploaded by ≈** {hell_mention}\n\n⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt]({chnl_link})** ⚡"
    the_plugin_file = "./hellbot/plugins/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
        lauda = await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            thumb=thumb,
            caption=omk,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
        await event.delete()
    else:
        await eod(event, "File not found..... Kek")


@bot.on(hell_cmd(pattern="install$", outgoing=True))
@bot.on(sudo_cmd(pattern="install$", allow_sudo=True))
async def install(event):
    if event.fwd_from:
        return
    a = "__Installing.__"
    b = 1
    await event.edit(a)
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "./hellbot/plugins/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                if shortname in CMD_LIST:
                    string = "**Commands found in** `{}`\n".format((os.path.basename(downloaded_file_name)))
                    for i in CMD_LIST[shortname]:
                        string += "  •  `" + i 
                        string += "`\n"
                        if b == 1:
                            a = "__Installing..__"
                            b = 2
                        else:
                            a = "__Installing...__"
                            b = 1
                        await eor(event, a)
                    return await eor(event, f"✅ **Installed module** :- `{shortname}` \n✨ BY :- {hell_mention}\n\n{string}\n\n        ⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ ɦɛʟʟɮօt]({chnl_link})** ⚡", link_preview=False)
                return await eor(event, f"Installed module `{os.path.basename(downloaded_file_name)}`")
            else:
                os.remove(downloaded_file_name)
                return await eod(event, f"**Failed to Install** \n`Error`\nModule already installed or unknown format")
        except Exception as e: 
            await eod(event, f"**Failed to Install** \n`Error`\n{str(e)}")
            return os.remove(downloaded_file_name)

@bot.on(hell_cmd(pattern=r"uninstall (?P<shortname>\w+)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"uninstall (?P<shortname>\w+)", allow_sudo=True))
async def uninstall(kraken):
    if kraken.fwd_from:
        return
    shortname = kraken.pattern_match["shortname"]
    dir_path =f"./hellbot/plugins/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await eod(kraken, f"Uninstalled `{shortname}` successfully")
    except OSError as e:
        await kraken.edit("Error: %s : %s" % (dir_path, e.strerror))


@bot.on(hell_cmd(pattern=r"unload (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"unload (?P<shortname>\w+)$", allow_sudo=True))
async def unload(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await event.edit(f"Successfully unloaded `{shortname}`")
    except Exception as e:
        await event.edit(
            "Successfully unloaded {shortname}\n{}".format(
                shortname, str(e)
            )
        )


@bot.on(hell_cmd(pattern=r"load (?P<shortname>\w+)$"))
@bot.on(sudo_cmd(pattern=r"load (?P<shortname>\w+)$", allow_sudo=True))
async def load(event):
    if event.fwd_from:
        return
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await event.edit(f"Successfully loaded `{shortname}`")
    except Exception as e:
        await event.edit(
            f"Sorry, could not load {shortname} because of the following error.\n{str(e)}"
        )

CmdHelp("core").add_command(
  "install", "<reply to a .py file>", "Installs the replied python file if suitable to Hêllẞø†'s codes."
).add_command(
  "uninstall", "<plugin name>", "Uninstalls the given plugin from Hêllẞø†. To get that again do .restart", "uninstall alive"
).add_command(
  "load", "<plugin name>", "Loades the unloaded plugin to your userbot", "load alive"
).add_command(
  "unload", "<plugin name>", "Unloads the plugin from your userbot", "unload alive"
).add_command(
  "send", "<file name>", "Sends the given file from your userbot server, if any.", "send alive"
).add_command(
  "cmds", None, "Gives out the list of modules in HellBot."
).add_warning(
  "❌ Install External Plugin On Your Own Risk. We won't help if anything goes wrong after installing a plugin."
).add()

# hellbot
