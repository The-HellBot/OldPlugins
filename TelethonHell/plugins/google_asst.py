import datetime
import os
import subprocess

import emoji
from googletrans import Translator
from gtts import gTTS
from TelethonHell.plugins import *


@hell_cmd(pattern="meaning ([\s\S]*)")
async def _(event):
    word = event.text[9:]
    try:
        response = await AioHttp().get_json(f"http://api.urbandictionary.com/v0/define?term={word}")
        word = response["list"][0]["word"]
        definition = response["list"][0]["definition"]
        example = response["list"][0]["example"]
        result = f"**Text: {word}**\n**Meaning:**\n`{definition}`\n\n**Example:**\n`{example}`"
        await eor(event, result)
    except Exception as e:
        await parse_error(event, e)


@hell_cmd(pattern="trt(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[5:]
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif "-" in input_str:
        lan, text = input_str.split("-")
    else:
        await eod(
            event,
            f"`{hl}trt LanguageCode - message`  or  `{hl}trt LanguageCode as reply to a message.`\n\nTry `{hl}trc` to get all language codes",
        )
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = "**Translated From** __{}__ **to** __{}__\n\n`{}`".format(
            translated.src, lan, after_tr_text
        )
        await eor(event, output_str)
    except Exception as exc:
        await parse_error(event, exc)


@hell_cmd(pattern="trc$")
async def _(hell):
    await eor(
        hell,
        "**All The Language Codes Can Be Found** ⚡ [Here](https://te.legra.ph/SfMæisér--𐌷𐌴ࠋࠋ𐌱𐍈𐌸-𐌾𐌰𐍀𐌾-06-04) ⚡",
        link_preview=False,
    )


@hell_cmd(pattern="voice(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "Preparing Voice....")
    input_str = event.pattern_match.group(1)
    start = datetime.datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "-" in input_str:
        lan, text = input_str.split("-")
    else:
        await eod(
            hell,
            f"Invalid Syntax. Module stopping. Check out `{hl}plinfo google_asst` for help.",
        )
        return
    text = text.strip()
    lan = lan.strip()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "voice.ogg"
    try:
        tts = gTTS(text, lang=lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
            required_file_name,
            "-map",
            "0:a",
            "-codec:a",
            "libopus",
            "-b:a",
            "100k",
            "-vbr",
            "on",
            required_file_name + ".opus",
        ]
        try:
            t_response = subprocess.check_output(
                command_to_execute, stderr=subprocess.STDOUT
            )
        except (subprocess.CalledProcessError, NameError, FileNotFoundError) as exc:
            await hell.edit(str(exc))
        else:
            os.remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await event.client.send_file(
            event.chat_id,
            required_file_name,
            caption=f"**• Voiced:** `{text[0:97]}....` \n**• Language:** `{lan}` \n**• Time Taken:** `{ms} seconds`",
            reply_to=event.message.reply_to_msg_id,
            allow_cache=False,
            voice_note=True,
        )
        os.remove(required_file_name)
        await hell.delete()
    except Exception as e:
        await parse_error(hell, e)


CmdHelp("google_asst").add_command(
    "voice", "<reply to a msg> <lang code>", "Sends the replied msg content in audio format."
).add_command(
    "trt", "<lang code> <reply to msg>", "Translates the replied message to desired language code. Type '.trc' to get all the language codes", f"trt en - hello | {hl}trt en <reply to msg>"
).add_command(
    "trc", None, "Gets all the possible language codes for google translate module"
).add_command(
    "meaning", "query", "Fetches meaning of given word from Urban Dictionary."
).add_info(
    "Google Assistant"
).add_warning(
    "✅ Harmless Module."
).add()
