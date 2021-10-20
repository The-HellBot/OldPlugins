from asyncio import sleep
from telethon.errors import rpcbaseerrors

from . import *

lg_id = Config.LOGGER_ID


@hell_cmd(pattern="del$")
@errors_handler
async def delete_it(event):
    msg_src = await event.get_reply_message()
    if event.reply_to_msg_id:
        try:
            await msg_src.delete()
            await event.delete()
        except rpcbaseerrors.BadRequestError:
        	pass


@hell_cmd(pattern=r"purge$")
@errors_handler
async def fastpurger(event):
    chat = await event.get_input_chat()
    msgs = []
    count = 0

    async for msg in event.client.iter_messages(chat, min_id=event.reply_to_msg_id):
        msgs.append(msg)
        count = count + 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await event.client.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await event.client.delete_messages(chat, msgs)
    done = await event.client.send_message(
        event.chat_id,
        "**Fast Purge Completed!** \nPurged `" + str(count) + "` messages.",
    )

    await event.client.send_message(
        lg_id, 
        "#PURGE\n\nPurged `" + str(count) + "` messages."
        )
    await sleep(4)
    await done.delete()


@hell_cmd(pattern="purgeme$")
@errors_handler
async def purgeme(event):
    message = event.text
    count = int(message[9:])
    i = 1

    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        "**Self Purge Complete!** Purged  `" + str(count) + "`  messages.",
    )
    await event.client.send_message(
        lg_id, "#PURGE \nSelf Purged  `" + str(count) + "`  messages."
    )
    await sleep(4)
    i = 1
    await smsg.delete()


@hell_cmd(pattern="sd$")
@errors_handler
async def selfdestruct(event):
    message = event.text[4:]
    splt = message.split("|")
    counter = int(splt[0])
    text = str(splt[1])
    await event.delete()
    smsg = await event.client.send_message(event.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    await event.client.send_message(lg_id, f"#SELF_DESTRUCT \n\nSelf Destruct message query done successfully!\n\n**SD Msg :**  `{text}`")
        

CmdHelp("purger").add_command(
  "purge", "<reply from a msg>", "Purges all the messages from replied message."
).add_command(
  "purgeme", "<no.of msgs>", "Purges the required number of your messages", "purgeme 100"
).add_command(
  "sd", "<time> | <text>", "Sends a self destruct text. Fill time in secs", "sd 10 | hello"
).add_command(
  "del", "<reply>", "Deletes the replied msg."
).add_info(
  "Ninja Techniques"
).add_warning(
  "✅ Harmless Module."
).add()
