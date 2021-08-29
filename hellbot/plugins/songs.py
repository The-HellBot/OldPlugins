import asyncio

from telethon.errors.rpcerrorlist import YouBlockedUserError

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
    owo = await troll[0].click(Config.LOGGER_ID)
    await asyncio.sleep(3)
    owo_id = owo.id
    lyri = await bot.get_messages(entity=Config.LOGGER_ID, ids=owo_id)
    await bot.send_message(kraken.chat_id, lyri)
    await uwu.delete()
    await owo.delete()


@bot.on(hell_cmd(pattern="lsong ?(.*)"))
@bot.on(sudo_cmd(pattern="lsong ?(.*)", allow_sudo=True))
async def _(event):
    hell_ = event.text[6:]
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


@bot.on(hell_cmd(pattern="wsong ?(.*)"))
async def _(event):
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to a mp3 file.")
    rply = await event.get_reply_message()
    chat = "@auddbot"
    hell = await eor(event, "Trying to identify song...")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            third = await conv.send_message(rply)
            fourth = await conv.get_response()
            if not fourth.text.startswith("Audio received"):
                await hell.edit(
                    "Error identifying audio."
                )
                await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id])
                return
            await hell.edit("Processed...")
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await hell.edit("Please unblock @auddbot and try again")
    audio = f"**Song Name : **{fifth.text.splitlines()[0]}\n\n**Details : **__{result.text.splitlines()[2]}__"
    await hell.edit(audio)
    await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id])


CmdHelp("songs").add_command(
  "song", "<song name>", "Downloads the song from YouTube."
).add_command(
  "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
  "lsong", "<song name>", "Sends the searched song in current chat.", "lsong Alone"
).add_command(
  "wsong", "<reply to a song file>", "Searches for the details of replied mp3 song file and uploads it's details."
).add_command(
  "lyrics", "<song name>", "Gives the lyrics of that song.."
).add_info(
  "Songs & Lyrics."
).add_warning(
  "✅ Harmless Module."
).add()
