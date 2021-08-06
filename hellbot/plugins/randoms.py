import random
from . import *

@bot.on(hell_cmd(pattern=r"sing$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"sing$", allow_sudo=True))
async def _(e):
    txt = random.choice(SONGS)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"hps$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"hps$", allow_sudo=True))
async def _(e):
    txt = random.choice(HARRY)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"gott$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gott$", allow_sudo=True))
async def _(e):
    txt = random.choice(GOTT)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"gotm$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gotm$", allow_sudo=True))
async def _(e):
    txt = random.choice(GOTM)
    await eor(e, txt, link_preview=True)

@bot.on(hell_cmd(pattern="bello$", outgoing=True))
@bot.on(sudo_cmd(pattern="bello$", allow_sudo=True))
async def _(e):
    txt = random.choice(BELLO)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=r"tip$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"tip$", allow_sudo=True))
async def _(e):
    txt = random.choice(TIPS)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=r"qt$"))
@bot.on(sudo_cmd(pattern=r"qt$", allow_sudo=True))
async def _(e):
    txt = random.choice(QT)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"logic$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"logic$", allow_sudo=True))
async def _(e):
    txt = random.choice(LOGIC)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=r"snow$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"sonw$", allow_sudo=True))
async def _(e):
    txt = random.choice(SNOW)
    await eor(e, txt)

@bot .on(hell_cmd(pattern=r"shayri$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"shayri$", allow_sudo=True))
async def _(e):
    txt = random.choice(SHAYRI)
    await eor(e, txt.format(hell_mention))

@bot.on(hell_cmd(pattern=r"hflirt$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"hflirt$", allow_sudo=True))
async def _(e):
    txt = random.choice(HFLIRT)
    await eor(e, txt.format(hell_mention))

@bot.on(hell_cmd(pattern=r"eflirt$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"eflirt$", allow_sudo=True))
async def _(e):
    txt = random.choice(EFLIRT)
    await eor(e, txt.format(hell_mention))

@bot.on(hell_cmd(pattern=r"attitude$", outgoing=True))
@bot.on(sudo_cmd(pattern=r"attitude$", allow_sudo=True))
async def _(e):
    txt = random.choice(ATTITUDE)
    await eor(e, txt.format(hell_mention))

@bot.on(hell_cmd(pattern="gbye$", outgoing=True))
@bot.on(sudo_cmd(pattern="gbye$", allow_sudo=True))
async def _(e):
    txt = random.choice(GBYE)
    await eor(e, txt.format(hell_mention))

CmdHelp("randoms").add_command(
  'sing', None, 'Sings a song'
).add_command(
  'hps', None, 'Random harry porter character'
).add_command(
  'gott', None, 'Sends a random thought'
).add_command(
  'gotm', None, 'Sends a random meme'
).add_command(
  'bello', None, 'Sends quote for being logical'
).add_command(
  'tip', None, 'Sends you a life changer tip'
).add_command(
  'qt', None, 'Sends a random question. solve it if you can!!'
).add_command(
  'logic', None, 'Sends you a logical quote'
).add_command(
  'snow', None, 'Sends random quote from Game of thrones'
).add_command(
  'gbye', None, 'Sends random good bye quote'
).add_command(
  'attitude', None, 'Sends a random attitude quote.'
).add_command(
  'eflirt', None, 'Sends a random flirt quote in english'
).add_command(
  'hflirt', None, 'Sends a random flirt quote in hindi'
).add_command(
  'shayri', None, 'Sends a random heart touching quote'
).add_info(
  'Some Random Quotes.'
).add_warning(
  '✅ Harmless Module.'
).add()
