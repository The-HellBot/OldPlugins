import asyncio
import datetime
import time

from . import *

ping_txt = """<b><i>╰•★★  ℘ơŋɠ ★★•╯</b></i>

    ⚘  <i>ʂ℘ɛɛɖ :</i> <code>{}</code>
    ⚘  <i>ų℘ɬıɱɛ :</i> <code>{}</code>
    ⚘  <i>ơῳŋɛཞ :</i> {}"""

@hell_cmd(pattern="ping$")
async def pong(hell):
    start = datetime.datetime.now()
    event = await eor(hell, "`·.·★ ℘ıŋɠ ★·.·´")
    cid = await client_id(event)
    ForGo10God, HELL_USER = cid[0], cid[1]
    hell_mention = f"<a href='tg://user?id={ForGo10God}'>{HELL_USER}</a>"
    uptime = await get_time((time.time() - StartTime))
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(ping_txt.format(ms, uptime, hell_mention), parse_mode="HTML")


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your Hêllẞø†"
).add_warning(
  "✅ Harmless Module"
).add()

# hellbot
