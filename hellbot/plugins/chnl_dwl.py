import os
import subprocess

from . import *

@hell_cmd(pattern="getc ([\s\S]*)")
async def get_media(event):
    dir = "./channel_dwl/"
    try:
        os.makedirs("./channel_dwl/")
    except:
        pass
    channel_username = event.text
    limit = channel_username[6:9]
    print(limit)
    channel_username = channel_username[11:]
    print(channel_username)
    hell = await eor(event, "Downloading Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await client.event.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "channel_dwl"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await hell.edit("Downloaded " + output + " files.")


@hell_cmd(pattern="geta ([\s\S]*)")
async def get_media(event):
    dir = "./channel_dwl/"
    try:
        os.makedirs("./channel_dwl/")
    except:
        pass
    channel_username = event.text
    channel_username = channel_username[7:]

    print(channel_username)
    hell = await eor(event, "Downloading All Media From this Channel.")
    msgs = await bot.get_messages(channel_username, limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "channel_dwl"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await hell.edit("Downloaded " + output + " files.")


CmdHelp("chnl_dwl").add_command(
  "geta", "channel username", "will download all media from channel into your bot server but there is limit of 3000 to prevent API limits."
).add_command(
  "getc", "<limit> <channel username>", "will download latest given number of media from channel into your bot server", "getc 1000 @Its_HellBot"
).add_info(
  "Channel Media Download"
).add_warning(
  "✅ Harmless Module."
).add()
