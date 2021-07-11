import datetime
from d3vilbot import *
from d3vilbot.config import Config
from d3vilbot.d3vlpers import *
from d3vilbot.utils import *
from d3vilbot.random_strings import *
from d3vilbot.version import __d3vil__
from telethon import version


D3VIL_USER = bot.me.first_name
d3krish = bot.uid
d3vil_mention = f"[{D3VIL_USER}](tg://user?id={d3krish})"
d3vil_logo = "./d3vilbot/resources/pics/d3vilbot_logo.jpg"
cjb = "./d3vilbot/resources/pics/cjb.jpg"
restlo = "./d3vilbot/resources/pics/rest.jpeg"
shuru = "./d3vilbot/resources/pics/shuru.jpg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
d3vil_ver = __d3vil__
tel_ver = version.__version__

async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid

sudos = Config.SUDO_USERS
if sudos:
    is_sudo = "True"
else:
    is_sudo = "False"

abus = Config.ABUSE
if abus == "ON":
    abuse_m = "Enabled"
else:
    abuse_m ="Disabled"

START_TIME = datetime.datetime.now()
uptime = f"{str(datetime.datetime.now() - START_TIME).split('.')[0]}"
my_channel = Config.MY_CHANNEL or "D3VIL_SUPPORT"
my_group = Config.MY_GROUP or "D3VIL_BOT_SUPPORT"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/D3VIL_SUPPORT"
d3vil_channel = f"[тнε ∂3vιℓ вσт υρ∂αтεs]({chnl_link})"
grp_link = "https://t.me/D3VIL_BOT_SUPPORT"
d3vil_grp = f"[тнε ∂3vιℓ вσт cнαт]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {mention} :  To mention the user
  {title} : To get chat name in message
  {count} : To get group members
  {first} : To use user first name
  {last} : To use user last name
  {fullname} : To use user full name
  {userid} : To use userid
  {username} : To use user username
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
"""
# will add more soon


