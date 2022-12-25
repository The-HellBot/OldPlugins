import json
import os

import requests
from TelethonHell.plugins import *


def ocr_space_file(filename, overlay=False, api_key=Config.OCR_API, language="eng"):
    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.json()


def ocr_space_url(url, overlay=False, api_key=Config.OCR_API, language="eng"):
    payload = {
        "url": url,
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    r = requests.post(
        "https://api.ocr.space/parse/image",
        data=payload,
    )
    return r.json()


@hell_cmd(pattern="ocrlang$")
async def get_ocr_languages(event):
    languages = {}
    languages["English"] = "eng"
    languages["Arabic"] = "ara"
    languages["Bulgarian"] = "bul"
    languages["Chinese (Simplified)"] = "chs"
    languages["Chinese (Traditional)"] = "cht"
    languages["Croatian"] = "hrv"
    languages["Czech"] = "cze"
    languages["Danish"] = "dan"
    languages["Dutch"] = "dut"
    languages["Finnish"] = "fin"
    languages["French"] = "fre"
    languages["German"] = "ger"
    languages["Greek"] = "gre"
    languages["Hungarian"] = "hun"
    languages["Korean"] = "kor"
    languages["Italian"] = "ita"
    languages["Japanese"] = "jpn"
    languages["Polish"] = "pol"
    languages["Portuguese"] = "por"
    languages["Russian"] = "rus"
    languages["Slovenian"] = "slv"
    languages["Spanish"] = "spa"
    languages["Swedish"] = "swe"
    languages["Turkish"] = "tur"
    a = json.dumps(languages, sort_keys=True, indent=4)
    await eor(event, str(a))


@hell_cmd(pattern="read(?:\s|$)([\s\S]*)")
async def parse_ocr_space_api(event):
    if not Config.OCR_API:
        return await parse_error(event, "`OCR_API` is not configured. Get an API: [click here](https://ocr.space/ocrapi/freekey)")
    hell = await eor(event, "Processing weit...🤓")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await event.client.download_media(
        await event.get_reply_message(),
        Config.TMP_DOWNLOAD_DIRECTORY,
    )
    test_file = ocr_space_file(filename=downloaded_file_name, language=lang_code)
    os.remove(downloaded_file_name)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        await parse_error(hell, e)
        return
    await hell.edit(ParsedText)


CmdHelp("ocr").add_command(
    "read", "<reply to a img> <lang code>", "Reads and sends you the text written in replied image in selected language"
).add_command(
    "ocrlang", None, "Gives the list of supported languages of OCR."
).add_info(
    "Read Texts On Images."
).add_warning(
    "✅ Harmless Module."
).add()
