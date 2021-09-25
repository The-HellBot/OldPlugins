import datetime
import os
import random
import time

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterDocument

from . import *


PICS_STR = []

@hell_cmd(pattern="logo ?(.*)")
async def _(event):
    hell = await eor(event, "`Processing.....`")
    text = event.text[6:]
    if text == "":
        await eod(hell, "**Give some text to make a logo !!**")
        return
    cid = await client_id(event)
    hell_mention = cid[2]
    start = datetime.datetime.now()
    fnt = await get_font_file(event.client, "@HELL_FRONTS")
    if event.reply_to_msg_id:
        rply = await event.get_reply_message()
        try:
            logo_ = await rply.download_media()
        except:
            pass
    else:
        await hell.edit("Picked a Logo BG...")
        async for i in event.client.iter_messages("@HELLBOT_LOGOS", filter=InputMessagesFilterPhotos):
            PICS_STR.append(i)
        pic = random.choice(PICS_STR)
        logo_ = await pic.download_media()
    if len(text) <= 8:
        font_size_ = 150
        strik = 10
    elif len(text) >= 9:
        font_size_ = 50
        strik = 5
    else:
        font_size_ = 130
        strik = 20
    await hell.edit("Making Logo...")
    img = Image.open(logo_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fnt, font_size_)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
    )
    w_ = (image_width - w) / 2
    h_ = (image_height - h) / 2
    draw.text(
        (w_, h_), text, font=font, fill="white", stroke_width=strik, stroke_fill="black"
    )
    file_name = "HellBot.png"
    end = datetime.datetime.now()
    ms = (end - start).seconds
    img.save(file_name, "png")
    await event.client.send_file(
        event.chat_id,
        file_name,
        caption=f"**Made By :** {hell_mention} \n**Time Taken :** `{ms} seconds`",
    )
    await hell.delete()
    try:
        os.remove(file_name)
        os.remove(fnt)
        os.remove(logo_)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


CmdHelp("logos").add_command(
  "logo", "<reply to pic + text> or <text>", "Makes a logo with the given text. If replied to a picture makes logo on that else gets random BG."
).add_info(
  "Logo Maker.\n**🙋🏻‍♂️ Note :**  Currently only supports custom pics. Fonts are choosen randomly."
).add_warning(
  "✅ Harmless Module."
).add()
