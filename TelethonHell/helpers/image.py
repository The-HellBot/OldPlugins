import math
import random
import re

from aiohttp import ClientSession as aio_client
from bs4 import BeautifulSoup
import PIL.ImageOps
from PIL import Image, ImageFont, ImageDraw
from telethon.tl.types import InputMessagesFilterDocument


# inverting colors...
async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(endname)


# upside down...
async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.flip(image)
    inverted_image.save(endname)


# gray tone...
async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)


# mirrored...
async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.mirror(image)
    inverted_image.save(endname)


# sun kissed...
# print("Agar Suraj ne sachme chum lia to gand fatt jaegi")
async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.solarize(image, threshold=128)
    inverted_image.save(endname)


async def resize_photo(photo):
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


async def get_font_size(font, text, image):
    temp_size = 100
    _font = ImageFont.truetype(font, temp_size)
    img = Image.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(img)
    wid, _ = draw.textsize(text, _font)
    _font_size = (
        temp_size / (wid / image.width) * 0.7
    )
    return round(_font_size)


async def unsplash(search, limit):
    _url = f"https://unsplash.com/s/photos/{search}"
    async with aio_client() as session:
        _data = await session.get(_url)
        aio_res = await _data.read()
    bs_res = BeautifulSoup(aio_res, "html.parser", from_encoding="utf-8")
    all_res = bs_res.find_all("img", srcset=re.compile("images.unsplash.com/photo"))
    random.shuffle(all_res)
    return list(map(lambda e: e['src'], all_res[:limit]))

# hellbot
