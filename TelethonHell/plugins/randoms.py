import random

from TelethonHell.plugins import *


@hell_cmd(pattern="sing$")
async def _(e):
    txt = random.choice(SONGS)
    await eor(e, txt)


@hell_cmd(pattern="hpotter$")
async def _(e):
    txt = random.choice(HARRY)
    await eor(e, txt)


@hell_cmd(pattern="gott$")
async def _(e):
    txt = random.choice(GOTT)
    await eor(e, txt)


@hell_cmd(pattern="gotm$")
async def _(e):
    txt = random.choice(GOTM)
    await eor(e, txt, link_preview=True)


@hell_cmd(pattern="bello$")
async def _(e):
    txt = random.choice(BELLO)
    await eor(e, txt)


@hell_cmd(pattern="tip$")
async def _(e):
    txt = random.choice(TIPS)
    await eor(e, txt)


@hell_cmd(pattern="qt$")
async def _(e):
    txt = random.choice(QT)
    await eor(e, txt)


@hell_cmd(pattern="logic$")
async def _(e):
    txt = random.choice(LOGIC)
    await eor(e, txt)


@hell_cmd(pattern="snow$")
async def _(e):
    txt = random.choice(SNOW)
    await eor(e, txt)


@hell_cmd(pattern="shayri$")
async def _(e):
    _, _, hell_mention = await client_id(e)
    txt = random.choice(SHAYRI)
    await eor(e, txt.format(hell_mention))


@hell_cmd(pattern="hflirt$")
async def _(e):
    _, _, hell_mention = await client_id(e)
    txt = random.choice(HFLIRT)
    await eor(e, txt.format(hell_mention))


@hell_cmd(pattern="eflirt$")
async def _(e):
    _, _, hell_mention = await client_id(e)
    txt = random.choice(EFLIRT)
    await eor(e, txt.format(hell_mention))


@hell_cmd(pattern="attitude$")
async def _(e):
    _, _, hell_mention = await client_id(e)
    txt = random.choice(ATTITUDE)
    await eor(e, txt.format(hell_mention))


@hell_cmd(pattern="gbye$")
async def _(e):
    _, _, hell_mention = await client_id(e)
    txt = random.choice(GBYE)
    await eor(e, txt.format(hell_mention))


CmdHelp("randoms").add_command(
    "sing", None, "Sings a song"
).add_command(
    "hpotter", None, "Random harry porter character"
).add_command(
    "gott", None, "Sends a random thought"
).add_command(
    "gotm", None, "Sends a random meme"
).add_command(
    "bello", None, "Sends quote for being logical"
).add_command(
    "tip", None, "Sends you a life changer tip"
).add_command(
    "qt", None, "Sends a random question. solve it if you can!!"
).add_command(
    "logic", None, "Sends you a logical quote"
).add_command(
    "snow", None, "Sends random quote from Game of thrones"
).add_command(
    "gbye", None, "Sends random good bye quote"
).add_command(
    "attitude", None, "Sends a random attitude quote."
).add_command(
    "eflirt", None, "Sends a random flirt quote in english"
).add_command(
    "hflirt", None, "Sends a random flirt quote in hindi"
).add_command(
    "shayri", None, "Sends a random heart touching quote"
).add_info(
    "Some Random Quotes."
).add_warning(
    "✅ Harmless Module."
).add()
