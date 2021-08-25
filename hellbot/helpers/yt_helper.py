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
