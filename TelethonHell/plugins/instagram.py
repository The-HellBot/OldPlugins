"""
TODO:
1. instagram story downloader - igdl -s <link>
2. recent 10 feed - .igdl -feed
3. hashtag's top 10 posts download - .igdl -ht <hashtag>
"""
import os
import re

from . import *


@hell_cmd(pattern="igdl(?:\s|$)([\s\S]*)")
async def download(event):
    flag, url = await get_flag(event)
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "IG downloader in action...")
    
    if flag.lower() in ["-post", "-story"]:
        result = re.search(insta_regex, url)
        if not result:
            return await eod(hell, "Need a instagram post/story link to download!")
        try:
            file, caption = await IGDL(event, result.group(0))
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        items_list = os.listdir("./insta/dl")
        count = 0
        if items_list != []:
            for i in items_list:
                file = open(f"./insta/dl/{i}", "rb")
                await event.client.send_message(
                    event.chat_id, 
                    file=file, 
                    message=f"📥 InstaGram Post Downloaded By :- {hell_mention}",
                )
                os.remove(f"./insta/dl/{i}")
                count += 1
            await eod(hell, f"**Downloaded Instagram Post!** \n\n__Total:__ `{count} posts.`")
        else:
            await hell.edit(f"Unable to upload video! Setup `INSTAGRAM_PASSWORD` & `INSTAGRAM_USERNAME` for better functionality.")

    elif flag.lower() == "-feed":
        await eod(hell, "soon")
        #### Recent 10 posts from feed
    elif flag.lower() == "-htag":
        await eod(hell, "soon")
        #### top 10 posts of hashtag
    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    

@hell_cmd(pattern="igup(?:\s|$)([\s\S]*)")
async def download(event):
    flag, url = await get_flag(event)
    hell = await eor(event, "IG uploader in action...")
    reply = await event.get_reply_message()
    caption = reply.message or "#Uploaded By HellBot"
    HELL_MEDIA = media_type(reply)

    try:
        IG = await InstaGram(event)
    except Exception as e:
        return await eod(hell, f"**ERROR:** \n\n`{str(e)}`")

    if not reply:
        return await eod(hell, "Reply to a media to upload on instagram.")
    if not reply.media:
        return await eod(hell, "Reply to a media to upload on instagram.")

    if flag.lower() == "-reel":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "A reel can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading reel to instagram...")
        try:
            video = IG.clip_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
        await hell.edit(f"**Uploaded Reel to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)
    
    elif flag.lower() == "-tv":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "An IGTV can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading IGTV to instagram...")
        try:
            video = IG.igtv_upload(path=file, title=caption, caption=caption)
        except Exception as e:
            os.remove(file)
            return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
        await hell.edit(f"**Uploaded IGTV to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)
    
    elif flag.lower() == "-vid":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "A video post can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading Video to instagram...")
        try:
            video = IG.video_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
        await hell.edit(f"**Uploaded Video to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)

    elif flag.lower() == "-pic":
        if HELL_MEDIA != "Photo":
            return await eod(hell, "A picture post can only be a Photo!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading Photo to instagram...")
        try:
            video = IG.photo_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
        await hell.edit(f"**Uploaded Photo to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)

    elif flag.lower() == "-story":
        if HELL_MEDIA in ["Gif", "Video"]:
            file = await event.client.download_media(reply)
            await hell.edit("**Downloaded!** \n\nNow uploading Story to instagram...")
            try:
                video = IG.video_upload_to_story(path=file, caption=caption)
            except Exception as e:
                os.remove(file)
                return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
            await hell.edit(f"**Uploaded Story to Instagram!** \n\n[See Story From Here](https://instagram.com/p/{video.code})", link_preview=False)
            os.remove(file)

        elif HELL_MEDIA == "Photo":
            file = await event.client.download_media(reply)
            await hell.edit("**Downloaded!** \n\nNow uploading Story to instagram...")
            try:
                video = IG.photo_upload_to_story(path=file, caption=caption)
            except Exception as e:
                os.remove(file)
                return await eod(hell, f"**ERROR !!** \n\n`{str(e)}`")
            await hell.edit(f"**Uploaded Story to Instagram!** \n\n[See Story From Here](https://instagram.com/p/{video.code})", link_preview=False)
            os.remove(file)
        
        else:
            return await eod(hell, "Invalid media format. Only Videos, Pictures, GIF are supported to upload story.")

    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    


CmdHelp("instagram").add_command(
    "igdl", "<flag> <link>", "Download posts/reels/stories from Instagram. Requires INSTAGRAM_SESSION to work."
).add_command(
    "igup", "<flag> <reply>", "Upload replied media on Instagram with caption from Telegram."
).add_extra(
    "🚩 Flags [igdl]", "-post, -story, -feed, -htag"
).add_extra(
    "🚩 Flags [igup]", "-reel, -tv, -vid, -pic, -story"
).add_info(
    "Instagram API for Telegram."
).add_warning(
    "✅ Harmless Module"
).add()
