import os
import requests

from shutil import rmtree
from TelethonHell.plugins import *


@hell_cmd(pattern="img(?:\s|$)([\s\S]*)")
async def img(event):
    sim = event.pattern_match.group(1)
    if not sim:
        return await parse_error(event, "Nothing given to search.")
    hell = await eor(event, f"Searching for `{sim}`...")
    if ";" in sim:
        try:
            lim = int(sim.split(";")[1])
            sim = sim.split(";")[0]
        except BaseException:
            lim = 5
    else:
        lim = 5
    imgs = googleimagesdownload()
    args = {
        "keywords": sim,
        "limit": lim,
        "format": "jpg",
        "output_directory": "./DOWNLOADS/",
    }
    letsgo = imgs.download(args)
    gotit = letsgo[0][sim]
    await event.client.send_file(event.chat_id, gotit, caption=sim, album=True)
    rmtree(f"./DOWNLOADS/{sim}/")
    await hell.delete()


@hell_cmd(pattern="wallpaper(?:\s|$)([\s\S]*)")
async def wallpaper(event):
    _lists = event.text.split(" ", 1)
    if len(_lists) == 1:
        return await parse_error(event, "Give some text to search wallpapers.")
    lists = (_lists[1]).split(";")
    limit = 5 if len(lists) == 1 else int(lists[1].strip())
    query = lists[0].strip()
    hell = await eor(event, "`Processing...`")
    _wall = await unsplash(query, limit)
    if not _wall:
        return await parse_error(hell, "No wallpapers found.")
    x = 0
    wall_list = []
    for i in _wall:
        bg = requests.get(i)
        with open(f"wallpaper{x}.jpg", "wb") as file:
            file.write(bg.content)
        wall_list.append(f"wallpaper{x}.jpg")
        x += 1
    await event.client.send_file(event.chat_id, wall_list, caption=query, album=True, force_document=True)
    await hell.delete()
    for i in wall_list:
        os.remove(i)


CmdHelp("image").add_command(
    "img", "<text>;<limit>", "Searches for images on google and sends the images.", "img car;5"
).add_command(
    "wallpaper", "<text>;<limit>", "Searches for wallpapers on unsplash and sends the wallpapers.", "wallpaper car;5"
).add_info(
    "Image Searcher."
).add_warning(
    "✅ Harmless Module."
).add()