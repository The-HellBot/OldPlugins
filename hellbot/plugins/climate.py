import io
import json
import logging
import datetime

import aiohttp
import requests
from pytz import country_names as c_n
from pytz import country_timezones as c_tz
from pytz import timezone as tz

from . import *

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)

DEFCITY = "Delhi"
OWM_API = Config.WEATHER_API

async def get_tz(con):
    for c_code in c_n:
        if con == c_n[c_code]:
            return tz(c_tz[c_code][0])
    try:
        if c_n[con]:
            return tz(c_tz[con][0])
    except KeyError:
        return


@bot.on(hell_cmd(pattern="climate ?(.*)"))
@bot.on(sudo_cmd(pattern="climate ?(.*)", allow_sudo=True))
async def get_weather(weather):
    if not OWM_API:
        await eor(weather, "**Get an API key from** https://openweathermap.org/ **first.**")
        return
    APPID = OWM_API
    if not weather.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await eod(weather, "`Please specify a city or set one as default.`")
            return
    else:
        CITY = weather.pattern_match.group(1)

    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }

    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                await eod(weather, "`Invalid country.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}"
    request = requests.get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await eod(weather, f"`Invalid country.`")
        return

    cityname = result["name"]
    curtemp = result["main"]["temp"]
    humidity = result["main"]["humidity"]
    min_temp = result["main"]["temp_min"]
    max_temp = result["main"]["temp_max"]
    pressure = result["main"]["pressure"]
    feel = result["main"]["feels_like"]
    desc = result["weather"][0]
    desc = desc["main"]
    country = result["sys"]["country"]
    sunrise = result["sys"]["sunrise"]
    sunset = result["sys"]["sunset"]
    wind = result["wind"]["speed"]
    winddir = result["wind"]["deg"]
    cloud = result["clouds"]["all"]
    ctimezone = tz(c_tz[country][0])
    time = datetime.datetime.now(ctimezone).strftime("%A, %I:%M %p")
    fullc_n = c_n[f"{country}"]
    # dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    #        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

    div = 360 / len(dirs)
    funmath = int((winddir + (div / 2)) / div)
    findir = dirs[funmath % len(dirs)]
    kmph = str(wind * 3.6).split(".")
    mph = str(wind * 2.237).split(".")

    def fahrenheit(f):
        temp = str(((f - 273.15) * 9 / 5 + 32)).split(".")
        return temp[0]

    def celsius(c):
        temp = str((c - 273.15)).split(".")
        return temp[0]

    def sun(unix):
        xx = datetime.datetime.fromtimestamp(unix, tz=ctimezone).strftime("%I:%M %p")
        return xx

    await eor(
        weather,
        f"🌡️ **Temperature :** `{celsius(curtemp)}°C | {fahrenheit(curtemp)}°F`\n"
        + f"👩‍🏫 **Human Feeling** `{celsius(feel)}°C | {fahrenheit(feel)}°F`\n"
        + f"🌨️ **Min. Temp. :** `{celsius(min_temp)}°C | {fahrenheit(min_temp)}°F`\n"
        + f"☀️ **Max. Temp. :** `{celsius(max_temp)}°C | {fahrenheit(max_temp)}°F`\n"
        + f"🌦️ **Humidity :** `{humidity}%`\n"
        + f"❕**Pressure :** `{pressure} hPa`\n"
        + f"🌬️ **Wind :** `{kmph[0]} kmh | {mph[0]} mph, {findir}`\n"
        + f"☁️ **Cloud :** `{cloud} %`\n"
        + f"🌄 **Sunrise :** `{sun(sunrise)}`\n"
        + f"🌅 **Sunset :** `{sun(sunset)}`\n\n\n"
        + f"**{desc}**\n"
        + f"`{cityname}, {fullc_n}`\n"
        + f"`{time}`\n\n"
        + f"**By :**  {hell_mention}",
    )


@bot.on(hell_cmd(outgoing=True, pattern="setcity(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="setcity(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def set_default_city(city):
    if city.fwd_from:
        return
    if not OWM_API:
        await edit_or_reply(
            city, "`Get an API key from` https://openweathermap.org/ `first.`"
        )
        return
    global DEFCITY
    APPID = OWM_API
    if not city.pattern_match.group(1):
        CITY = DEFCITY
        if not CITY:
            await edit_or_reply(city, "`Please specify a city to set it as default.`")
            return
    else:
        CITY = city.pattern_match.group(1)
    timezone_countries = {
        timezone: country
        for country, timezones in c_tz.items()
        for timezone in timezones
    }
    if "," in CITY:
        newcity = CITY.split(",")
        if len(newcity[1]) == 2:
            CITY = newcity[0].strip() + "," + newcity[1].strip()
        else:
            country = await get_tz((newcity[1].strip()).title())
            try:
                countrycode = timezone_countries[f"{country}"]
            except KeyError:
                await edit_or_reply(city, "`Invalid country.`")
                return
            CITY = newcity[0].strip() + "," + countrycode.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={APPID}"
    request = requests.get(url)
    result = json.loads(request.text)
    if request.status_code != 200:
        await city.edit(f"`Invalid country.`")
        return
    DEFCITY = CITY
    cityname = result["name"]
    country = result["sys"]["country"]
    fullc_n = c_n[f"{country}"]
    await edit_or_reply(city, f"`Set default city as {cityname}, {fullc_n}.`")


@bot.on(hell_cmd(pattern="wttr ?(.*)"))
@bot.on(sudo_cmd(pattern="wttr ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    global DEFCITY
    reply_to_id = None
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
    if not input_str:
        input_str = DEFCITY
    await event.edit("Collecting Weather Reports...")
    async with aiohttp.ClientSession() as session:
        sample_url = "https://wttr.in/{}.png"
        response_api_zero = await session.get(sample_url.format(input_str))
        response_api = await response_api_zero.read()
        with io.BytesIO(response_api) as out_file:
            await event.reply(
                f"**City : **`{input_str}`", file=out_file, reply_to=reply_to_id
            )
    try:
        await event.delete()
    except:
        pass


CmdHelp("climate").add_command(
  "climate", "Name of state/country", "Gets the weather of a city. By default it is Delhi, change it by setcity"
).add_command(
  "setcity", "<city>/<country>", "Sets your default city."
).add_command(
  "wttr", "<city>", "Shows you the climate data of 3 days from today in a image format."
).add_info(
  "Climates And Weathers."
).add_warning(
  "✅ Harmless Module."
).add()
