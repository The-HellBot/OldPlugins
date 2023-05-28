import datetime
import io
import os
import traceback
import urllib.request
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from search_engine_parser import GoogleSearch
from search_engine_parser.core.exceptions import \
    NoResultsOrTrafficError as GoglError
from selenium import webdriver
from telethon.tl import types
from TelethonHell.plugins import *
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError


@hell_cmd(pattern="wiki(?:\s|$)([\s\S]*)")
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
        return await parse_error(event, f"__DISAMBIGUATED PAGE:__\n{result}", False)
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
            return await parse_error(event, f"__DISAMBIGUATED PAGE:__\n{result}", False)
        except PageError:
            return await eod(event, f"**Sorry i Can't find any results for **`{match}`")
    await eor(event, "**Search:**\n`" + match + "`\n\n**Result:**\n" + f"__{result}__")


@hell_cmd(pattern="google(?:\s|$)([\s\S]*)")
async def google(event):
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await parse_error(event, "Nothing given to search.")
    hell = await eor(event, "Searching...")
    gos = GoogleSearch()
    try:
        got = await gos.async_search(f"{input_str}", cache=False)
    except GoglError as e:
        return await parse_error(hell, e)
    output = ""
    for i in range(len(got["links"])):
        text = got["titles"][i]
        url = got["links"][i]
        des = got["descriptions"][i]
        output += f"<a href='{url}'>• {text}</a>\n≈ <code>{des}</code>\n\n"
    res = f"""<h3><b><i>Google Search Query:</b></i> <u>{input_str}</u></h3>

»» <b>Results:</b>
{output}"""
    paste = await telegraph_paste(f"Google Search Query “ {input_str} ”", res)
    await hell.edit(
        f"**Google Search For** `{input_str}` \n[📌 See Results Here]({paste})",
        link_preview=False,
    )


@hell_cmd(pattern="reverse(?:\s|$)([\s\S]*)")
async def _(event):
    reply = await event.get_reply_message()
    if not reply:
        return await parse_error(event, "Reply to an image or sticker.")
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
    await hell.edit(f"**Possible Results:** [{text}](google.com{link})")
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


@hell_cmd(pattern="gps(?:\s|$)([\s\S]*)")
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
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await hell.delete()
    else:
        await eod(hell, "I coudn't find it😫")


@hell_cmd(pattern="webshot ([\s\S]*)")
async def _(event):
    if Config.GOOGLE_CHROME_BIN is None:
        return await parse_error(event, "Google chrome not installed.")
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "Webshot in action...")
    start = datetime.datetime.now()
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = Config.GOOGLE_CHROME_BIN
        await hell.edit("Starting Google Chrome BIN")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        input_str = event.pattern_match.group(1)
        driver.get(input_str)
        await hell.edit("Calculating Page Dimensions")
        height = driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
        )
        width = driver.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
        )
        await hell.edit("Painting web-page")
        driver.set_window_size(width + 100, height + 100)
        im_png = driver.get_screenshot_as_png()
        driver.close()
        await hell.edit("Stopping Google Chrome BIN")
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        end = datetime.datetime.now()
        ms = (end - start).seconds
        caption = f"**Webshot Completed !!** \n\n**URL:** {input_str} \n**Time Taken:** `{ms} seconds`\n**By:** {hell_mention}"
        with io.BytesIO(im_png) as out_file:
            out_file.name = "Hell_Capture.PNG"
            await event.client.send_file(
                event.chat_id,
                out_file,
                caption=caption,
                force_document=True,
                reply_to=message_id,
                allow_cache=False,
                silent=True,
            )
            await hell.delete()
    except Exception:
        await parse_error(hell, traceback.format_exc())


@hell_cmd(pattern="cricket$")
async def _(event):
    score_page = "http://static.cricinfo.com/rss/livescores.xml"
    page = urllib.request.urlopen(score_page)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")
    final = ""
    for match in result:
        final += match.get_text() + "\n\n"
    await eor(
        event,
        f"<b><i><u>Match information gathered successful</b></i></u>\n\n<code>{final}</code>",
        parse_mode="HTML",
    )


CmdHelp("google").add_command(
    "google", "<query>", "Does a google search for the query provided", "google hellbot"
).add_command(
    "reverse", "<reply to a sticker/pic>", "Does a reverse image search on google and provides the similar images"
).add_command(
    "gps", "<place>", "Gives the location of the given place/city/state."
).add_command(
    "wiki", "<query>", "Searches for the query on Wikipedia."
).add_command(
    "webshot", "<link>", f"Gives out the web screenshot of given link via Google Crome Bin in .png format", "webshot https://github.com/hellboy-op/hellbot"
).add_command(
    "cricket", None, "Collects all the live cricket scores."
).add_info(
    "Google Search."
).add_warning(
    "✅ Harmless Module."
).add()
