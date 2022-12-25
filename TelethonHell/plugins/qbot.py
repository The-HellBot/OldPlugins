from telethon.errors.rpcerrorlist import YouBlockedUserError
from TelethonHell.plugins import *


@hell_cmd(pattern="ss(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await parse_error(event, "Reply to a message to quote it.")
    hell = await eor(event, "`Making a Quote ...`")
    reply_message = await event.get_reply_message()
    clr = event.text[4:]
    colour = "#292232"
    limit = None
    if "'" in clr:
        lists = clr.split("'")
        colour = lists[1].strip()
        limit = lists[2].strip() or None
    limit = event.text[-2:].strip()
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
    async with event.client.conversation("@QuotLyBot") as conv:
        try:
            first = await conv.send_message(f"/qemoji 👻")
            second = await conv.get_response()
            third = await conv.send_message(f"/qcolor {colour}")
            fourth = await conv.get_response()
            await event.client.forward_messages("@QuotLyBot", to_quote, event.chat_id)
            fifth = await conv.get_response()
        except YouBlockedUserError:
            return await parse_error(hell, "__Unblock @QuotLyBot and try again.__", False)
        await hell.delete()
        await event.client.send_message(event.chat_id, fifth, reply_to=reply_message)
        q_d = []
        async for qdel in event.client.iter_messages("@QuotLyBot", min_id=first.id):
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
