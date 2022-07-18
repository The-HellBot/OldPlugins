from . import *


@hell_cmd(pattern="mev(?:\s|$)([\s\S]*)")
async def _(event):
    hell = event.text[5:]
    rply = await event.get_reply_message()
    if not hell:
        return await parse_error(event, "Nothing given to search.")
    troll = await event.client.inline_query("TrollVoiceBot", f"{(deEmojify(hell))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
                reply_to=rply,
            )
        await hel_.delete()
    else:
        await parse_error(event, "__404:__ Not Found", False)


@hell_cmd(pattern="mev2(?:\s|$)([\s\S]*)")
async def _(event):
    hell = event.text[6:]
    rply = await event.get_reply_message()
    if not hell:
        return await parse_error(event, "Nothing given to search.")
    troll = await event.client.inline_query("Myinstantsbot", f"{(deEmojify(hell))}")
    if troll:
        await event.delete()
        hel_ = await troll[0].click(Config.LOGGER_ID)
        if hel_:
            await event.client.send_file(
                event.chat_id,
                hel_,
                caption="",
                reply_to=rply,
            )
        await hel_.delete()
    else:
        await parse_error(event, "__404:__  Not Found", False)


CmdHelp("memevoice").add_command(
    "mev", "<query>", "Searches the given meme and sends audio if found."
).add_command(
    "mev2", "<query>", f"Same as {hl}mev but with different bot server."
).add_info(
    "Audio Memes."
).add_warning(
    "✅ Harmless Module."
).add()
