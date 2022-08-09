import datetime
import time

from HellConfig import Config, db_config, os_config
from TelethonHell import *
from TelethonHell.clients import *
from TelethonHell.DB.gvar_sql import gvarstat
from TelethonHell.helpers import *
from TelethonHell.strings import *
from TelethonHell.utils import *
from TelethonHell.version import __hellver__, __telever__

hell_logo = "./HellConfig/resources/pics/hellbot_logo.jpg"
cjb = "./HellConfig/resources/pics/cjb.jpg"
restlo = "./HellConfig/resources/pics/rest.jpeg"
shuru = "./HellConfig/resources/pics/shuru.jpg"
shhh = "./HellConfig/resources/pics/chup_madarchod.jpeg"
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
hell_ver = __hellver__
tel_ver = __telever__


async def get_user_id(ids):
    if str(ids).isdigit():
        userid = int(ids)
    else:
        userid = (await bot.get_entity(ids)).id
    return userid


is_sudo = "True" if gvarstat("SUDO_USERS") else "False"

abus = Config.ABUSE
if abus == "ON":
    abuse_m = "Enabled"
else:
    abuse_m = "Disabled"


my_channel = Config.MY_CHANNEL or "Its_HellBot"
my_group = Config.MY_GROUP or "HellBot_Chat"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/its_hellbot"
hell_channel = f"[†hê Hêllẞø†]({chnl_link})"
grp_link = "https://t.me/HellBot_Chat"
hell_grp = f"[Hêllẞø† Group]({grp_link})"

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

# TelethonHell
