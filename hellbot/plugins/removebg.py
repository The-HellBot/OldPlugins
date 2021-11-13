import os
import requests

from PIL import Image

from . import *


@hell_cmd(pattern="rmbg(?:\s|$)([\s\S]*)")
async def _(event):
    if Config.REMOVE_BG_API is None:
        return await eod(event, "You need to set  `REMOVE_BG_API`  for this module to work...")
    txt = event.text[6:]
    try:
        input_str = txt.replace("-s", "")
    except:
        input_str = txt
    flag = event.text[-2:]
    cid = await client_id(event)
    hell_memtion = cid[2]
    if event.reply_to_msg_id and input_str == "":
        reply_message = await event.get_reply_message()
        hell = await eor(event, "`Analysing...`")
        file_name = "./remove_bg/rmbg.png"
        try:
            await event.client.download_media(reply_message, file_name)
        except Exception as e:
            await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
            return
        else:
            await hell.edit("`Removing background of this media`")
            file_name = toimage(file_name)
            response = ReTrieveFile(file_name)
            os.remove(file_name)
    elif input_str:
        hell = await eor(event, "`Removing Background of this media`")
        response = ReTrieveURL(input_str)
    else:
        await eod(event, f"Reply to a image/sticker with `{hl}rmbg` or give image link to remove background.")
        return
    contentType = response.headers.get("content-type")
    remove_bg_image = "HellBot.png"
    if "image" in contentType:
        with open("HellBot.png", "wb") as removed_bg_file:
            removed_bg_file.write(response.content)
    else:
        await eod(hell, f"`{response.content.decode('UTF-8')}`")
        return
    if flag and flag == "-s":
        file = tosticker(remove_bg_image, filename="HellBot.webp")
        await event.client.send_file(
            event.chat_id,
            file,
            reply_to=reply_message,
        )
    else:
        file = remove_bg_image
        await event.client.send_file(
            event.chat_id,
            file,
            force_document=False,
            reply_to=reply_message,
        )
    file = remove_bg_image
    await event.client.send_file(
        event.chat_id,
        file,
        caption=f"**Background removed by** {hell_memtion}",
        force_document=True,
        )
    await hell.delete()


def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REMOVE_BG_API,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REMOVE_BG_API,
    }
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
  "rmbg", "<reply to image/stcr> or <link> <flag>", "`Removes Background of replied image or sticker. Need` REMOVE_BG_API `to be set in Heroku Config Vars.", "rmbg <reply to img> -s"
).add_info(
  "Remove Background. \n**🚩 Flags :** -s = output as sticker"
).add_warning(
  "✅ Harmless Module."
).add()
