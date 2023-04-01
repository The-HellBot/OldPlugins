import os
import requests

from TelethonHell.plugins import *


@hell_cmd(pattern="wallpaper(?:\s|$)([\s\S]*)")
async def wallpaper(event):
    _lists = event.text.split(" ", 1)
    if len(_lists) == 1:
        return await parse_error(event, "Give some text to search wallpapers.")
    lists = (_lists[1]).split(";")
    limit = 5 if len(lists) == 1 else int(lists[1])
    query = lists[0]
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
    await event.client.send_file(event.chat_id, wall_list, caption=query, album=True)
    for i in wall_list:
        os.remove(i)
