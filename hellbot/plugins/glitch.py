########### IMPORTANT #############
# Original Plugin By -> @Krishna_Singhal
# Plugin link -> https://github.com/UsergeTeam/Userge-Plugins/blob/master/plugins/glitch.py
# Info -> Glitch plugin for Userge made by @Krishna_Singhal in Pyrogram.

# Ported from Pyrogram to Telethon by @ForGo10God for †hê Hêllẞø†

# USE WITH CREDITS !!
##################################

import os

from PIL import Image
from glitch_this import ImageGlitcher

from . import *

Glitched = Config.TMP_DOWNLOAD_DIRECTORY + "glitch.gif"


@hell_cmd(pattern="glitch(?:\s|$)([\s\S]*)")
async def glitch_(event):
    hell = await eor(event, "`Trying to glitch this ...`")
    replied = await event.get_reply_message()
    inp = event.text[8:]
    if not (replied and (
            replied.photo or replied.sticker or replied.video or replied.gif)):
        return await hell.edit("```Media not found...```")
    if inp != "":
        if not inp.isdigit():
            return await eod(hell, "**Invalid Input !!** \n\nPlease enter digits only.")
        input_ = int(inp)
        if not 0 < input_ < 9:
            return await eod(hell, "**Invalid Range !!** \n\n**Valid Range** - 1 to 8")
        args = input_
    else:
        args = 2
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    await hell.edit("`Glitchingggggg`")
    dls = await event.client.download_media(
        replied,
        Config.TMP_DOWNLOAD_DIRECTORY
    )
    dls_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, os.path.basename(dls))
    glitch_file = None
    if dls.endswith(".tgs"):
        file_1 = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "glitch.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {file_1}"
        stdout, stderr = (await runcmd(cmd))[:2]
        if not os.path.lexists(file_1):
            await eod(hell, "```Sticker not found...```")
            raise Exception(stdout + stderr)
        glitch_file = file_1
    elif dls.endswith(".webp"):
        file_2 = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "glitch.png")
        os.rename(dls_loc, file_2)
        if not os.path.lexists(file_2):
            await eod(hell, "```Sticker not found...```")
            return
        glitch_file = file_2
    elif replied.gif or replied.video:
        file_3 = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "glitch.png")
        await take_ss(dls_loc, 0, file_3)
        if not os.path.lexists(file_3):
            await eod(hell, "```Sticker not found...```")
            return
        glitch_file = file_3
    if glitch_file is None:
        glitch_file = dls_loc
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    message_id = replied.id
    glitch_img = glitcher.glitch_image(img, args, color_offset=True, gif=True)
    DURATION = 200
    LOOP = 0
    glitch_img[0].save(
        Glitched,
        format='GIF',
        append_images=glitch_img[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP)
    await event.client.send_file(
        event.chat_id,
        Glitched,
        reply_to=message_id)
    os.remove(Glitched)
    await hell.delete()
    for files in (dls_loc, glitch_file):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("glitch").add_command(
  "glitch", "1 to 8", "Glitches the replied gif/sticker/pic/video.", "glitch 5 <reply_to_a_media>"
).add_info(
  "Glitcher"
).add_warning(
  "✅ Harmless Module."
).add()
