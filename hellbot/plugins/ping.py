from hellbot.utils.decorators import register

@register(pattern="ping$")
async def _(event):
    await eor(event, "Pong")
