import asyncio
import io
import os
import time
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE

from . import *

if not os.path.isdir("./SAVED"):
    os.makedirs("./SAVED")
if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@bot.on(hell_cmd(pattern="pips(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="pips(?: |$)(.*)", allow_sudo=True))
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        pip = await eor(pip, "`Searching . . .`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output too large, sending as file`")
                file = open("pips.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "pips.txt",
                    reply_to=pip.id,
                    caption=pipmodule,
                )
                os.remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await pip.edit(f"`Use {hl}plinfo execmod to see an example`")


@bot.on(hell_cmd(pattern="suicide$"))
@bot.on(sudo_cmd(pattern="suicide$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "rm -rf *"
    #    if dirname == tempdir:

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Hêllẞø†'s](tg://need_update_for_some_feature/) SUICIDE BOMB:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await event.edit(OUTPUT)


@bot.on(hell_cmd(pattern="date$"))
@bot.on(sudo_cmd(pattern="date$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "date"
    #    if dirname == tempdir:

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**Date & Time Of India:**\n\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await event.edit(OUTPUT)


@bot.on(hell_cmd(pattern="env$"))
@bot.on(sudo_cmd(pattern="env$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "env"
    #    if dirname == tempdir:

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Hêllẞø†'s](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await bot.send_file(
                Config.LOGGER_ID,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="#ENV",
                reply_to=eply_to_id,
            )
            await event.edit("ENV Sent to LOGGER..")
            await event.delete()
    else:
        await bot.send_message(Config.LOGGER_ID, f"#ENV \n\n{OUTPUT}")
        await event.edit("ENV sent to LOGGER")
        


@bot.on(hell_cmd(pattern="speed$"))
@bot.on(sudo_cmd(pattern="speed$", allow_sudo=True))
async def _(event):
    await event.edit("calculating...")
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "speedtest-cli"
    #    if dirname == tempdir:

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[Hêllẞø†'s](tg://need_update_for_some_feature/) , Server Speed Calculated:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await event.edit(OUTPUT)


CmdHelp("execmod").add_command(
  "pips", "<query>", "Gives the result of your query"
).add_command(
  "suicide", None, "Suicide"
).add_command(
  "date", None, "Shows current date and time"
).add_command(
  "env", None, "Shows Environment veriables from Heroku"
).add_command(
  "speed", None, "Shows server speed of your bot"
).add_info(
  "Exec Modules."
).add_warning(
  "✅ Harmless Module."
).add()
