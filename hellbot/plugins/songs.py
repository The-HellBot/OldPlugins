import asyncio
from . import *

@bot.on(hell_cmd(pattern="lyrics(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="lyrics(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.text[8:]
    uwu = await eor(kraken, f"Searching lyrics for  `{hell}` ...")
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(uwu, "Give song name to get lyrics...")
            return
    troll = await bot.inline_query("iLyricsBot", f"{(deEmojify(hell))}")
    if troll:
        owo = await troll[0].click(Config.LOGGER_ID)
        hmm = await owo.get_edit()
        await uwu.edit(hmm.message)
        await owo.delete()
    else:
        await uwu.edit("**ERROR 404 :** __NOT FOUND__")


@bot.on(hell_cmd(pattern="lsong ?(.*)"))
@bot.on(sudo_cmd(pattern="lsong ?(.*)", allow_sudo=True))
async def _(event):
    hell_ = event.text[4:]
    if hell_ == "":
        return await eor(event, "Give a song name to search")
    hell = await eor(event, f"Searching song `{hell_}`")
    somg = await event.client.inline_query("Lybot", f"{(deEmojify(hell_))}")
    if somg:
        fak = await somg[0].click(Config.LOGGER_ID)
        if fak:
            await bot.send_file(
                event.chat_id,
                file=fak,
                caption=f"**Song by :** {hell_mention}",
            )
        await hell.delete()
        await fak.delete()
    else:
        await hell.edit("**ERROR 404 :** __NOT FOUND__")


CmdHelp("songs").add_command(
  "song", "<song name>", "Downloads the song from YouTube."
).add_command(
  "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
  "lsong", "<song name>", "Sends the searched song in current chat.", "lsong Alone"
).add_command(
  "lyrics", "<song name>", "Gives the lyrics of that song.."
).add_info(
  "Songs & Lyrics."
).add_warning(
  "✅ Harmless Module."
).add()
