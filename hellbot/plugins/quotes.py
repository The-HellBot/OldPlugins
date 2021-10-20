import requests

from random import choice

from . import *


@hell_cmd(pattern="love$")
async def love(e):
    txt = choice(LOVESTR)
    await eor(e, txt)

@hell_cmd(pattern="dhoka$")
async def katgya(e):
    txt = choice(DHOKA)
    await eor(e, txt)

@hell_cmd(pattern="metoo$")
async def metoo(e):
    txt = choice(METOOSTR)
    await eor(e, txt)

@hell_cmd(pattern="gdnoon$")
async def noon(e):
    txt = choice(GDNOON)
    await eor(e, txt)

@hell_cmd(pattern="chase$")
async def police(e):
    txt = choice(CHASE_STR)
    await eor(e, txt)

@hell_cmd(pattern="congo$")
async def Sahih(e):
    txt = choice(CONGRATULATION)
    await eor(e, txt)

@hell_cmd(pattern="qhi$")
async def hoi(e):
    txt = choice(HELLOSTR)
    await eor(e, txt)

@hell_cmd(pattern="gdbye$")
async def bhago(e):
    txt = choice(BYESTR)
    await eor(e, txt)

@hell_cmd(pattern="gdnyt$")
async def night(e):
    txt = choice(GDNIGHT)
    await eor(e, txt)

@hell_cmd(pattern="gdmng$")
async def morning(e):
    txt = choice(GDMORNING)
    await eor(e, txt)

@hell_cmd(pattern="quote ?(.*)")
async def quote_search(event):
    hell = await eor(event, "`Processing...`")
    input_str = event.pattern_match.group(1)
    if not input_str:
        api_url = "https://quotes.cwprojects.live/random"
        try:
            response = requests.get(api_url).json()
        except:
            response = None
    else:
        api_url = f"https://quotes.cwprojects.live/search/query={input_str}"
        try:
            response = choice(requests.get(api_url).json())
        except:
            response = None
    if response is not None:
        await hell.edit(f"`{response['text']}`")
    else:
        await eod(hell, "`Sorry Zero results found`")


CmdHelp("quotes").add_command(
  "quote", "<input>", "Sends a random mind-blowing quote"
).add_command(
  "gdmng", None, "Sends a random Good Morning Quote"
).add_command(
  "gdnyt", None, "Sends a random Good Night Quote"
).add_command(
  "gdbye", None, "Sends a random Good Byee Quote"
).add_command(
  "qhi", None, "Sends a random Hello msg"
).add_command(
  "congo", None, "Sends a random congratulations quote"
).add_command(
  "chase", None, "Sends a random Chase quote"
).add_command(
  "gdnoon", None, "Sends a random Good Afternoon quote"
).add_command(
  "metoo", None, "Sends a text saying Mee too."
).add_command(
  "dhoka", None, "Sends a random Dhoka quote(katt gya bc)"
).add_command(
  "love", None, "Sends a random love quote🥰. (A stage before .dhoka)"
).add_info(
  "Random Quotes."
).add_warning(
  "✅ Harmless Module."
).add()
