from hellbot.utils.decorators import on, hell_cmd

@on(hell_cmd(pattern="ping$"))
async def _(event):
    await eor(event, "Pong")
