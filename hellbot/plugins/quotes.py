import random
from random import choice
import requests
from . import *


@bot.on(hell_cmd(pattern=f"love$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"love$", allow_sudo=True))
async def love(e):
    txt = random.choice(LOVESTR)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"dhoka$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"dhoka$", allow_sudo=True))
async def katgya(e):
    txt = random.choice(DHOKA)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"metoo$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"metoo$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(METOOSTR)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"gdnoon$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gdnoon$", allow_sudo=True))
async def noon(e):
    txt = random.choice(GDNOON)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"chase$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"chase$", allow_sudo=True))
async def police(e):
    txt = random.choice(CHASE_STR)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"congo$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"congo$", allow_sudo=True))
async def Sahih(e):
    txt = random.choice(CONGRATULATION)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"qhi$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"qhi$", allow_sudo=True))
async def hoi(e):
    txt = random.choice(HELLOSTR)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"gdbye$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gdbye$", allow_sudo=True))
async def bhago(e):
    txt = random.choice(BYESTR)
    await eor(e, txt)
    

@bot.on(hell_cmd(pattern=f"gdnyt$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gdnyt$", allow_sudo=True))
async def night(e):
    txt = random.choice(GDNIGHT)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"gdmng$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gdmng$", allow_sudo=True))
async def morning(e):
    txt = random.choice(GDMORNING)
    await eor(e, txt)
  
  
@bot.on(hell_cmd(pattern="quote ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="quote ?(.*)", allow_sudo=True))
async def quote_search(event):
    if event.fwd_from:
        return
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
            response = random.choice(requests.get(api_url).json())
        except:
            response = None
    if response is not None:
        await hell.edit(f"`{response['text']}`")
    else:
        await eod(hell, "`Sorry Zero results found`")


CmdHelp("quotes").add_command(
  "quote", None, "Sends a random mind-blowing quote"
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
