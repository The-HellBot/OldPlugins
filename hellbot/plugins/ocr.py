import json
import os
import requests

from . import *


def ocr_space_file(
    filename, overlay=False, api_key=Config.OCR_API, language="eng"
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

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
    """OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

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


def progress(current, total):
    logger.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


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


@hell_cmd(pattern="ocr(?:\s|$)([\s\S]*)")
async def parse_ocr_space_api(event):
    hell = await eor(event, "Processing weit...🤓")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await event.client.download_media(
        await event.get_reply_message(),
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=progress,
    )
    test_file = ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
        ProcessingTimeInMilliseconds = str(
            int(test_file["ProcessingTimeInMilliseconds"]) // 1000
        )
    except Exception as e:
        await eod(hell, "**Errors !!** \n`{}`\n**Report This to** {}\n\n`{}`".format(
                str(e), hell_grp, json.dumps(test_file, sort_keys=True, indent=4)
            )
        )
    else:
        await hell.edit("Read Document in {} seconds. \n{}".format(
                ProcessingTimeInMilliseconds, ParsedText
            )
        )
    os.remove(downloaded_file_name)
    await hell.edit(ParsedText)


CmdHelp("ocr").add_command(
  "ocr", "<reply to a img> <lang code>", "Reads and sends you the text written in replied image in selected language"
).add_command(
  "ocrlang", None, "Gives the list of supported languages of OCR."
).add_info(
  "Read Texts On Images."
).add_warning(
  "✅ Harmless Module."
).add()
