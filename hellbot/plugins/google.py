import asyncio
import datetime
import os
import requests

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError as GoglError
from shutil import rmtree
from telethon.tl import types
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from . import *

def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@hell_cmd(pattern="wiki ?(.*)")
async def _(event):
    match = event.text[6:]
    result = None
    try:
        result = summary(match, auto_suggest=False)
    except DisambiguationError as error:
        error = str(error).split("\n")
        result = "".join(
            f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
            for lineno, i in enumerate(error, start=1)
        )
        return await eor(event, f"**DISAMBIGUATED PAGE !!.**\n\n{result}")
    except PageError:
        pass
    if not result:
        try:
            result = summary(match, auto_suggest=True)
        except DisambiguationError as error:
            error = str(error).split("\n")
            result = "".join(
                f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
                for lineno, i in enumerate(error, start=1)
            )
            return await eor(
                event, f"**DISAMBIGUATED PAGE !!**\n\n{result}"
            )
        except PageError:
            return await eod(
                event, f"**Sorry i Can't find any results for **`{match}`"
            )
    await eor(
        event, "**Search :**\n`" + match + "`\n\n**Result:**\n" + f"__{result}__"
    )


@hell_cmd(pattern="google ?(.*)")
async def google(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await eod(event, "`Give something to search..`")
    hell = await eor(event, "Searching...")
    gos = GoogleSearch()
    try:
        got = await gos.async_search(f"{input_str}", cache=False)
    except GoglError as e:
        return await eod(event, str(e), 10)
    output = ""
    for i in range(len(got["links"])):
        text = got["titles"][i]
        url = got["links"][i]
        des = got["descriptions"][i]
        output += f"<a href='{url}'>• {text}</a>\n≈ <code>{des}</code>\n\n"
    res = f"""<h3><b><i>Google Search Query :</b></i> <u>{input_str}</u></h3>

»» <b>Results :</b>
{output}"""
    paste = await telegraph_paste(f"Google Search Query “ {input_str} ”", res)
    await hell.edit(f"**Google Search For** `{input_str}` \n[📌 See Results Here]({paste})", link_preview=False)


@hell_cmd(pattern="img ?(.*)")
async def img(event):
    sim = event.pattern_match.group(1)
    if not sim:
        return await eod(event, "`Give something to search...`")
    hell = await eor(event, f"Searching for `{sim}`...")
    if ";" in sim:
        try:
            lim = int(sim.split(";")[1])
            sim = sim.split(";")[0]
        except BaseExceptaion:
            lim = 5
    else:
        lim = 5
    imgs = googleimagesdownload()
    args = {
        "keywords": sim,
        "limit": lim,
        "format": "jpg",
        "output_directory": "./DOWNLOADS/",
    }
    letsgo = imgs.download(args)
    gotit = letsgo[0][sim]
    await event.client.send_file(event.chat_id, gotit, caption=sim, album=True)
    rmtree(f"./DOWNLOADS/{sim}/")
    await hell.delete()


@hell_cmd(pattern="reverse ?(.*)")
async def _(event):
    reply = await event.get_reply_message()
    if not reply:
        return await eod(event, "`Reply to an Image or stciker...`")
    hell = await eor(event, "`Processing...`")
    dl = await reply.download_media()
    file = {"encoded_image": (dl, open(dl, "rb"))}
    grs = requests.post(
        "https://www.google.com/searchbyimage/upload",
        files=file,
        allow_redirects=False,
    )
    loc = grs.headers.get("Location")
    response = requests.get(
        loc,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    )
    xx = BeautifulSoup(response.text, "html.parser")
    div = xx.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    link = alls["href"]
    text = alls.text
    await hell.edit(f"**Possible Results :** [{text}](google.com{link})")
    img = googleimagesdownload()
    args = {
        "keywords": text,
        "limit": 3,
        "format": "jpg",
        "output_directory": "./DOWNLOADS/",
    }
    final = img.download(args)
    ok = final[0][text]
    await event.client.send_file(
        event.chat_id,
        ok,
        album=True,
        caption=f"Similar Images Related to {text}",
    )
    rmtree(f"./DOWNLOADS/{text}/")
    os.remove(dl)


@hell_cmd(pattern="gps ?(.*)")
async def gps(event):
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await eod(event, "What should i find? Give me location.🤨")
    hell = await eor(event, "Finding😁")
    geolocator = Nominatim(user_agent="hellbot")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)))
        await hell.delete()
    else:
        await eod(hell, "I coudn't find it😫")


CmdHelp("google").add_command(
  "google", "<query>", "Does a google search for the query provided"
).add_command(
  "img", "<query>", "Does a image search for the query provided"
).add_command(
  "reverse", "<reply to a sticker/pic>", "Does a reverse image search on google and provides the similar images"
).add_command(
  "gps", "<place>", "Gives the location of the given place/city/state."
).add_command(
  "wiki", "<query>", "Searches for the query on Wikipedia."
).add_info(
  "Google Search."
).add_warning(
  "✅ Harmless Module."
).add()
