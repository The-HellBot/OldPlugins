from telethon.tl.functions.messages import SaveDraftRequest

from . import *

@bot.on(hell_cmd(pattern="chain$"))
@bot.on(sudo_cmd(pattern="chain$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = await eor(event, "Counting...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await hell.edit(f"⛓️ **Chain length :**  `{count}`")


CmdHelp("chain").add_command(
  "chain", "Reply to a message", "Reply this command to any msg so that it finds chain length of that msg"
).add_info(
  "Chained Messages."
).add_warning(
  "✅ Harmless Module."
).add()
