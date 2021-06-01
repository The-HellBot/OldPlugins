from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *

@bot.on(hell_cmd(pattern="circle ?(.*)"))
@bot.on(sudo_cmd(pattern="circle ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user message")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "Reply to media message")
        return
    chat = "@TelescopyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await edit_or_reply(event, "Reply to actual users message.")
        return
    kraken = await edit_or_reply(event, "Trying to convert...")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=397367589)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await kraken.edit("```Please unblock @TelescopyBot and try again```")
            return
        if response.text.startswith("Send me square Video"):
            await kraken.edit(
                "Currently only square videos are converted into circle video..."
            )
        elif response.text.startswith("File is too big!"):
            await kraken.edit(
                "File size more than 8mb. Reply to a square video less than 8mb."
            )
        else:
            await kraken.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
            )
            await event.client.send_read_acknowledge(conv.chat_id)

CmdHelp("circle").add_command(
  "circle", "<reply to a 4×4(square) media>", "Converts the replied square media into circle telegram video"
).add_info(
  "Telegram Circle Video"
).add_warning(
  "✅ Harmless Module."
).add()
