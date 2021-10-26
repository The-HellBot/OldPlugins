import cv2
import html
import os

from PIL import Image
from telegraph import upload_file
from telethon.tl.functions.users import GetFullUserRequest

from . import *


dwllpath = "./imgs/"
if not os.path.isdir(dwllpath):
    os.makedirs(dwllpath)


@hell_cmd(pattern="thug$")
async def _(event):
    if not event.reply_to_msg_id:
        return await eod(event, "Reply to a image...")
    hell = await eor(event, "`Converting To thug Image..`")
    await event.get_reply_message()
    img = await convert_to_image(event, event.client)
    imagePath = img
    maskPath = "./hellbot/resources/pics/mask (1).png"
    cascPath = "./hellbot/resources/xmls/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.15)
    background = Image.open(imagePath)
    for (x, y, w, h) in faces:
        mask = Image.open(maskPath)
        mask = mask.resize((w, h), Image.ANTIALIAS)
        offset = (x, y)
        background.paste(mask, offset, mask=mask)
    file_name = "thug.png"
    ok = dwllpath + "/" + file_name
    background.save(ok, "PNG")
    await event.client.send_file(event.chat_id, ok)
    await hell.delete()
    for files in (ok, img):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="trigger$")
async def _(event):
    hell = await eor(event, "`Trigggggggggerrr`")
    owo = await event.get_reply_message()
    img = await convert_to_image(event, bot)
    url_s = upload_file(img)
    imglink = f"https://telegra.ph{url_s[0]}"
    doit = f"https://some-random-api.ml/canvas/triggered?avatar={imglink}"
    r = requests.get(doit)
    open("triggered.gif", "wb").write(r.content)
    lolbruh = "triggered.gif"
    await event.client.send_file(
        event.chat_id, lolbruh, caption="You got triggered....", reply_to=owo
    )
    await hell.delete()
    for files in (lolbruh, img):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="geyy$")
async def _(event):
    hell = await eor(event, "`Geyyyy`")
    owo = await event.get_reply_message()
    img = await convert_to_image(event, event.client)
    url_s = upload_file(img)
    imglink = f"https://telegra.ph{url_s[0]}"
    doit = f"https://some-random-api.ml/canvas/gay?avatar={imglink}"
    r = requests.get(doit)
    open("geys.png", "wb").write(r.content)
    lolbruh = "geys.png"
    await event.client.send_file(
        event.chat_id, lolbruh, caption="`You Gey.`", reply_to=owo
    )
    await hell.delete()
    for files in (lolbruh, img):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="pix$")
async def _(event):
    hell = await eor(event, "`Pixing This Image.`")
    owo = await event.get_reply_message()
    img = await convert_to_image(event, event.client)
    url_s = upload_file(img)
    imglink = f"https://telegra.ph{url_s[0]}"
    doit = f"https://some-random-api.ml/canvas/pixelate?avatar={imglink}"
    r = requests.get(doit)
    open("pix.png", "wb").write(r.content)
    lolbruh = "pix.png"
    await event.client.send_file(
        event.chat_id, lolbruh, caption="`Pixeled This Image.`", reply_to=owo
    )
    await hell.delete()
    for files in (lolbruh, img):
        if files and os.path.exists(files):
            os.remove(files)


@hell_cmd(pattern="ytc ?(.*)")
async def _(event):
    hell = await eor(event, "`Making a youthuub comment...`")
    owo = await event.get_reply_message()
    senderr = await event.client(GetFullUserRequest(owo.sender_id))
    if not senderr.profile_photo:
        imglink = 'https://telegra.ph/file/93e181ec03a3761a63918.jpg'
    elif senderr.profile_photo:
        img = await event.client.download_media(senderr.profile_photo, dwllpath)
        url_s = upload_file(img)
        imglink = f"https://telegra.ph{url_s[0]}"
    first_name = html.escape(senderr.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    xyz = event.text[5:]
    comment = owo.raw_text or xyz
    doit = f"https://some-random-api.ml/canvas/youtube-comment?avatar={imglink}&username={first_name}&comment={comment}"
    r = requests.get(doit)
    open("ytc.png", "wb").write(r.content)
    lolbruh = "ytc.png"
    await hell.delete()
    await event.client.send_file(event.chat_id, lolbruh, reply_to=owo)
    for files in (lolbruh, img):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("img_memes").add_command(
  "ytc", "<reply to a msg>", "Makes a fake youtube comment."
).add_command(
  "pix", "<reply to a img>", "Pixilates the replied image."
).add_command(
  "geyy", "<reply to a img>", "Makes the replied image gey."
).add_command(
  "trigger", "<reply to a img>", "Makes a triggered gif of replied image."
).add_command(
  "thug", "<reply to a img>", "Adds a thug life glasses and cigar to face detected in replied image."
).add_info(
  "Come let's do some komedy"
).add_warning(
  "✅ Harmless Module."
).add()
