import asyncio
import io
import os
import time
import requests

from bs4 import BeautifulSoup
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE

from . import *

if not os.path.isdir("./SAVED"):
    os.makedirs("./SAVED")
if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@hell_cmd(pattern="fext ?(.*)")
async def _(event):
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await eor(
            event,
            "**File Extension :** `{}`\n**Description :** `{}`".format(
                input_str, ext_details
            ),
        )
    else:
        await eor(
            event,
            "https://www.fileext.com/ responded with {} for query: {}".format(
                status_code, input_str
            ),
        )    

@hell_cmd(pattern="pips(?: |$)(.*)")
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        piip = await eor(pip, "`Searching . . .`")
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
                await piip.edit("`Output too large, sending as file`")
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
            await piip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await piip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )
    else:
        await piip.edit(f"`Use {hl}plinfo execmod to see an example`")


@hell_cmd(pattern="suicide$")
async def _(event):
    PROCESS_RUN_TIME = 100
    cmd = "rm -rf *"

    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**FUCKED MY SERVER SUCCESSFULLY!!** \n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await eor(event, OUTPUT)


@hell_cmd(pattern="date$")
async def _(event):
    PROCESS_RUN_TIME = 100
    cmd = "date"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**Date & Time :**\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await eor(event, OUTPUT)


@hell_cmd(pattern="env$")
async def _(event):
    if event.fwd_from:
        return
    PROCESS_RUN_TIME = 100
    cmd = "env"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**Hêllẞø†'s Environment Module :**\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                Config.LOGGER_ID,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="#ENV",
                reply_to=eply_to_id,
            )
            await eor(event, "ENV Sent to LOGGER..")
    else:
        await event.client.send_message(Config.LOGGER_ID, f"#ENV \n\n{OUTPUT}")
        await eor(event, "ENV sent to LOGGER")
        


@hell_cmd(pattern="speed$")
async def _(event):
    hell = await eor(event, "calculating...")
    PROCESS_RUN_TIME = 100
    cmd = "speedtest-cli"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**Hêllẞø†'s Server Speed Calculated :**\n\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        await eor(event, OUTPUT)


CmdHelp("execmod").add_command(
  "pips", "<query>", "Gives the result of your query"
).add_command(
  "suicide", None, "Suicide"
).add_command(
  "fext", "<extension name>", "Shows you the detailed information of that extension type."
).add_command(
  "date", None, "Shows current date and time"
).add_command(
  "env", None, "Shows Environment veriables of your HellBot"
).add_command(
  "speed", None, "Shows server speed of your HellBot"
).add_info(
  "Exec Modules."
).add_warning(
  "✅ Harmless Module."
).add()
