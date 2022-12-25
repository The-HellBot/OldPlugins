import asyncio
import os

import cv2
from PIL import Image
from TelethonHell.plugins import *


@hell_cmd(pattern="mms(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "__Memifying ...__")
    hell = await _reply.download_media()
    if hell and hell.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell and hell.endswith((".webp", ".png")):
        pics = Image.open(hell)
        pics.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif hell:
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(hel_, "Unable to memify this!")
    output = await draw_meme_text(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
        os.remove(output)
    except BaseException:
        pass


@hell_cmd(pattern="mmf(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "__Memifying ...__")
    hell = await _reply.download_media()
    if hell and hell.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", hell, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif hell and hell.endswith((".webp", ".png")):
        pic = Image.open(hell)
        pic.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif hell:
        img = cv2.VideoCapture(hell)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(hel_, "Unable to memify this!")
    output = await draw_meme(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(hell)
        os.remove(file)
    except BaseException:
        pass
    os.remove(pic)


CmdHelp("memify").add_command(
    "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mms <reply to a img/stcr/gif> hii ; hello"
).add_command(
    "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mmf <reply to a img/stcr/gif> hii ; hello"
).add_info(
    "Memify images and stickers."
).add_warning(
    "✅ Harmless Module."
).add()
