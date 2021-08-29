import asyncio
import os
from shutil import rmtree
import datetime
import wikipedia
import requests
from bs4 import BeautifulSoup
from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError as GoglError
from geopy.geocoders import Nominatim
from telethon.tl import types

from . import *

def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


@bot.on(hell_cmd(pattern="wikipedia (.*)"))
@bot.on(sudo_cmd(pattern="wikipedia (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await edit_or_reply(event, "Processing ...")
    input_str = event.pattern_match.group(1)
    result = ""
    results = wikipedia.search(input_str)
    for s in results:
        page = wikipedia.page(s)
        url = page.url
        result += f"> [{s}]({url}) \n"
    await edit_or_reply(event, "WikiPedia **Search**: {} \n\n **Result**: \n\n{}".format(input_str, result)
    )


@bot.on(hell_cmd(pattern="google (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="google (.*)", allow_sudo=True))
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
        output += f" 👉🏻  [{text}]({url})\n`{des}`\n\n"
    res = f"**Google Search Query:**\n`{input_str}`\n\n**Results:**\n{output}"
    see = []
    for i in range(0, len(res), 4095):
        see.append(res[i : i + 4095])
    for j in see:
        await bot.send_message(event.chat_id, j, link_preview=False)
    await hell.delete()
    see.clear()


@bot.on(hell_cmd(pattern="img (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="img (.*)", allow_sudo=True))
async def img(event):
    sim = event.pattern_match.group(1)
    if not sim:
        return await eod(event, "`Give something to search...`")
    hell = await eor(event, f"Searching for  `{sim}`...")
    if "-" in sim:
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


@bot.on(hell_cmd(pattern="reverse"))
@bot.on(sudo_cmd(pattern="reverse", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.datetime.now()
    BASE_URL = "http://www.google.com"
    OUTPUT_STR = "Reply to an image to do Google Reverse Search"
    if event.reply_to_msg_id:
        hell = await eor(event, "Pre Processing Media")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        if previous_message.media:
            downloaded_file_name = await bot.download_media(
                previous_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(downloaded_file_name, "rb"),
                ),
                "image_content": "",
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await hell.edit("Found Google Result. Processing results...")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = BASE_URL + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        # document.getElementById("jHnbRc")
        img_size_div = soup.find(id="jHnbRc")
        img_size = img_size_div.find_all("div")
        end = datetime.datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """Possible Related Search : <a href="{prs_url}">{prs_text}</a>

More Info: Open this <a href="{the_location}">Link</a> in {ms} seconds""".format(
            **locals()
        )
    await hell.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)


@bot.on(hell_cmd(pattern="gps ?(.*)"))
@bot.on(sudo_cmd(pattern="gps ?(.*)", allow_sudo=True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await eod(event, "What should i find? Give me location.🤨")
        
    await edit_or_reply(event, "Finding😁")

    geolocator = Nominatim(user_agent="hellbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await event.delete()
    else:
        await eod(event, "I coudn't find it😫")


CmdHelp("google").add_command(
  "google", "<query>", "Does a google search for the query provided"
).add_command(
  "img", "<query>", "Does a image search for the query provided"
).add_command(
  "reverse", "<reply to a sticker/pic>", "Does a reverse image search on google and provides the similar images"
).add_command(
  "gps", "<place>", "Gives the location of the given place/city/state."
).add_command(
  "wikipedia", "<query>", "Searches for the query on Wikipedia."
).add_info(
  "Google Search."
).add_warning(
  "✅ Harmless Module."
).add()
