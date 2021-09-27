import asyncio
import io
import os
import time

from . import *

if not os.path.isdir("./SAVED"):
    os.makedirs("./SAVED")
if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@hell_cmd(pattern="ls ?(.*)")
async def lst(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        msg = "📂 **Files in {} :**\n".format(input_str)
        files = os.listdir(input_str)
    else:
        msg = "📂 **Files in Current Directory :**\n"
        files = os.listdir(os.getcwd())
    for file in files:
        msg += "📑 `{}`\n".format(file)
    if len(msg) <= Config.MAX_MESSAGE_SIZE_LIMIT:
        await eor(event, msg)
    else:
        msg = msg.replace("`", "")
        out = "filesList.txt"
        with open(out, "w") as f:
            f.write(f)
        await event.client.send_file(
            event.chat_id,
            out,
            force_document=True,
            allow_cache=False,
            caption="`Output is huge. Sending as a file...`",
        )
        await event.delete()


@hell_cmd(pattern="ls_local$")
async def _(event):
    PROCESS_RUN_TIME = 100
    cmd = "ls -lh ./DOWNLOADS/"
    event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in Hêllẞø† DOWNLOADS Folder:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    if stderr.decode():
        await eor(event, f"**{stderr.decode()}**")
        return
    await eor(event, f"{OUTPUT}`{stdout.decode()}`")


@hell_cmd(pattern="ls_root$")
async def _(event):
    PROCESS_RUN_TIME = 100
    cmd = "ls -lh"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    if stderr.decode():
        await eor(event, f"**{stderr.decode()}**")
        return
    await eor(event, f"{OUTPUT}`{stdout.decode()}`")


@hell_cmd(pattern="ls_saved$")
async def _(event):
    PROCESS_RUN_TIME = 100
    cmd = "ls ./SAVED/"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in SAVED directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    if stderr.decode():
        await eor(event, f"**{stderr.decode()}**")
        return
    await eor(event, f"{OUTPUT}`{stdout.decode()}`")


@hell_cmd(pattern="rnsaved ?(.*)")
async def _(event):
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        src, dst = input_str.split("|")
        src = src.strip()
        dst = dst.strip()
    cmd = f"mv ./SAVED/{src} ./SAVED/{dst}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    if stderr.decode():
        await eor(event, f"**{stderr.decode()}**")
        return
    await eor(event, f"File renamed `{src}` to `{dst}`")


@hell_cmd(pattern="rnlocal ?(.*)")
async def _(event):
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        src, dst = input_str.split("|")
        src = src.strip()
        dst = dst.strip()
    cmd = f"mv ./DOWNLOADS/{src} ./DOWNLOADS/{dst}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id,
            )
            await event.delete()
    if stderr.decode():
        await eor(event, f"**{stderr.decode()}**")
        return
    await eor(event, f"File renamed `{src}` to `{dst}`")


@hell_cmd(pattern="delsave (.*)")
async def handler(event):
    input_str = event.pattern_match.group(1)
    pathtofile = f"./SAVED/{input_str}"

    if os.path.isfile(pathtofile):
        os.remove(pathtofile)
        await eod(event, "✅ File Deleted 🗑")
    else:
        await eod(event, "⛔️File Not Found😬")


@hell_cmd(pattern="delocal (.*)")
async def handler(event):
    input_str = event.pattern_match.group(1)
    pathtofile = f"./DOWNLOADS/{input_str}"

    if os.path.isfile(pathtofile):
        os.remove(pathtofile)
        await eod(event, "✅ File Deleted 🗑")
    else:
        await eod(event, "⛔️File Not Found😬")


CmdHelp("managers").add_command(
  "ls_local", None, "Gives the list of downloaded medias in your hellbot server."
).add_command(
  "ls_root", None, "Gives the list of all files in root directory of Hellbot repo."
).add_command(
  "ls_saved", None, "Gives the list of all files in Saved directory of your hellbot server"
).add_command(
  "rnsaved", "from | to", "Renames the file in saved directory"
).add_command(
  "rnlocal", "from | to", "Renames the file in downloaded directory"
).add_command(
  "delsave", "saved path", "Deletes the file from given saved path"
).add_command(
  "delocal", "downloaded path", "Deletes the file from given downloaded path"
).add_command(
  "ls", "<path name>", "Gives the list of all files in the given path"
).add_info(
  "HellBot Managers."
).add_warning(
  "✅ Harmless Module."
).add()
