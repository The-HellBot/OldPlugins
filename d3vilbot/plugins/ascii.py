from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@bot.on(d3vil_cmd(pattern="ascii (.*)"))
@bot.on(sudo_cmd(pattern="ascii (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user message.😒🤐")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "Reply to media message😒🤐")
        return
    bot = "@asciiart_bot"
    d3vilkrish = await eor(event, "Wait making ASCII...🤓🔥🔥")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(reply_message)
            output_op = await conv.get_response()
            last = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await d3vilkrish.edit("User Blocked!! Please Unblock @asciiart_bot and try again...")
            return
        await d3vilkrish.delete()
        final = await event.client.send_file(
            event.chat_id,
            output_op,
        )
        await final.edit(
            f"ASCII art By :- {d3vil_mention}")
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, output_op.id, last.id]
    )

@bot.on(d3vil_cmd(pattern="line (.*)"))
@bot.on(sudo_cmd(pattern="line (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user message.😒🤐")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "Reply to media message😒🤐")
        return
    bot = "@lines50bot"
    d3vilkrish = await eor(event, "`Processing...`")
    async with event.client.conversation(bot) as conv:
        try:
            first = await conv.send_message("/start")
            response = await conv.get_response()
            second = await conv.send_message(reply_message)
            output_op = await conv.get_response()
            last = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await d3vilkrish.edit("User Blocked!! Please Unblock @Lines50Bot and try again...")
            return
        await d3vilkrish.delete()
        final = await event.client.send_file(
            event.chat_id,
            output_op,
        )
        await final.edit(
            f"Lines By :- {d3vil_mention}")
    await event.client.delete_messages(
        conv.chat_id, [first.id, response.id, second.id, output_op.id, last.id]
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
