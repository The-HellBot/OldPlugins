import os

import requests
from PIL import Image
from TelethonHell.plugins import *


@hell_cmd(pattern="rmbg(?:\s|$)([\s\S]*)")
async def _(event):
    if Config.REMOVE_BG_API is None:
        return await parse_error(event, "`REMOVE_BG_API` __is not configured.__", False)
    lists = event.text.split(" ", 2)
    flag = None
    url = None
    if len(lists) == 3:
        flag = lists[1].strip()
        url = lists[2].strip()
    elif len(lists) == 2:
        stripped = lists[1].strip()
        if stripped.startswith("-s"):
            flag = stripped
        else:
            url = stripped
    _, _, hell_memtion = await client_id(event)
    reply = await event.get_reply_message()
    if reply:
        hell = await eor(event, "`Analysing...`")
        file_name = "rmbg.png"
        try:
            await event.client.download_media(reply, file_name)
        except Exception as e:
            return await parse_error(hell, e)
        else:
            await hell.edit("`Removing background of this media`")
            file_name = toimage(file_name, "temp.jpeg")
            response = ReTrieveFile(file_name)
            os.remove(file_name)
    elif url:
        hell = await eor(event, "`Removing Background of this media`")
        response = ReTrieveURL(url)
    else:
        return await eod(event, f"Reply to a image/sticker with `{hl}rmbg` or give image link to remove background.")
    contentType = response.headers.get("content-type")
    remove_bg_image = "HellBot.png"
    if "image" in contentType:
        with open("HellBot.png", "wb") as removed_bg_file:
            removed_bg_file.write(response.content)
    else:
        return await parse_error(hell, response.content.decode('UTF-8'))
    if flag and flag == "-s":
        file = tosticker(remove_bg_image, filename="HellBot.webp")
        await event.client.send_file(
            event.chat_id,
            file,
            reply_to=reply,
        )
        await event.client.send_file(
            event.chat_id,
            file,
            caption=f"**Background removed by** {hell_memtion}",
            force_document=True,
        )
    else:
        file = remove_bg_image
        await event.client.send_file(
            event.chat_id,
            file,
            caption=f"**Background removed by** {hell_memtion}",
            force_document=True,
        )
    await hell.delete()
    os.remove(file)


def ReTrieveFile(input_file_name):
    headers = {"X-API-Key": Config.REMOVE_BG_API}
    files = {"image_file": (input_file_name, open(input_file_name, "rb"))}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


def ReTrieveURL(input_url):
    headers = {"X-API-Key": Config.REMOVE_BG_API}
    data = {"image_url": input_url}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )


def tosticker(response, filename=None):
    filename = filename or os.path.join("./temp/", "temp.webp")
    image = Image.open(response)
    if image.mode != "RGB":
        image.convert("RGB")
    image.save(filename, "webp")
    os.remove(response)
    return filename


def toimage(image, filename=None):
    filename = filename or os.path.join("./temp/", "temp.jpg")
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filename, "jpeg")
    os.remove(image)
    return filename


CmdHelp("removebg").add_command(
    "rmbg", "<flag> <reply to image/stcr or url>", "`Removes Background of replied image or sticker or given url of picture. Need` REMOVE_BG_API `to be set in Heroku Config Vars.", "rmbg -s <reply to img/url>"
).add_info(
    "Remove Background."
).add_extra(
    "🚩 Flags", "-s = output as sticker"
).add_warning(
    "✅ Harmless Module."
).add()
