import telethon.utils

from . import client_id


@hell_cmd(pattern="ping$")
async def p(event):
    x = await client_id(event)
    ForGo10God, HELL_USER, hell_mention = x[0], x[1], x[2]
    await eor(event, f"**Pong !!**\n\n{ForGo10God} \n\n{HELL_USER} \n\n{hell_mention}")
