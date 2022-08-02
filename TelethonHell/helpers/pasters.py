import json

import requests
from html_telegraph_poster import TelegraphPoster

from TelethonHell import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}


async def pasty(event, message, extension=None):
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        try:
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#PASTE \n\n**Open Paste From** [here]({purl}). \n**Delete that paste by using this token** `{response['deletionToken']}`",
            )
        except Exception as e:
            LOGS.info(str(e))
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}


async def space_paste(message, extension=None):
    site = "https://spaceb.in/api/v1/documents/"
    if extension is None:
        extension == "txt"
    try:
        response = requests.post(
            site, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{site}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": "Unable to reach spacebin."}


async def telegraph_paste(page_title, temxt, auth="[ †he Hêllẞø† ]", url="https://t.me/its_hellbot"):
    cl1ent = TelegraphPoster(use_api=True)
    cl1ent.create_api_token(auth)
    post_page = cl1ent.post(
        title=page_title,
        author=auth,
        author_url=url,
        text=temxt,
    )
    return post_page["url"]
