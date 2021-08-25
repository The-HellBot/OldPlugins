import json
import re
import requests

from telethon.errors.rpcerrorlist import ChatSendMediaForbiddenError

from . import *

FILLERS = {}

@bot.on(hell_cmd(pattern="anilist (.*)"))
@bot.on(sudo_cmd(pattern="anilist (.*)", allow_sudo=True))
async def anilist(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    event = await eor(event, "Searching...")
    result = await callAPI(input_str)
    hell = await formatJSON(result)
    title_img, msg = hell[0], hell[1]
    try:
        await event.client.send_file(event.chat_id, title_img, caption=msg, force_document=True)
        await event.delete()
        for files in (title_img):
            if files and os.path.exists(files):
                os.remove(files)
    except ChatSendMediaForbiddenError:
        await event.edit(msg, link_preview=True)


@bot.on(hell_cmd(pattern="anime(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="anime(?: |$)(.*)", allow_sudo=True))
async def nope(hel_):
    hell = hel_.pattern_match.group(1)
    if not hell:
        if hel_.is_reply:
            (await hel_.get_reply_message()).message
        else:
            await eod(hel_, "Sir please give some query to search and download it for you..!"
            )
            return

    troll = await bot.inline_query("AniFluidbot", f".anime {(deEmojify(hell))}")
    if troll:
        await hel_.delete()
        kraken = await troll[0].click(Config.LOGGER_ID)
        if kraken:
            await bot.send_message(
                hel_.chat_id,
                kraken,
            )
        await kraken.delete()
    else:
    	await eod(hel_, "**Error 404:**  Not Found")
    
    
@bot.on(hell_cmd(pattern="manga(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="manga(?: |$)(.*)", allow_sudo=True))
async def nope(hel_):
    hell = hel_.pattern_match.group(1)
    if not hell:
        if hel_.is_reply:
            (await hel_.get_reply_message()).message
        else:
            await eod(hel_, "Sir please give some query to search and download it for you..!"
            )
            return
    troll = await bot.inline_query("AniFluidbot", f".manga {(deEmojify(hell))}")
    if troll:
        await hel_.delete()
        kraken = await troll[0].click(Config.LOGGER_ID)
        if kraken:
            await bot.send_message(
                hel_.chat_id,
                kraken,
            )
        await kraken.delete()
    else:
    	await eod(hel_, "**Error 404:**  Not Found")
    
    

@bot.on(hell_cmd(pattern="character(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="character(?: |$)(.*)", allow_sudo=True))
async def nope(hel_):
    hell = hel_.pattern_match.group(1)
    if not hell:
        if hel_.is_reply:
            (await hel_.get_reply_message()).message
        else:
            await eod(hel_, "Sir please give some query to search and download it for you..!"
            )
            return
    troll = await bot.inline_query("AniFluidbot", f".character {(deEmojify(hell))}")
    if troll:
        await hel_.delete()
        kraken = await troll[0].click(Config.LOGGER_ID)
        if kraken:
            await bot.send_message(
                hel_.chat_id,
                kraken,
            )
        await kraken.delete()
    else:
    	await eod(hel_, "**Error 404:**  Not Found")
    


@bot.on(hell_cmd(pattern="fillers ?(.*)"))
@bot.on(sudo_cmd(pattern="fillers ?(.*)", allow_sudo=True))
async def canon(event):
    hell = event.text[9:]
    if hell == "":
        return await eor(event, "`Give anime name to search filler episodes.`")
    nub = await eor(event, f"Searching Filler Episodes For `{hell}`")
    hel_ = search_filler(hell)
    if hel_ == {}:
        return await nub.edit(f"No filler found for `{hell}`")
    list_ = list(hel_.keys())
    if len(list_) == 1:
        result = parse_filler(hel_.get(list_[0]))
        msg = ""
        msg += f"<h2>Fillers for {list_[0]} :</h2>\n\n<b>Manga Canon Episodes :</b>\n"
        msg += f'<code>{str(result.get("total_ep"))}</code>'
        msg += "\n\n<b>Mixed/Canon fillers :</b>\n"
        msg += f'<code>{str(result.get("mixed_ep"))}</code>'
        msg += "\n\n<b>Fillers :</b>\n"
        msg += f'<code>{str(result.get("filler_ep"))}</code>'
        if result.get("ac_ep") is not None:
            msg += "\n\n<b>Anime Canon episodes :</b>\n"
            msg += f'<code>{str(result.get("ac_ep"))}</code>'
        paste = await telegraph_paste(f"📃 Fillers List For “ {list_[0]} ”", msg)
        await nub.edit(f"**📃 Filler Episode List For [“ {list_[0]} ”]({paste}) !!**")
        return
    hellbot = f"**📃 Filler Episode Lists :** \n\n"
    for i in list_:
        result = parse_filler(hel_.get(i))
        msg = ""
        msg += f"<h2>Fillers for {i} :</h2>\n\n<b>Manga Canon Episodes :</b>\n"
        msg += f'<code>{str(result.get("total_ep"))}</code>'
        msg += "\n\n<b>Mixed/Canon fillers :</b>\n"
        msg += f'<code>{str(result.get("mixed_ep"))}</code>'
        msg += "\n\n<b>Fillers :</b>\n"
        msg += f'<code>{str(result.get("filler_ep"))}</code>'
        if result.get("ac_ep") is not None:
            msg += "\n\n<b>Anime Canon episodes :</b>\n"
            msg += f'<code>{str(result.get("ac_ep"))}</code>'
        paste = await telegraph_paste(f"📃 Fillers List For “ {i} ”", msg)
        hellbot += f"• [{i}]({paste})\n"
    await nub.edit(hellbot)


@bot.on(hell_cmd(pattern="airing ?(.*)"))
@bot.on(sudo_cmd(pattern="airing ?(.*)", allow_sudo=True))
async def _(event):
    query = event.text[8:]
    hell = await eor(event, f"__Searching airing details for__ `{query}`")
    if query == "":
        return await eod(hell, "Give anime name to seaech airing information.")
    vars_ = {"search": query}
    if query.isdigit():
        vars_ = {"id": int(query), "asHtml": True}
    result = await get_airing(vars_)
    if len(result) == 1:
        return await eor(event, result[0])
    coverImg, out = result[0]
    await event.client.send_file(event.chat_id, coverImg, caption=out, force_document=False)
    await hell.delete()
    for files in (coverImg):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(hell_cmd(pattern="aniquote$"))
@bot.on(sudo_cmd(pattern="aniquote$", allow_sudo=True))
async def quote(event):
    hell = await eor(event, "(ﾉ◕ヮ◕)ﾉ*.✧")
    q = requests.get("https://animechan.vercel.app/api/random").json()
    await asyncio.sleep(1.5)
    await hell.edit("`"+q["quote"]+"`\n\n—  **"+q["character"]+"** (From __"+q["anime"]+"__)") #dimag ka bhosda hogya bc yha pe (*﹏*;)


CmdHelp("anime").add_command(
  "anime", "<anime name>", "Searches for the given anime and sends the details.", "anime violet evergarden"
).add_command(
  "manga", "<manga name>", "Searches for the given manga and sends the details.", "manga Jujutsu kaisen"
).add_command(
  "character", "<character name>", "Searches for the given anime character and sends the details.", "character Mai Sakurajima"
).add_command(
  "anilist", "<anime name>", "Searches Details of the anime directly from anilist", "anilist attack on titan"
).add_command(
  "fillers", "<anime name>", "Searches for the filler episodes of given Anime.", "fillers Naruto"
).add_command(
  "aniquote", None, "Gives a random quote from Anime."
).add_info(
  "Anime Search"
).add_warning(
  "✅ Harmless Module."
).add()
