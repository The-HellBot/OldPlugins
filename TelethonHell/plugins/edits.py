import asyncio
import random

import pyfiglet
from TelethonHell.plugins import *


@hell_cmd(pattern="type(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    shiiinabot = "\u2060"
    for i in range(601):
        shiiinabot += "\u2060"
    try:
        await eor(event, shiiinabot)
    except Exception as e:
        LOGS.warn(str(e))
    typing_symbol = "_"
    previous_text = ""
    await eor(event, typing_symbol)
    await asyncio.sleep(0.3)
    for character in input_str:
        previous_text = previous_text + "" + character
        typing_text = previous_text + "" + typing_symbol
        try:
            await eor(event, typing_text)
        except Exception as e:
            LOGS.warn(str(e))
        await asyncio.sleep(0.3)
        try:
            await eor(event, previous_text)
        except Exception as e:
            LOGS.warn(str(e))
        await asyncio.sleep(0.3)


@hell_cmd(pattern="emoji(?:\s|$)([\s\S]*)")
async def _(event):
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "shrug":
        await eor(event, "¯\_(ツ)_/¯")
    elif input_str == "apple":
        await eor(event, "\uF8FF")
    elif input_str == ":/":
        hell = await eor(event, input_str)
        animation_chars = [":\\", ":/"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await hell.edit(animation_chars[i % 2])
    elif input_str == "-_-":
        hell = await eor(event, input_str)
        animation_chars = ["-__-", "-_-"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await hell.edit(animation_chars[i % 2])


@hell_cmd(pattern=f"gendar$")
async def metoo(e):
    txt = random.choice(GENDER)
    await eor(e, txt)


@hell_cmd(pattern=f"shrug$")
async def metoo(e):
    txt = random.choice(SHRUG)
    await eor(e, txt)


@hell_cmd(pattern=f"dogge")
async def metoo(e):
    txt = random.choice(DOG)
    await eor(e, txt)


@hell_cmd(pattern=f"mesed$")
async def metoo(e):
    txt = random.choice(SED)
    await eor(e, txt)


@hell_cmd(pattern=f"medead$")
async def metoo(e):
    txt = random.choice(DEAD)
    await eor(e, txt)


@hell_cmd(pattern=f"confused$")
async def metoo(e):
    txt = random.choice(CONFUSED)
    await eor(e, txt)


@hell_cmd(pattern=f"lobb$")
async def metoo(e):
    txt = random.choice(LOB)
    await eor(e, txt)


@hell_cmd(pattern=f"wut$")
async def metoo(e):
    txt = random.choice(WTF)
    await eor(e, txt)


@hell_cmd(pattern=f"wavee$")
async def metoo(e):
    txt = random.choice(WAVING)
    await eor(e, txt)


@hell_cmd(pattern=f"hehe$")
async def metoo(e):
    txt = random.choice(EMOTICONS)
    await eor(e, txt)


@hell_cmd(pattern="figlet(?:\s|$)([\s\S]*)")
async def figlet(event):
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = event.pattern_match.group(1)
    if ":" in input_str:
        text, cmd = input_str.split(":", 1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await eod(event, "Please add some text to figlet")
        return
    if cmd is not None:
        cmd = cmd.strip()
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await parse_error(event, "Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await eor(event, "‌‌‎`{}`".format(result))


CmdHelp("edits").add_command(
    "hehe", None, "Use and see"
).add_command(
    "wavee", None, "Use and see"
).add_command(
    "wut", None, "Use and see"
).add_command(
    "lobb", None, "Use and see"
).add_command(
    "confused", None, "Use and see"
).add_command(
    "medead", None, "Use and see"
).add_command(
    "mesed", None, "Use and see"
).add_command(
    "doge", None, "Use and see"
).add_command(
    "shrug", None, "Use and see"
).add_command(
    "gendar", None, "Use and see"
).add_command(
    "type", "<word>", "Animates the given word into a typewriter."
).add_command(
    "emoji", None, "Available cmnds are:-\n• shrug\n• apple\n• :/\n• -_-\n Add .emoji in front of all cmds."
).add_command(
    "figlet", "text : type", "The types are slant, 3D, 5line, alpha, banner, doh, iso, letter, allig, dotm, bubble, bulb, digi"
).add_info(
    "Bass Bakchodi hai ye."
).add_warning(
    "✅ Harmless Module."
).add()
