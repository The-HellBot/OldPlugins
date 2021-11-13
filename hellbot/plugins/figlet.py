import pyfiglet

from . import *

@hell_cmd(pattern="figlet ([\s\S]*)")
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
        text, cmd = input_str.split(":", maxsplit=1)
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
            await eod(event, "Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await eor(event, "‌‌‎`{}`".format(result))


CmdHelp("figlet").add_command(
  "figlet", "text : type", "The types are slant, 3D, 5line, alpha, banner, doh, iso, letter, allig, dotm, bubble, bulb, digi"
).add_info(
  "Another Art plugin but figlet."
).add_warning(
  "✅ Harmless Module."
).add()
