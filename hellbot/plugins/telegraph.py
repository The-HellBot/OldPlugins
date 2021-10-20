import os
import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from . import *


@hell_cmd(pattern="t(m|t) ?(.*)")
async def _(event):
    if Config.LOGGER_ID is None:
        await eod(event, "You need to setup `LOGGER_ID` to use telegraph...")
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    telegraph = Telegraph()
    optional_title = event.text[4:]
    hell = await eor(event, "Making Telegraph Link....")
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.text[2:3]
        if input_str == "m":
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await hell.edit(f"Downloaded to  `{downloaded_file_name}`  in  `{ms}`  seconds. \nMaking Telegraph Link.....")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await eod(hell, "ERROR: " + str(exc), 8)
                os.remove(downloaded_file_name)
            else:
                end = datetime.datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await hell.edit("✓ **[File uploaded to telegraph](https://telegra.ph{})** \n✓ **Time Taken :-** `{}` secs \n✓ **By :- {}** \n✓  `https://telegra.ph{}`".format(
                        media_urls[0], (ms + ms_two), hell_mention, media_urls[0],
                    ),
                    link_preview=True,
                )
        elif input_str == "t":
            user_object = await event.client.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await event.client.download_media(
                    r_message, Config.TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.datetime.now()
            ms = (end - start).seconds
            hellboy = f"https://telegra.ph/{response['path']}"
            await hell.edit(f"✓ **[Pasted to telegraph]({hellboy})** \n✓ **Time Taken :-** `{ms}` secs\n✓** By :**  {hell_mention} \n✓  `{hellboy}`", link_preview=True)
    else:
        await eod(hell, "Reply to a message to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CmdHelp("telegraph").add_command(
  "tt", "<reply to text message>", "Uploads the replied text message to telegraph making a short telegraph link"
).add_command(
  "tm", "<reply to media>", "Uploads the replied media (sticker/ gif/ video/ image) to telegraph and gives a short telegraph link"
).add_info(
  "Make Telegraph Links."
).add_warning(
  "✅ Harmless Module."
).add()
