import random

import nekos
from WaifuPicsPython import WaifuAsync
from TelethonHell.plugins import *

neko_category = ['wallpaper', 'ngif', 'tickle', 'feed', 'gecg', 'gasm', 'slap', 'avatar', 'lizard', 'waifu', 'pat', '8ball', 'kiss', 'neko', 'spank', 'cuddle', 'fox_girl', 'hug', 'smug', 'goose', 'woof']
nsfw_list = ["waifu", "neko", "trap", "blowjob", "random"]
sfw_list = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe', 'random']


@hell_cmd(pattern="nsfw(?:\s|$)([\s\S]*)")
async def nsfw(event):
    x = await event.get_chat()
    y = x.id
    if y == 1496036895:
        return await parse_error(event, "Can't use this command here.")
    if abuse_m == "Disabled":
        return await eod(event, "**This command is only for users with variable** `ABUSE` **as** `ON`")
    lists = event.text.split(" ")
    category = None
    limit = 0
    if len(lists) == 1:
        category = "random"
        limit = 1
    elif len(lists) == 2 & lists[1].isdigit():
        category = "random"
        limit = lists[1].strip()
    elif len(lists) == 3:
        category = lists[1].strip()
        limit = lists[2].strip()
    else:
        category = lists[1].strip()
        limit = 1
    if int(limit) > 30:
        limit = 30
    if category not in nsfw_list:
        nsfw_cat = "Available categories are: \n"
        for n in nsfw_list:
            nsfw_cat += f"• `{n}` \n"
        txt = f"**Invalid category provided:** `{category}`\n\n{nsfw_cat}"
        return await eor(event, txt)
    waifu = WaifuAsync()
    pics = await waifu.nsfw(category, many=True)
    for p in range(int(limit)):
        await event.client.send_file(event.chat_id, file=pics[p])
    await event.delete()


@hell_cmd(pattern="sfw(?:\s|$)([\s\S]*)")
async def sfw(event):
    x = await event.get_chat()
    y = x.id
    if y == 1496036895:
        return await parse_error(event, "Can't use this command here.")
    lists = event.text.split(" ")
    category = None
    limit = 0
    if len(lists) == 1:
        category = "random"
        limit = 1
    elif len(lists) == 2 & lists[1].isdigit():
        category = "random"
        limit = lists[1].strip()
    elif len(lists) == 3:
        category = lists[1].strip()
        limit = lists[2].strip()
    else:
        category = lists[1].strip()
        limit = 1
    if int(limit) > 30:
        limit = 30
    if category not in sfw_list:
        sfw_cat = "Available categories are: \n"
        for s in sfw_list:
            sfw_cat += f"• `{s}` \n"
        txt = f"**Invalid category provided:** `{category}`\n\n{sfw_cat}"
        return await eor(event, txt)
    waifu = WaifuAsync()
    pics = await waifu.sfw(category, many=True)
    for p in range(int(limit)):
        await event.client.send_file(event.chat_id, file=pics[p])
    await event.delete()


@hell_cmd(pattern="nekos(?:\s|$)([\s\S]*)")
async def _(event):
    x = await event.get_chat()
    y = x.id
    if y == 1496036895:
        return await parse_error(event, "Can't use this command here.")
    if abuse_m == "Disabled":
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


CmdHelp("waifu").add_command(
    "nekos", "<category>", "Searches and sends some SFW & NSFW neko images/gifs according to category mentioned or sends a random NSFW/SFW image/gif."
).add_command(
    "nsfw", "<category> <limit>", "Sends NSFW pictures and GIFs. Category and Limit are optional."
).add_command(
    "sfw", "<category> <limit>", "Sends SFW pictures and GIFs."
).add_info(
    "Some NSFW Content."
).add_warning(
    "🔞 NSFW & SFW"
).add()
