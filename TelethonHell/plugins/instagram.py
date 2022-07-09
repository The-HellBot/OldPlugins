import re

from . import *


@hell_cmd(pattern="insta(?:\s|$)([\s\S]*)")
async def download(event):
    insta_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel)\/.+\/?"
    ForGo10God, HELL_USER, hell_mention = await client_id(event)
    url = event.text[7:]
    is_video = None
    result = re.search(insta_regex, url)
    hell = await eor(event, "Downloading IG post...")
    
    if not result:
        return await eod(hell, "Need a instagram post link to download!")
    
    try:
        video = InstaGram.VideoURL(result.group(0))
    except LoginError as e:
        return await eod(hell, f"**ERROR !!** \n\n`{e}`")
        
    if video is not None:
        await event.client.send_file(
            event.chat_id,
            file=video,
            caption=f"📥 InstaGram Post Downloaded By :- {hell_mention}",
        )
    else:
        await hell.edit(f"Unable to upload video! \n\nOUTPUT: {video}")
 

CmdHelp("instagram").add_command(
    "insta", "<link>", "Downloads the provided instagram video/pic from link.", "insta www.instagram.com/yeuehiwnwiqo"
).add_info(
    "Insta Downloader."
).add_warning(
    "✅ Harmless Module"
).add()
