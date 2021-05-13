import os
import re
import requests

import PIL.ImageOps
from PIL import Image

# convertions are done here...


# make a image
def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.jpg", "jpeg")
    os.remove(image)
    return "./temp/temp.jpg"


# make a sticker
async def convert_tosticker(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.webp", "webp")
    os.remove(image)
    return "./temp/temp.webp"

# hellbot
