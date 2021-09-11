

@hell_cmd.on(pattern="ping$")
async def _(event):
    await eor(event, "Pong")
