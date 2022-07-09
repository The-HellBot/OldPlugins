import os
import re

from TelethonHell.clients.instaAPI import InstaGram

insta_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel|s|stories)\/.+\/?"


async def IGDL(event, url):
    dl_path = "./insta/dl"
    if not os.path.isdir(dl_path):
        os.makedirs(dl_path)
    type = url.split("/")[3]

    if type == "p":
        try:
            pk = InstaGram.media_pk_from_url(url)
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        try:
            info = InstaGram.media_info(pk).dict()
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        if info['media_type'] == 8:
            try:
                file = InstaGram.album_download(pk, folder=dl_path)
            except Exception as e:
                os.remove(dl_path)
                return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        elif info['media_type'] == 1:
            try:
                file = InstaGram.photo_download(pk, folder=dl_path)
            except Exception as e:
                os.remove(dl_path)
                return await eod(hell, f"**ERROR !!** \n\n`{e}`")

        elif info['media_type'] == 2 and info['product_type'] == "feed":
            try:
                file = InstaGram.video_download(pk, folder=dl_path)
            except Exception as e:
                os.remove(dl_path)
                return await eod(hell, f"**ERROR !!** \n\n`{e}`")

    elif type == "tv":
        try:
            pk = InstaGram.media_pk_from_url(url)
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")
        try:
            file = InstaGram.igtv_download(pk, folder=dl_path)
        except Exception as e:
            os.remove(dl_path)
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

    elif type == "reel":
        try:
            pk = InstaGram.media_pk_from_url(url)
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")
        try:
            file = InstaGram.clip_download(pk, folder=dl_path)
        except Exception as e:
            os.remove(dl_path)
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")
    
    elif type == "stories":
        try:
            pk = InstaGram.story_pk_from_url(url)
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")
        try:
            file = InstaGram.story_download(pk, folder=dl_path)
        except Exception as e:
            os.remove(dl_path)
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")

    elif type == "s" and "story_media_id" in url:
        try:
            pk = InstaGram.media_pk_from_url(url)
        except Exception as e:
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")
        try:
            file = InstaGram.story_download(pk, folder=dl_path)
        except Exception as e:
            os.remove(dl_path)
            return await eod(hell, f"**ERROR !!** \n\n`{e}`")


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
