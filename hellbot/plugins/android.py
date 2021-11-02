import json
import re

from bs4 import BeautifulSoup
from requests import get

from . import *

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/devices.json"
)


@hell_cmd(pattern="magisk$")
async def _(magisk):
    if magisk.fwd_from:
        return
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    magisk_dict = {
        "⦁ **Stable**": magisk_repo + "master/stable.json",
        "⦁ **Beta**": magisk_repo + "master/beta.json",
        "⦁ **Canary**": magisk_repo + "canary/canary.json",
    }
    releases = "**Latest Magisk Releases**\n\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        if "canary" in release_url:
            data["app"]["link"] = magisk_repo + "canary/" + data["app"]["link"]
            data["magisk"]["link"] = magisk_repo + "canary/" + data["magisk"]["link"]
            data["uninstaller"]["link"] = (
                magisk_repo + "canary/" + data["uninstaller"]["link"]
            )

        releases += (
            f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | '
            f'[Uninstaller]({data["uninstaller"]["link"]})\n'
        )
    await eor(magisk, releases)


@hell_cmd(pattern="device(?:\s|$)([\s\S]*)")
async def device_info(request):
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await eor(request, f"`Usage: {hl}device <codename> / <model>`")
        return
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await eor(request, reply)


@hell_cmd(pattern="codename(?: |)([\S]*)(?: |)([\s\S]*)")
async def codename_info(request):
    if request.fwd_from:
        return
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await eor(request, f"`Usage: {hl}codename <brand> <device>`")
        return

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Device**: {item['device']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await eor(request, reply)


@hell_cmd(pattern="specs(?: |)([\S]*)(?: |)([\s\S]*)")
async def devices_specifications(request):
    if request.fwd_from:
        return
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await eor(request, f"`Usage: {hl}specs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await eor(request, f"`{brand} is unknown brand!`")
        return
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await eor(request, f"`can't find {device}!`")
        return
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await eor(request, reply)


@hell_cmd(pattern="twrp(?:\s|$)([\s\S]*)")
async def twrp(request):
    if request.fwd_from:
        return
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await eor(request, f"`Usage: {hl}twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await eor(request, reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await eor(request, reply)


CmdHelp("android").add_command(
  "magisk", None, "Get latest magisk release"
).add_command(
  "device", "<codename>", "Get info about android device codename or model"
).add_command(
  "codename", "<brand> <device>", "Search for android device codename"
).add_command(
  "specs", "<brand> <device>", "Get device specifications info."
).add_command(
  "twrp", "<codename>", "Get latest twrp download for android device."
).add_info(
  "Techy Stuff!"
).add_warning(
  "✅ Harmless Module."
).add()
