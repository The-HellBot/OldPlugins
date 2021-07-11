import asyncio
import datetime

from . import *

@bot.on(d3vil_cmd(pattern="ping$"))
@bot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(d3vil):
    if d3vil.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(d3vil, "`·.·★ ℘ıŋɠ ★·.·´")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"╰•★★  ℘ơŋɠ ★★•╯\n\n    ⚘  `{ms}`\n    ⚘  __**Oɯɳҽɾ**__ **:**  {d3vil_mention}"
    )


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your Hêllẞø†"
).add_warning(
  "✅ Harmless Module"
).add()

# d3vilbot
