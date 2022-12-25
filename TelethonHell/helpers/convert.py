import asyncio
import os
import re
import time
from os.path import basename
from typing import Optional

from HellConfig import Config
from PIL import Image
from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.helpers.progress import progress
from TelethonHell.helpers.runner import runcmd
from TelethonHell.helpers.vids import take_screen_shot
from TelethonHell.utils.extras import edit_or_reply as eor

dwlpath = Config.TMP_DOWNLOAD_DIRECTORY

# convertions are done here...

# make a image
async def convert_to_image(event, client):
    hell = await event.get_reply_message()
    if not (
        hell.gif
        or hell.audio
        or hell.voice
        or hell.video
        or hell.video_note
        or hell.photo
        or hell.sticker
        or hell.media
    ):
        await eor(event, "`Format Not Supported.`")
        return
    else:
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                hell.media,
                dwlpath,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "`Downloading...`")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await eor(event, str(e))
        else:
            await eor(
                event, "Downloaded to `{}` successfully.".format(downloaded_file_name)
            )
    if not os.path.exists(downloaded_file_name):
        await eor(event, "Download Unsucessfull :(")
        return
    if hell and hell.photo:
        hell_final = downloaded_file_name
    elif hell.sticker and hell.sticker.mime_type == "application/x-tgsticker":
        rpath = downloaded_file_name
        image_name20 = os.path.join(dwlpath, "omk.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {downloaded_file_name} {image_name20}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(rpath)
        hell_final = image_name20
    elif hell.sticker and hell.sticker.mime_type == "image/webp":
        pathofsticker2 = downloaded_file_name
        image_new_path = dwlpath + "image.png"
        im = Image.open(pathofsticker2)
        im.save(image_new_path, "PNG")
        if not os.path.exists(image_new_path):
            await eor(event, "`Unable To Fetch Shot.`")
            return
        hell_final = image_new_path
    elif hell.audio:
        omk_p = downloaded_file_name
        hmmyes = dwlpath + "semx.mp3"
        imgpath = dwlpath + "semxy.jpg"
        os.rename(omk_p, hmmyes)
        await runcmd(f"ffmpeg -i {hmmyes} -filter:v scale=500:500 -an {imgpath}")
        os.remove(omk_p)
        if not os.path.exists(imgpath):
            await eor(event, "`Unable To Fetch Shot.`")
            return
        hell_final = imgpath
    elif hell.gif or hell.video or hell.video_note:
        omk_p2 = downloaded_file_name
        jpg_file = os.path.join(dwlpath, "image.jpg")
        await take_screen_shot(omk_p2, 0, jpg_file)
        os.remove(omk_p2)
        if not os.path.exists(jpg_file):
            await eor(event, "`Couldn't Fetch shot`")
            return
        hell_final = jpg_file
    return hell_final


async def take_ss(video_file: str, duration: int, path: str = "") -> Optional[str]:
    LOGS.info(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join(dwlpath, f"{basename(video_file)}.jpg")
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def tgs_to_gif(file, tgs=False, video=False):
    if tgs:
        cmd = f"lottie_convert.py '{file}' 'hellbot.gif'"
    elif video:
        cmd = f"ffmpeg -i '{file}' -c copy 'hellbot.gif'"
    await runcmd(cmd)
    return 'hellbot.gif'


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


async def get_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


async def VSticker(event, file):
    _width_ = file.file.width
    _height_ = file.file.height
    if _height_ > _width_:
        _height_, _width_ = (512, -1)
    else:
        _height_, _width_ = (-1, 512)
    _video = await event.client.download_media(file, dwlpath)
    await runcmd(
        f"ffmpeg -to 00:00:02.900 -i '{_video}' -vf scale={_width_}:{_height_} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an 'VideoSticker.webm'"
    )
    os.remove(_video)
    return "VideoSticker.webm"


# hellbot
