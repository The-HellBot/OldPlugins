import asyncio
import os
import datetime

from PIL import Image, ImageDraw, ImageFont
from . import *


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


@bot.on(hell_cmd(pattern="time ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="time ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.datetime.now().strftime(
        "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\
        \n   HELLBOT TIMEZONE   \
        \n   LOCATION: India🇮🇳  \
        \n   Time: %H:%M:%S  \
        \n   Date: %d.%m.%y     \
        \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
    )
    start = datetime.datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = (
        Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.datetime.now()) + ".webp"
    )
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await bot.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
    )
    os.remove(required_file_name)
    end = datetime.datetime.now()
    time_taken_ms = (end - start).seconds
    await event.edit("Created sticker in {} seconds".format(time_taken_ms))
    await asyncio.sleep(3)
    await event.delete()


CmdHelp("time").add_command(
  "time", None, "Gives current time in a cool sticker format."
).add()
