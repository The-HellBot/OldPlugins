"""
TODO:
1. instagram post downloader (reel/igtv/post) - .igdl -p <link>
2. instagram story downloader - igdl -s <link>
3. recent 10 feed - .igdl -feed
4. hashtag's top 10 posts download - .igdl -ht <hashtag>
5. upload video/pic in instagram - .igup -reel <reply>
6. upload stories in instagram - .igup -s <reply>
"""
import os
import re

from . import *


@hell_cmd(pattern="igdl(?:\s|$)([\s\S]*)")
async def download(event):
    flag, url = await get_flag(event)
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "IG downloader in action...")
    
    if flag.lower() in ["-p", "-s"]:
        result = re.search(insta_regex, url)
        if not result:
            return await eod(hell, "Need a instagram post/story link to download!")
        try:
            file, caption = await IGDL(event, result.group(0))
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        items_list = os.listdir("./insta/dl")
        if items_list != []:
            for i in items_list:
                file = open(f"./insta/dl/{i}", "rb")
                await event.client.send_message(
                    event.chat_id, 
                    file=file, 
                    message=f"📥 InstaGram Post Downloaded By :- {hell_mention}",
                )
                os.remove(f"./insta/dl/{i}")
        else:
            await hell.edit(f"Unable to upload video! Setup `INSTAGRAM_PASSWORD` & `INSTAGRAM_USERNAME` for better functionality.")

    elif flag.lower() == "-feed":
        await eod(hell, "soon")
        #### Recent 10 posts from feed
    elif flag.lower() == "-ht":
        await eod(hell, "soon")
        #### top 10 posts of hashtag
    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    

@hell_cmd(pattern="igup(?:\s|$)([\s\S]*)")
async def download(event):
    flag, url = await get_flag(event)
    hell = await eor(event, "IG uploader in action...")
    reply = await event.get_reply_message()
    IG = await InstaGram(event)

    if not reply:
        return await eod(hell, "Reply to a media to upload on instagram.")
    if not reply.media:
        return await eod(hell, "Reply to a media to upload on instagram.")
    
    HELL_MEDIA = media_type(reply)
    if HELL_MEDIA not in ["Photo", "Gif", "Video"]:
        return await eod(hell, "Reply to a media to upload on instagram.")

    if flag.lower() == "-reel":
        caption = event.message.message or "#Uploaded By HellBot"
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading to instagram...")
        try:
            video = IG.clip_upload(file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
        await hell.edit(f"**Uploaded to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)

    elif flag.lower() == "-s":
        await eod(hell, "soon")
        #### instagram story upload from tg

    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    


CmdHelp("instagram").add_command(
    "igdl", "<flag> <link>", "Instagram posts downloader based on flags."
).add_command(
    "igup", "<flag> <reply>", "Upload posts on Instagram from Telegram. Replied video/pic is uploaded with caption."
).add_extra(
    "🚩 Flags", "-p, -s, -feed(igdl only), -ht(igdl only), -reel(igup only)"
).add_info(
    "Instagram API for Telegram."
).add_warning(
    "✅ Harmless Module"
).add()
