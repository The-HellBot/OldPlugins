import nekos
import os
import random

from . import *

neko_category = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof']

@hell_cmd(pattern="nekos ?(.*)")
async def _(event):
    x = await event.get_chat()
    y = x.id

    if y == 1496036895:
        return await eor(event, "Can't use this command here.")

    if Config.ABUSE != "ON":
        return await eor(event, "**This command is only for users with heroku variable** `ABUSE` **as** `ON`")
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
        await eor(event, f"**Unmatched argument.** \n\n__Get all the required queries for nekos here__ -> **[Nekos Queries](http://telegra.ph/Nekos-Queries-08-20)**")


CmdHelp("adultzone").add_command(
  "nekos", "<category>", "Searches and sends some SFW & NSFW neko images/gifs according to category mentioned or sends a random NSFW/SFW image/gif."
).add_info(
  "Some NSFW Content."
).add_warning(
  "🔞 NSFW content."
).add()
