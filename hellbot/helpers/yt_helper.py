import json
import os

from youtube_search import YoutubeSearch

from hellbot.utils.extras import delete_hell as eod


# Gets yt link of given query.
async def song_search(event, query, max_results, details=False):
    try:
        results = json.loads(YoutubeSearch(query, max_results=max_results).to_json())
    except KeyError:
        return await eod(event, "Unable to find relevant search query.")
    x = ""
    for i in results["videos"]:
        x += f"https://www.youtube.com{i['url_suffix']}\n"
        if details:
            title = f"{i['title']}"
            views = f"{i['views']}"
            duration = f"{i['duration']}"
            thumb = f"{i['thumbnails'][0]}"
            return x, title, views, duration, thumb
    return x


song_opts = {
    "format": "bestaudio",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "age_limit": 25,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }
    ],
    "outtmpl": "%(id)s.mp3",
    "quiet": True,
    "logtostderr": False,
}


video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "age_limit": 25,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
    ],
    "outtmpl": "%(id)s.mp4",
    "logtostderr": False,
    "quiet": True,
}
