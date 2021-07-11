import re
from . import *

# Credits to @ForGo10God developer of HellBot.
# This is my first plugin that I made when I released first HellBot.
# Modified to work in groups with inline mode disabled.
# Added error msg if no voice is found.
# So please dont remove credit. 
# You can use it in your repo. But dont remove these lines...

@bot.on(d3vil_cmd(pattern="mev(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="mev(?: |$)(.*)", allow_sudo=True))
async def nope(d3vilkrish):
    d3vil = d3vilkrish.pattern_match.group(1)
    if not d3vil:
        if d3vilkrish.is_reply:
            (await d3vilkrish.get_reply_message()).message
        else:
            await edit_or_reply(d3vilkrish, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("TrollVoiceBot", f"{(deEmojify(d3vil))}")
    if troll:
        await d3vilkrish.delete()
        d3vl_ = await troll[0].click(Config.LOGGER_ID)
        if d3vl_:
            await bot.send_file(
                d3vilkrish.chat_id,
                d3vl_,
                caption="",
            )
        await d3vl_.delete()
    else:
    	await eod(d3vilkrish, "**Error 404:**  Not Found")
    	
@bot.on(d3vil_cmd(pattern="meev(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="meev(?: |$)(.*)", allow_sudo=True))
async def nope(d3vilkrish):
    d3vil = d3vilkrish.pattern_match.group(1)
    if not d3vil:
        if d3vilkrish.is_reply:
            (await d3vilkrish.get_reply_message()).message
        else:
            await edit_or_reply(d3vilkrish, "`Sir please give some query to search and download it for you..!`"
            )
            return

    troll = await bot.inline_query("Myinstantsbot", f"{(deEmojify(d3vil))}")
    if troll:
        await d3vilkrish.delete()
        d3vl_ = await troll[0].click(Config.LOGGER_ID)
        if d3vl_:
            await bot.send_file(
                d3vilkrish.chat_id,
                d3vl_,
                caption="",
            )
        await d3vl_.delete()
    else:
    	await eod(d3vilkrish, "**Error 404:**  Not Found")


CmdHelp("memevoice").add_command(
	"mev", "<query>", "Searches the given meme and sends audio if found."
).add_command(
	"meev", "<query>", "Same as {hl}mev"
).add_info(
	"Audio Memes."
).add_warning(
	"✅ Harmless Module."
).add()
