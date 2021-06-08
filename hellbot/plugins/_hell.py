import asyncio
import datetime
import time

from telethon import Button, custom, events, version
from telethon.events import InlineQuery
from telethon.tl.custom import Button

from . import *

START_TIME = datetime.datetime.now()
uptime = f"{str(datetime.datetime.now() - START_TIME).split('.')[0]}"
alv_name = Config.YOUR_NAME or "Hêll"
my_channel = Config.MY_CHANNEL or "Its_HellBot"
my_group = Config.MY_GROUP or "HellBot_Chat"
if "@" in my_channel:
	my_channel = my_channel.replace("@", "")
if "@" in my_group:
	my_group = my_group.replace("@", "")


if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  
    async def in_alive(event):
        builder = event.builder
        result = None
        query = event.text
        me = await bot.get_me()
        alive_txt = f"""
**⚡ нєℓℓвσт ιѕ σиℓιиє ⚡**

{Config.ALIVE_MSG}

**🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅**

**Telethon :**  `{version.__version__}`
**Hêllẞø†  :**  **{hell_ver}**
**Uptime   :**  `{uptime}`
**Mode     :**  **{abuse_m}**
**Sudo     :**  **{is_sudo}**
"""
        if query.startswith("alive") and event.query.user_id == me.id:
            buttons = [
                [
                    Button.url(f"{alv_name}", f"tg://user?id={ForGo10God}")
                ],
                [
                    Button.url("My Channel", f"https://t.me/{my_channel}"),
                    Button.url("My Group", f"https://t.me/{my_group}"),
                ],
            ]
            if Config.ALIVE_PIC and Config.ALIVE_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    Config.ALIVE_PIC,
                    title="Alive",
                    text=alive_txt,
                    buttons=buttons,
                    link_preview=False
                )
            elif Config.ALIVE_PIC:
                result = builder.document(
                    Config.ALIVE_PIC,
                    title="Hêllẞø† Ãlívê",
                    text=alive_txt,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="Hêllẞø† Ãlívê",
                    text=alive_txt,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)

# test
