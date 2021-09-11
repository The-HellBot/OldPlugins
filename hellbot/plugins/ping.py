

@on(hell_cmd(pattern="ping$"))
async def _(event):
    await eor(event, "Pong")
