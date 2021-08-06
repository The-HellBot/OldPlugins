import os
import asyncio
import re
import requests
import time
import lottie

import PIL.ImageOps
from PIL import Image
from hellbot import *
from hellbot.helpers import *
hellpath = Config.TMP_DOWNLOAD_DIRECTORY
if not os.path.isdir(hellpath):
    os.makedirs(hellpath)
    
# convertions are done here...
#
# make a image
async def convert_toimage(event, bot):
    rply = await event.get_reply_message()
    if not (
            rply.gif
            or rply.audio
            or rply.voice
            or rply.video
            or rply.video_note
            or rply.photo
            or rply.sticker
            or rply.media
    ):
        await event.edit("`File Format Not Supported`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await bot.download_media(
                rply.media,
                hellpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit(
                "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await event.edit("Download Unsucessfull :(")
        return
    if rply and rply.photo:
        rply_final = downloaded_file_name
    elif rply.sticker and rply.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(hellpath, "HELL.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        rply_final = image_name20
    elif rply.sticker and rply.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = hellpath + "image.png"
        im = Image.open(pathofsticker2)
        im.save(image_new_path, "PNG")
        if not os.path.exists(image_new_path):
            await event.edit("`Error`")
            return
        rply_final = image_new_path
    elif rply.audio:
        hell_p = downloaded_file_name
        hmmyes = hellpath + "hellboy.mp3"
        imgpath = hellpath + "hellboy.jpg"
        os.rename(hell_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(hell_p)
        if not os.path.exists(imgpath):
            await event.edit("`Error`")
            return
        rply_final = imgpath
    elif rply.gif or rply.video or rply.video_note:
        hell_p2 = downloaded_file_name
        jpg_file = os.path.join(hellpath, "image.jpg")
        await take_screen_shot(hell_p2, 0, jpg_file)
        os.remove(hell_p2)
        if not os.path.exists(jpg_file):
            await event.edit("`Error`")
            return
        rply_final = jpg_file
    return lmao_final

# make a sticker
async def convert_tosticker(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.webp", "webp")
    os.remove(image)
    return "./temp/temp.webp"


# deal with it...
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


# hellbot
