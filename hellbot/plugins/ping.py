import asyncio
import datetime
from datetime import datetime

from . import *

@bot.on(hell_cmd(pattern="ping$"))
@bot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(hell):
    if hell.fwd_from:
        return
    start = datetime.now()
    event = await eor(hell, "`·.·★ ℘ıŋɠ ★·.·´")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"╰•★★  ℘ơŋɠ ★★•╯\n\n    ⚘  {ms}\n    ⚘  __**Oɯɳҽɾ**__ **:** {hell_mention}"
    )


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your Hêllẞø†"
).add_warning(
  "✅ Harmless Module"
).add()
