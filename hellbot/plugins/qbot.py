from telethon.errors.rpcerrorlist import YouBlockedUserError


@hell_cmd(pattern="ss ?(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "```Reply to any user's message.```")
        return
    reply_message = await event.get_reply_message()
    colour = event.text[4:] or "#1b1429"
    chat = "@QuotLyBot"
    hell = await eor(event, "```Making a Quote...```")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message(f"/qcolor {colour}")
            second = await conv.get_response()
            third = await event.client.forward_messages(reply_message)
            fourth = await conv.get_response()
        except YouBlockedUserError:
            await hell.edit("Please unblock @QuotLyBot and try again!!")
            return
        await hell.delete()
        await event.client.forward_messages(event.chat_id, fourth)
    await event.client.delete_messages(
        conv.chat_id, [first.id, second.id, third.id, fourth.id]
    )

CmdHelp("qbot").add_command(
  "ss", "<reply to msg> <bg colour>", "Makes the sticker of the replied text, sticker, pic.", "ss black <reply to a msg>"
).add_info(
  "Makes Quoted Sticker."
).add_warning(
  "✅ Harmless Module."
).add()
