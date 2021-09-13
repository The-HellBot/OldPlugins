from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@hell_cmd(pattern="ascii ?(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to any user message.😒🤐")
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        return await eor(event, "Reply to media message😒🤐")
    bot = "@asciiart_bot"
    kraken = await eor(event, "Wait making ASCII...🤓🔥🔥")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(reply_message)
            output_op = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kraken.edit("User Blocked!! Please Unblock @asciiart_bot and try again...")
            return
    await event.client.send_file(event.chat_id, file=output_op, caption=f"ASCII art By :- {hell_mention}", force_document=False)
    await kraken.delete()  
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, output_op.id]
    )

@hell_cmd(pattern="line ?(.*)")
async def _(event):
    if not event.reply_to_msg_id:
        await eor(event, "Reply to any user message.😒🤐")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eor(event, "Reply to media message😒🤐")
        return
    bot = "@lines50bot"
    kraken = await eor(event, "`Processing...`")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(reply_message)
            output_op = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await kraken.edit("User Blocked!! Please Unblock @Lines50Bot and try again...")
            return
    await event.client.send_file(event.chat_id, file=output_op, caption=f"Lines By :- {hell_mention}", force_document=False)
    await kraken.delete()
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, output_op.id]
    )


CmdHelp("ascii").add_command(
  'ascii', 'reply to any image file', 'Makes an image ascii style, try out your own'
).add_command(
  'line', 'reply to any image file', 'Makes an image in line style'
).add_info(
  'Lines And Ascii'
).add_warning(
  '✅ Harmless Module.'
).add()
