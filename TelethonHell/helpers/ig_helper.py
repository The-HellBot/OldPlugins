import os

from TelethonHell.clients.instaAPI import InstaGram
from TelethonHell.clients.logger import LOGGER as LOGS

insta_regex = r"(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|tv|reel|s|stories)\/.+\/?"


async def IGDL(event, url):
    dl_path = "./insta/dl"
    if not os.path.isdir(dl_path):
        os.makedirs(dl_path)
    
    caption, file = None, None
    type = url.split("/")[3]
    IG = await InstaGram(event)
    if not IG:
        await event.edit("INSTAGRAM_SESSION not configured or Expired !")
        return file, caption
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
            spk = IG.story_pk_from_url(url)
            info =  IG.story_info(pk).dict()
            if info['video_url']:
                file = IG.story_download_by_url(info['video_url'], folder=dl_path)
            elif info['thumbnail_url']:
                file = IG.story_download_by_url(info['thumbnail_url'], folder=dl_path)
            else:
                file = None
        except Exception as e:
            LOGS.info(str(e))
            file = None

    elif type == "s" and "story_media_id" in url:
        try:
            spk = IG.story_pk_from_url(url)
            info =  IG.story_info(pk).dict()
            if info['video_url']:
                file = IG.story_download_by_url(info['video_url'], folder=dl_path)
            elif info['thumbnail_url']:
                file = IG.story_download_by_url(info['thumbnail_url'], folder=dl_path)
            else:
                file = None
        except Exception as e:
            LOGS.info(str(e))
            file = None
    
    if info["caption_text"]:
        caption = info["caption_text"]
        
    return file, caption


async def Htag_Dict(event, client, hashtag, count):
    pk_dict = {}

    try:
        medias = client.hashtag_medias_top(hashtag, count)
        for media in medias:
            info = media.dict()
            pk = info['pk']
            mtype = info['media_type']
            product = info['product_type']
            pk_dict[pk] = [mtype, product]
    except Exception as e:
        LOGS.info(str(e))

    return pk_dict


async def IG_Htag_DL(event, hashtag, count):
    dl_path = "./insta/dl"
    if not os.path.isdir(dl_path):
        os.makedirs(dl_path)

    IG = await InstaGram(event)
    if IG:
        pk_dict = await Htag_Dict(event, IG, hashtag, count)
        if pk_dict:
            key = list(pk_dict.keys())
            val = list(pk_dict.values())
            for i in range(len(pk_dict)):
                pk, mt, pt = key[i], val[i][0], val[i][1]
                if mt == 1:
                    try:
                        IG.photo_download(pk, folder=dl_path)
                    except Exception as e:
                        LOGS.info(str(e))
                elif mt == 2 and pt == "feed":
                    try:
                        IG.video_download(pk, folder=dl_path)
                    except Exception as e:
                        LOGS.info(str(e))
                elif mt == 2 and pt == "igtv":
                    try:
                        IG.igtv_download(pk, folder=dl_path)
                    except Exception as e:
                        LOGS.info(str(e))
                elif mt == 2 and pt == "clips":
                    try:
                        IG.clip_download(pk, folder=dl_path)
                    except Exception as e:
                        LOGS.info(str(e))
                else:
                    # Well I dont want bot to spam medias.
                    # As this statement handles album post,
                    # Meaning that post will surely contain
                    # Atleast 2 medias and Atmost 10 medias.
                    # It'll get spammy AF!!
                    pass
                


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
