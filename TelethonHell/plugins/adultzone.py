import random
import nekos

from . import *

neko_category = [
    'wallpaper',
    'ngif',
    'tickle',
    'feed',
    'gecg',
    'gasm',
    'slap',
    'avatar',
    'lizard',
    'waifu',
    'pat',
    '8ball',
    'kiss',
    'neko',
    'spank',
    'cuddle',
    'fox_girl',
    'hug',
    'smug',
    'goose',
    'woof',
]


@hell_cmd(pattern="nekos(?:\s|$)([\s\S]*)")
async def _(event):
    x = await event.get_chat()
    y = x.id
    if y == 1496036895:
        return await parse_error(event, "Can't use this command here.")
    if Config.ABUSE != "ON":
        return await eod(
            event,
            "**This command is only for users with variable** `ABUSE` **as** `ON`",
        )
    owo = event.text[7:]
    if owo in neko_category:
        hell = await eor(event, f"`Searching {owo} ...`")
        link = nekos.img(owo)
        x = await event.client.send_file(event.chat_id, link, force_document=False)
        await hell.delete()
        if link.endswith((".gif")):
            await unsave_gif(event, x)
    elif owo == "":
        hell = await eor(event, "`Searching randoms...`")
        uwu = random.choice(neko_category)
        link = nekos.img(uwu)
        x = await event.client.send_file(event.chat_id, link, force_document=False)
        await hell.delete()
        if link.endswith((".gif")):
            await unsave_gif(event, x)
    else:
        out = ""
        for x in neko_category:
            out += f"• `{x}` \n"
        await eor(
            event,
            f"**Invalid Argument. Choose from these:**\n\n{out}",
        )


CmdHelp("adultzone").add_command(
    "nekos", "<category>", "Searches and sends some SFW & NSFW neko images/gifs according to category mentioned or sends a random NSFW/SFW image/gif."
).add_info(
    "Some NSFW Content."
).add_warning(
    "🔞 NSFW"
).add()
