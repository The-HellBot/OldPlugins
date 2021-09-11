from . import ForGo10God, HELL_USER

@hell_cmd(pattern="ping$")
async def _(event):
    await eor(event, f"Pong \n\n{ForGo10God}\n\n{HELL_USER}")
