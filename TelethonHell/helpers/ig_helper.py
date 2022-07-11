import os
import re

from TelethonHell import LOGS
from TelethonHell.clients.instaAPI import InstaGram

insta_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel|s|stories)\/.+\/?"


async def IGDL(event, url):
    dl_path = "./insta/dl"
    if not os.path.isdir(dl_path):
        os.makedirs(dl_path)
    
    caption, file = None, None
    type = url.split("/")[3]
    IG = await InstaGram(event)
    if not IG:
        return await event.edit("INSTAGRAM_SESSION not configured or Expired !")
    try:
        pk = IG.media_pk_from_url(url)
        info = IG.media_info(pk).dict()
    except Exception as e:
        LOGS.info(str(e))
        return file, caption

    if type == "p":
        if info['media_type'] == 8:
            try:
                file = IG.album_download(pk, folder=dl_path)
            except Exception as e:
                LOGS.info(str(e))
                file = None

        elif info['media_type'] == 1:
            try:
                file = IG.photo_download(pk, folder=dl_path)
            except Exception as e:
                LOGS.info(str(e))
                file = None

        elif info['media_type'] == 2 and info['product_type'] == "feed":
            try:
                file = IG.video_download(pk, folder=dl_path)
            except Exception as e:
                LOGS.info(str(e))
                file = None

    elif type == "tv":
        try:
            file = IG.igtv_download(pk, folder=dl_path)
        except Exception as e:
            LOGS.info(str(e))
            file = None

    elif type == "reel":
        try:
            file = IG.clip_download(pk, folder=dl_path)
        except Exception as e:
            LOGS.info(str(e))
            file = None
    
    elif type == "stories":
        try:
            file = IG.story_download(pk, folder=dl_path)
        except Exception as e:
            LOGS.info(str(e))
            file = None

    elif type == "s" and "story_media_id" in url:
        try:
            file = IG.story_download(pk, folder=dl_path)
        except Exception as e:
            LOGS.info(str(e))
            file = None
    
    if info["caption_text"]:
        caption = info["caption_text"]
        
    return file, caption


async def get_flag(event):
    dicts = event.text.split(" ", 2)
    if len(dicts) == 3:
        flag = dicts[1]
        url = dicts[2]
        return flag, url
    elif len(dicts) == 2:
        flag = dicts[1]
        url = None
        return flag, url
    else:
        flag = None
        url = None
        return flag, url

# hellbot
