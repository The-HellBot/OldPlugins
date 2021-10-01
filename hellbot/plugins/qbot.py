from telethon.errors.rpcerrorlist import YouBlockedUserError


@hell_cmd(pattern="ss ?(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eod(event, "```Reply to any user's message.```")
        return
    reply_message = await event.get_reply_message()
    clr = event.text[4:]
    colour = clr.replace("'", "")
    limit = event.text[-2:]
    to_quote = []
    if limit and limit.isnumeric():
        to_quote.append(reply_message.id)
        async for to_qt in event.client.iter_messages(
            event.chat_id,
            limit=(int(limit) - 1),
            offset_id=reply_message.id,
            reverse=True,
        ):
            if to_qt.id != event.id:
                to_quote.append(to_qt.id)
    else:
        to_quote.append(reply_message.id)
    chat = "@QuotLyBot"
    hell = await eor(event, "```Making a Quote...```")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message(f"/qcolor {colour}")
            second = await conv.get_response()
            third = await event.client.forward_messages(chat, to_quote, event.chat_id)
            fourth = await conv.get_response()
        except YouBlockedUserError:
            await hell.edit("Please unblock @QuotLyBot and try again!!")
            return
        await hell.delete()
        await event.client.send_message(event.chat_id, fourth, reply_to=reply_message)
    q_d = []
    async for qdel in event.client.iter_messages(chat, min_id=first.id):
        q_d.append(first.id)
        q_d.append(qdel)
        await event.client.delete_messages(conv.chat_id, q_d)


CmdHelp("qbot").add_command(
  "ss", "<reply to msg> '<bg colour>' <number of msgs>", "Makes the sticker of the replied text, sticker, pic till next given count msgs.", "ss 'black' 05 <reply to a msg>"
).add_info(
  "Makes Quoted Sticker."
).add_warning(
  "✅ Harmless Module."
).add()
