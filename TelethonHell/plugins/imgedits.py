import io
import os
from random import randint, uniform

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeFilename
from TelethonHell.plugins import *
from vcam import meshGen, vcam


@hell_cmd(pattern="feye$")
async def fun(event):
    path = "omk"
    hell = await eor(event, "Editing In Progress...")
    reply = await event.get_reply_message()
    lol = await event.client.download_media(reply.media, path)
    file_name = "fishy.jpg"
    hehe = path + "/" + file_name
    img = cv2.imread(lol)
    H, W = img.shape[:2]
    c1 = vcam(H=H, W=W)
    plane = meshGen(H, W)
    plane.Z -= 100 * np.sqrt(
        (plane.X * 1.0 / plane.W) ** 2 + (plane.Y * 1.0 / plane.H) ** 2
    )
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x, map_y = c1.getMaps(pts2d)
    output = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=0)
    output = cv2.flip(output, 1)
    out1 = cv2.resize(output, (700, 350))
    cv2.imwrite(file_name, out1)
    await event.client.send_file(event.chat_id, file_name)
    await hell.delete()
    for files in (hehe, lol):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="warp$")
async def fun(event):
    path = "omk"
    hell = await eor(event, "Warping In Progress...")
    reply = await event.get_reply_message()
    lol = await event.client.download_media(reply.media, path)
    file_name = "warped.jpg"
    hehe = path + "/" + file_name
    img = cv2.imread(lol)
    H, W = img.shape[:2]
    c1 = vcam(H=H, W=W)
    plane = meshGen(H, W)
    plane.Z += (
        20
        * np.exp(-0.5 * ((plane.Y * 1.0 / plane.H) / 0.1) ** 2)
        / (0.1 * np.sqrt(2 * np.pi))
    )
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x, map_y = c1.getMaps(pts2d)
    output = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=0)
    output = cv2.flip(output, 1)
    out1 = cv2.resize(output, (700, 350))
    cv2.imwrite(file_name, out1)
    await event.client.send_file(event.chat_id, file_name)
    await hell.delete()
    for files in (hehe, lol):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="distort$")
async def fun(event):
    path = "omk"
    hell = await eor(event, "Distortion In Progress...")
    reply = await event.get_reply_message()
    lol = await event.client.download_media(reply.media, path)
    file_name = "dist.jpg"
    hehe = path + "/" + file_name
    img = cv2.imread(lol)
    H, W = img.shape[:2]
    c1 = vcam(H=H, W=W)
    plane = meshGen(H, W)
    plane.Z += (
        20
        * np.exp(-0.5 * ((plane.X * 1.0 / plane.W) / 0.1) ** 2)
        / (0.1 * np.sqrt(2 * np.pi))
    )
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x, map_y = c1.getMaps(pts2d)
    output = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=0)
    output = cv2.flip(output, 1)
    out1 = cv2.resize(output, (700, 350))
    cv2.imwrite(file_name, out1)
    await event.client.send_file(event.chat_id, file_name)
    await hell.delete()
    for files in (hehe, lol):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="frybot$")
async def _(event):
    reply = await event.get_reply_message()
    if not reply:
        return await parse_error(event, "No replied message found.")
    data = await check_media(reply)
    if isinstance(data, bool):
        return await parse_error(event, "Invalid media format.")
    chat = "@image_deepfrybot"
    hell = await eor(event, "`Processing`")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message(reply)
            response = await conv.get_response()
        except YouBlockedUserError:
            return await parse_error(hell, "__Unblock @image_deepfrybot and try again.__", False)
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_file(event.chat_id, response.message.media)
        await event.client.delete_messages(conv.chat_id, [first.id, response.id])
        await hell.delete()


@hell_cmd(pattern="fry(?:\s|$)([\s\S]*)")
async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 2
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await parse_error(event, "Invalid media format.")
            return
    else:
        await parse_error(event, "No replied message found.")
        return
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)
    hmm = await eor(event, "`Deep frying media…`")
    for _ in range(frycount):
        image = await deepfry(image)
    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)
    await event.reply(file=fried_io)
    await hmm.delete()


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )
    img = img.copy().convert("RGB")
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))
    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    if not data or data is None:
        return False
    return data


CmdHelp("imgedits").add_command(
    "feye", "<reply to a img/stcr>", "Edits the replied image or sticker to a 3-D Box like image."
).add_command(
    "warp", "<reply to a img/stcr>", "Edits the replied image or sticker to a funny image. `#Must_Try` !!"
).add_command(
    "distort", "<reply to a img/stcr>", "Edits the replied image or sticker to a funny image. `#Must_Try` !!"
).add_command(
    "frybot", "<reply to a image/sticker>", "Fries the given sticker or image"
).add_command(
    "fry", "<1-9> <reply to image/sticker>", "Fries the given sticker or image based on level if you dont give anything then it is default to 2"
).add_info(
    "Funs are here boiz"
).add_warning(
    "✅ Harmless Module."
).add()
