import asyncio
import json
import os
import datetime
from urllib.parse import quote

from telethon import events
import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@bot.on(hell_cmd(pattern="scan ?(.*)"))
@bot.on(sudo_cmd(pattern="scan ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "Reply to any user message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eod(event, "Reply to a media message")
        return
    chat = "@DrWebBot"
    if reply_message.sender.bot:
        await eod(event, "Reply to actual users message.")
        return
    hellevent = await eor(event, " `Scanning This media..... wait👀`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=161163358)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await eod(hellevent, "`Please unblock `@DrWebBot `and try again`")
            return
        if response.text.startswith("Forward"):
            await eod(hellevent,
                "Can you kindly disable your forward privacy settings for good?"
            )
        else:
            if response.text.startswith("Select"):
                await eod(hellevent,
                    "`Please go to` @DrWebBot `and select your language.`"
                )
            else:
                await hellevent.edit(
                    f"**Antivirus scan was completed. I got the final results.**\n\n {response.message.message}"
                )


@bot.on(hell_cmd(pattern=r"decode$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"decode$", allow_sudo=True))
async def parseqr(qr_e):
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    # For .decode command, get QR Code/BarCode content from the replied photo.
    downloaded_file_name = await qr_e.client.download_media(
        await qr_e.get_reply_message(), Config.TMP_DIR
    )
    # parse the Official ZXing webpage to decode the QRCode
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
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if not t_response:
        return await edit_or_reply(qr_e, f"Failed to decode.\n`{e_response}`")
    soup = BeautifulSoup(t_response, "html.parser")
    qr_contents = soup.find_all("pre")[0].text
    await edit_or_reply(qr_e, qr_contents)
    if os.path.exists(downloaded_file_name):
        os.remove(downloaded_file_name)


@bot.on(hell_cmd(pattern="barcode ?(.*)"))
@bot.on(sudo_cmd(pattern="barcode ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
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


@bot.on(hell_cmd(pattern=r"makeqr(?: |$)([\s\S]*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"makeqr(?: |$)([\s\S]*)", allow_sudo=True))
async def make_qr(makeqr):
    input_str = makeqr.pattern_match.group(1)
    message = f"SYNTAX: `{hl}makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif makeqr.reply_to_msg_id:
        previous_message = await makeqr.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await makeqr.client.download_media(previous_message)
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
    await makeqr.client.send_file(
        makeqr.chat_id, "img_file.webp", reply_to=reply_msg_id
    )
    os.remove("img_file.webp")
    await makeqr.delete()


@bot.on(hell_cmd(pattern="cal (.*)"))
@bot.on(sudo_cmd(pattern="cal (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.datetime.now()
    input_str = event.pattern_match.group(1)
    hell = await eor(event, "Processing...")
    input_sgra = input_str.split(".")
    if len(input_sgra) == 3:
        yyyy = input_sgra[0]
        mm = input_sgra[1]
        dd = input_sgra[2]
        required_url = "https://calendar.kollavarsham.org/api/years/{}/months/{}/days/{}?lang={}".format(
            yyyy, mm, dd, "en"
        )
        headers = {"Accept": "application/json"}
        response_content = requests.get(required_url, headers=headers).json()
        a = ""
        if "error" not in response_content:
            current_date_detail_arraays = response_content["months"][0]["days"][0]
            a = json.dumps(current_date_detail_arraays, sort_keys=True, indent=4)
        else:
            a = response_content["error"]
        await hell.edit(str(a))
    else:
        await eod(hell, f"SYNTAX: {hl}calendar YYYY.MM.DD")
    end = datetime.datetime.now()
    (end - start).seconds


@bot.on(hell_cmd(pattern="currency (.*)"))
@bot.on(sudo_cmd(pattern="currency (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from
            )
            current_response = requests.get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await edit_or_reply(
                    event,
                    "{} {} = {} {}".format(number, currency_from, rebmun, currency_to),
                )
            else:
                await edit_or_reply(
                    event,
                    f"Well, Hate to tell yout this but this Currency isn't supported😣 **yet**.\n__Try__ `{hl}currencies` __for a list of supported currencies.__🤐",
                )
        except Exception as e:
            await eod(event, str(e))
    else:
        await edit_or_reply(
            event,
            f"**Syntax:**\n{hl}currency amount from to\n**Example:**\n`{hl}currency 10 usd inr`",
        )


@bot.on(hell_cmd(pattern="currencies$"))
@bot.on(sudo_cmd(pattern="currencies$", allow_sudo=True))
async def currencylist(ups):
    if ups.fwd_from:
        return
    request_url = "https://api.exchangeratesapi.io/latest?base=USD"
    current_response = requests.get(request_url).json()
    dil_wale_puch_de_na_chaaa = current_response["rates"]
    hmm = ""
    for key, value in dil_wale_puch_de_na_chaaa.items():
        hmm += f"`{key}`" + "\t\t\t"
    await eor(ups, f"**List of some currencies:**\n{hmm}\n")


@bot.on(hell_cmd(pattern="ifsc (.*)"))
@bot.on(sudo_cmd(pattern="ifsc (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://ifsc.razorpay.com/{}".format(input_str)
    r = requests.get(url)
    if r.status_code == 200:
        b = r.json()
        a = json.dumps(b, sort_keys=True, indent=4)
        # https://stackoverflow.com/a/9105132/4723940
        await eor(event, str(a))
    else:
        await eor(event, "`{}`: {}".format(input_str, r.text))


@bot.on(hell_cmd(pattern="color (.*)"))
@bot.on(sudo_cmd(pattern="color (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
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
        await eod(
            event, f"**Syntax : **`{hl}color <color_code>` example : `{hl}color #ff0000`"
        )


@bot.on(hell_cmd(pattern="xkcd ?(.*)"))
@bot.on(sudo_cmd(pattern="xkcd ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
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

@bot.on(hell_cmd(pattern="dns (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="dns (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(event, "DNS records of [This link]({}) are \n{}".format(input_str, response_api, link_preview=False))
    else:
        await eod(event, "i can't seem to find [this link]({}) on the internet".format(input_str, link_preview=False))


@bot.on(hell_cmd(pattern="url (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="url (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await eor(event, f"**Generated  [short link]({response_api})** \n**Long link :** [here]({input_str})", link_preview=True)
    else:
        await eod(event, "something is wrong. please try again later.")


@bot.on(hell_cmd(pattern="unshort (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="unshort (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await eor(event, "Input URL: [Short Link]({}) \nReDirected URL: [Long link]({})".format(input_str, r.headers["Location"], link_preview=False)
        )
    else:
        await eod(event, 
            "Input URL [short link]({}) returned status_code {}".format(input_str, r.status_code)
        )


CmdHelp("tools").add_command(
  "xkcd", "<query>", "Searches for the query for the relevant XKCD comic"
).add_command(
  "color", "<color code>", "Sends you a plain image of the color", ".color #ff0000"
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
  "cal", "<year ; month>", "Shows you the calendar of given month and year"
).add_command(
  "decode", "<reply to barcode/qrcode>", "To get decoded content of those codes."
).add_command(
  "barcode", "<content>", "Make a BarCode from the given content.", ".barcode www.google.com"
).add_command(
  "makeqr", "<content>", "Make a Qrcode from the given content.", ".makeqr www.google.com"
).add_command(
  "scan", "<reply to media or file>", "It scans the media or file and checks either any virus is in the file or media"
).add_info(
  "Some Basic Tools."
).add_warning(
  "✅ Harmless Module."
).add()
