import cv2
import math
import numpy as np
import os
import sys

from vcam import vcam, meshGen

from . import *

if not os.path.isdir("./hellbot/"):
    os.makedirs("./hellbot/")


@hell_cmd(pattern="feye$")
async def fun(event):
    path = "omk"
    hell = await eor(event, "Editing In Progress...")
    reply = await event.get_reply_message()
    lol = await event.client.download_media(reply.media, path)
    file_name = "fishy.jpg"
    hehe = path + "/" + file_name
    img = cv2.imread(lol)
    H,W = img.shape[:2]
    fps = 30
    c1 = vcam(H=H,W=W)
    plane = meshGen(H,W)
    plane.Z -= 100*np.sqrt((plane.X*1.0/plane.W)**2+(plane.Y*1.0/plane.H)**2)
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x,map_y = c1.getMaps(pts2d)
    output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR,borderMode=0)
    output = cv2.flip(output,1)
    out1 = cv2.resize(output,(700,350))
    cv2.imwrite(file_name,out1)
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
    H,W = img.shape[:2]
    fps = 30
    c1 = vcam(H=H,W=W)
    plane = meshGen(H,W)
    plane.Z += 20*np.exp(-0.5*((plane.Y*1.0/plane.H)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x,map_y = c1.getMaps(pts2d)
    output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR,borderMode=0)
    output = cv2.flip(output,1)
    out1 = cv2.resize(output,(700,350))
    cv2.imwrite(file_name,out1)
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
    H,W = img.shape[:2]
    fps = 30
    c1 = vcam(H=H,W=W)
    plane = meshGen(H,W)
    plane.Z += 20*np.exp(-0.5*((plane.X*1.0/plane.W)/0.1)**2)/(0.1*np.sqrt(2*np.pi))
    pts3d = plane.getPlane()
    pts2d = c1.project(pts3d)
    map_x,map_y = c1.getMaps(pts2d)
    output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR,borderMode=0)
    output = cv2.flip(output,1)
    out1 = cv2.resize(output,(700,350))
    cv2.imwrite(file_name,out1)
    await event.client.send_file(event.chat_id, file_name)
    await hell.delete()
    for files in (hehe, lol):
        if files and os.path.exists(files):
            os.remove(files)


CmdHelp("imgedits").add_command(
  "feye", "<reply to a img/stcr>", "Edits the replied image or sticker to a 3-D Box like image."
).add_command(
  "warp", "<reply to a img/stcr>", "Edits the replied image or sticker to a funny image. `#Must_Try` !!"
).add_command(
  "distort", "<reply to a img/stcr>", "Edits the replied image or sticker to a funny image. `#Must_Try` !!"
).add_info(
  "Funs are here boiz"
).add_warning(
  "✅ Harmless Module."
).add()
