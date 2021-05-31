from . import *

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

    await troll[0].click(
        hel_.chat_id,
        reply_to=hel_.reply_to_msg_id,
        silent=True if hel_.is_reply else False,
        hide_via=True,
    )
    await hel_.delete()
    
    
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

    await troll[0].click(
        hel_.chat_id,
        reply_to=hel_.reply_to_msg_id,
        silent=True if hel_.is_reply else False,
        hide_via=True,
    )
    await hel_.delete()
    

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

    await troll[0].click(
        hel_.chat_id,
        reply_to=hel_.reply_to_msg_id,
        silent=True if hel_.is_reply else False,
        hide_via=True,
    )
    await hel_.delete()


CmdHelp("anime").add_command(
  "anime", "<anime name>", "Searches for the given anime and sends the details.", "anime violet evergarden"
).add_command(
  "manga", "<manga name>", "Searches for the given manga and sends the details.", "manga Jujutsu kaisen"
).add_command(
  "character", "<character name>", "Searches for the given anime character and sends the details.", "character Mai Sakurajima"
).add_info(
  "Anime Search"
).add_warning(
  "✅ Harmless Module."
).add()
