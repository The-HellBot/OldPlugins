from . import *


@hell_cmd(pattern="insta(?:\s|$)([\s\S]*)")
async def download(event):
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
    url = event.text[7:]
    is_video = None
    hell = await eor(event, "Downloading IG post...")
    if "instagram.com" in url:
        url_code = url.split("/")[4]
        url = f"https://instagram.com/p/{url_code}?__a=1"
        try:
            visit = requests.get(url).json()
            is_video = visit['graphql']['shortcode_media']['is_video']
        except:
            return await eod(hell, "Only public instagram posts are allowed.")
        
        if is_video == True:
            try:
                video_url = visit['graphql']['shortcode_media']['video_url']
                await event.client.send_file(event.chat_id, file=video_url, caption=f"📥 InstaGram Video Downloaded By :- {hell_mention}")
                await hell.delete()
            except Exception as e:
                LOGS.info(str(e))

        elif is_video == False:
            try:
                post_url = visit['graphql']['shortcode_media']['display_url']
                await event.client.send_file(event.chat_id, file=post_url, caption=f"📥 InstaGram Post Downloaded By :- {hell_mention}")
                await hell.delete()
            except Exception as e:
                LOGS.info(str(e))
        else:
            await eod(hell, "Only public instagram posts are allowed.")
    else:
        await eod(hell, "Only public instagram posts are allowed.")


CmdHelp("instagram").add_command(
    "insta", "<link>", "Downloads the provided instagram video/pic from link.", "insta www.instagram.com/yeuehiwnwiqo"
).add_info(
    "Insta Downloader."
).add_warning(
    "✅ Harmless Module"
).add()
