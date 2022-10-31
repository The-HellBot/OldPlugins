import asyncio
import calendar
import datetime
import json
import os
from urllib.parse import quote

import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor, ImageDraw, ImageFont
from TelethonHell.plugins import *

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


@hell_cmd(pattern="time(?:\s|$)([\s\S]*)")
async def _(event):
    current_time = datetime.datetime.now().strftime(
        "⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\
        \n   HELLBOT TIMEZONE   \
        \n   LOCATION: India🇮🇳  \
        \n   Time: %H:%M:%S  \
        \n   Date: %d.%m.%y     \
        \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡"
    )
    start = datetime.datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = (
        Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.datetime.now()) + ".webp"
    )
    img = Image.new("RGBA", (350, 220), color=(0, 0, 0, 115))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await event.client.send_file(
        event.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
    )
    os.remove(required_file_name)
    end = datetime.datetime.now()
    time_taken_ms = (end - start).seconds
    await eod(event, "Created sticker in {} seconds".format(time_taken_ms))


@hell_cmd(pattern="decode$")
async def parseqr(event):
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    downloaded_file_name = await event.client.download_media(
        await event.get_reply_message(), Config.TMP_DIR
    )
    command_to_exec = [
        "curl",
        "-X",
        "POST",
        "-F",
        "f=@" + downloaded_file_name + "",
        "https://zxing.org/w/decode",
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if not t_response:
        return await edit_or_reply(event, f"Failed to decode.\n`{e_response}`")
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await edit_or_reply(event, qr_contents)
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)


@hell_cmd(pattern="barcode(?:\s|$)([\s\S]*)")
async def _(event):
    hellevent = await eor(event, "...")
    start = datetime.datetime.now()
    input_str = event.pattern_match.group(1)
    message = f"SYNTAX: `{hl}barcode <long text to include>`"
    reply_msg_id = event.message.id
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = f"SYNTAX: `{hl}barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await event.client.send_file(
            event.chat_id,
            filename,
            caption=message,
            reply_to=reply_msg_id,
        )
        os.remove(filename)
    except Exception as e:
        await hellevent.edit(str(e))
        return
    end = datetime.datetime.now()
    ms = (end - start).seconds
    await hellevent.edit("Created BarCode in {} seconds🤓".format(ms))
    await asyncio.sleep(5)
    await hellevent.delete()


@hell_cmd(pattern="makeqr(?: |$)([\s\S]*)")
async def make_qr(event):
    input_str = event.pattern_match.group(1)
    message = f"SYNTAX: `{hl}makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(previous_message)
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("img_file.webp", "PNG")
    await event.client.send_file(event.chat_id, "img_file.webp", reply_to=reply_msg_id)
    os.remove("img_file.webp")
    await event.delete()


@hell_cmd(pattern="calendar(?:\s|$)([\s\S]*)")
async def _(event):
    lists = event.text.split(" ", 1)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    if len(lists) == 2:
        query = lists[1].split("/")
        year = query[0].strip()
        month = query[1].strip()
    try:
        cal = calendar.month(int(year), int(month))
        await eor(event, f"`{cal}`")
    except Exception as e:
        return await parse_error(event, e)


@hell_cmd(pattern="currency(?:\s|$)([\s\S]*)")
async def _(event):
    if not Config.CURRENCY_API:
        return await parse_error(event, "`CURRENCY_API` __not configured.__", False)
    lists = event.text.split(" ", 3)
    if not len(lists) == 4:
        return await parse_error(event, f"__Give proper command:__ \n__Ex:__`{hl}currency 10 usd inr`", False)
    if lists[1].strip().isdigit():
        amnt = lists[1].strip()
        base = lists[2].strip().upper()
        into = lists[3].strip().upper()
    else:
        return await parse_error(event, f"__Give proper command:__ \n__Ex:__`{hl}currency 10 usd inr`", False)
    hell = await eor(event, f"**Converting currency:** \n__From:__ `{base}` \n__To:__ `{into}` \n__Amount:__ `{amnt}`")
    url = f"https://v6.exchangerate-api.com/v6/{Config.CURRENCY_API}/pair/{base}/{into}/{int(amnt)}"
    data = requests.get(url).json()
    try:
        if data['result'] == 'success':
            base = data['base_code']
            into = data['target_code']
            rate = data['conversion_rate']
            conv = data['conversion_result']
            output = f"__» From:__ `{amnt} {base}` \n__» To:__ `{into}` \n__» Rate:__ `{rate}` \n__» Result:__ `{conv} {into}`"
            await hell.edit(f"**Currency Converted !!** \n\n{output}")
        else:
            await eod(hell, "Something went wrong. Try again later!")
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="currencies$")
async def currencylist(event):
    if not Config.CURRENCY_API:
        return await parse_error(event, "`CURRENCY_API` __not configured.__", False)
    hell = await eor(event, "Fetching supportred currencies lists ...")
    url = f"https://v6.exchangerate-api.com/v6/{Config.CURRENCY_API}/codes"
    data = requests.get(url).json()
    codes = data['supported_codes']
    dicts = {}
    for x, y in codes:
        dicts.setdefault(x, y)
    key = list(dicts.keys())
    value = list(dicts.values())
    output = "<b><i><u>◈ List of supported currencies are:</b></i></u> \n\n"
    try:
        for i in range(len(key)):
            output += f"<code>▸ {key[i]} : {value[i]}</code> \n"
        output += "\n<img src='https://te.legra.ph/file/2c546060b20dfd7c1ff2d.jpg'/>"
        link = await telegraph_paste("Currency List For HellBot", output)
        await hell.edit(
            f"<b><i>⊹ Supported currency lists are:</b></i> \n\n<i>⊷ <u><a href='{link}'>Currency Lists</a></u> ⊶</i>",
            link_preview=False,
            parse_mode='HTML',
        )
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="ifsc(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url)
    if r.status_code == 200:
        b = r.json()
        a = json.dumps(b, sort_keys=True, indent=4)
        await eor(event, str(a))
    else:
        await eor(event, "`{}`: {}".format(input_str, r.text))


@hell_cmd(pattern="color(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    message_id = None
    if event.sender_id != bot.uid:
        message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("hell.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await event.client.send_file(
                event.chat_id,
                "hell.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id,
            )
            os.remove("hell.png")
            await event.delete()
    else:
        await parse_error(event, f"__Give proper command:__ \n`{hl}color <color_code>` \n__Example:__ `{hl}color #ff0000`", False)


@hell_cmd(pattern="xkcd(?:\s|$)([\s\S]*)")
async def _(event):
    hellevent = await eor(event, "`processiong...`")
    input_str = event.pattern_match.group(1)
    xkcd_id = None
    if input_str:
        if input_str.isdigit():
            xkcd_id = input_str
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url, params={"action": "xkcd", "query": quote(input_str)}
            ).text
            xkcd_id = queryresult.split(" ")[2].lstrip("\n")
    if xkcd_id is None:
        xkcd_url = "https://xkcd.com/info.0.json"
    else:
        xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
    r = requests.get(xkcd_url)
    if r.ok:
        data = r.json()
        year = data.get("year")
        month = data["month"].zfill(2)
        day = data["day"].zfill(2)
        xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
        safe_title = data.get("safe_title")
        data.get("transcript")
        alt = data.get("alt")
        img = data.get("img")
        data.get("title")
        output_str = """[\u2060]({})**{}**
[XKCD ]({})
Title: {}
Alt: {}
Day: {}
Month: {}
Year: {}""".format(
            img, input_str, xkcd_link, safe_title, alt, day, month, year
        )
        await hellevent.edit(output_str, link_preview=True)
    else:
        await eod(hellevent, "xkcd n.{} not found!".format(xkcd_id))


@hell_cmd(pattern="dns(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            "DNS records of [This link]({}) are \n{}".format(
                input_str, response_api, link_preview=False
            ),
        )
    else:
        await eod(
            event,
            "i can't seem to find [this link]({}) on the internet".format(
                input_str, link_preview=False
            ),
        )


@hell_cmd(pattern="url(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(
            event,
            f"**Generated  [short link]({response_api})** \n**Long link :** [here]({input_str})",
            link_preview=True,
        )
    else:
        await eod(event, "something is wrong. please try again later.")


@hell_cmd(pattern="unshort(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await eor(
            event,
            "Input URL: [Short Link]({}) \nReDirected URL: [Long link]({})".format(
                input_str, r.headers["Location"], link_preview=False
            ),
        )
    else:
        await eod(
            event,
            "Input URL [short link]({}) returned status_code {}".format(
                input_str, r.status_code
            ),
        )


CmdHelp("tools").add_command(
    "xkcd", "<query>", "Searches for the query for the relevant XKCD comic"
).add_command(
    "color", "<color code>", "Sends you a plain image of the color", ".color #ff0000"
).add_command(
    "time", None, "Gives current time in a cool sticker format."
).add_command(
    "ifsc", "<IFSC code>", "Helps to get details of the relevant bank or branch", ".ifsc SBIN0016086"
).add_command(
    "currencies", None, "Shows you the some list of currencies"
).add_command(
    "dns", "<link>", "Shows you Domain Name System (DNS) of the given link", ".dns google.com"
).add_command(
    "unshort", "<link>", "Unshortens the given short link"
).add_command(
    "url", "<link>", "Shortens the given long link"
).add_command(
    "currency", "<amount> <from> <to>", "Currency converter for HellBot", ".currency 10 usd inr"
).add_command(
    "calendar", "<year / month>", "Shows you the calendar of given month and year"
).add_command(
    "decode", "<reply to barcode/qrcode>", "To get decoded content of those codes."
).add_command(
    "barcode", "<content>", "Make a BarCode from the given content.", ".barcode www.google.com"
).add_command(
    "makeqr", "<content>", "Make a Qrcode from the given content.", ".makeqr www.google.com"
).add_info(
    "Some Basic Tools."
).add_warning(
    "✅ Harmless Module."
).add()
