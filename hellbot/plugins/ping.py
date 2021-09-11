from hellbot.utils.decorators import hell_cmd

@hell_cmd(pattern="ping$")
async def _(event):
    await eor(event, "Pong")
