from asyncio import sleep

from telethon.errors import rpcbaseerrors

from . import *


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


@hell_cmd(pattern="purge(?:\s|$)([\s\S]*)")
@errors_handler
async def fastpurger(event):
    hell = event.text[7:]
    what = hell.split(" ", 1)[0]

    if what == "-me":
        count = int(hell.split(" ", 1)[1])
        if count:
            i = 1
            async for message in event.client.iter_messages(event.chat_id, from_user="me", min_id=event.reply_to_msg_id):
                if i > count + 1:
                    break
                i += 1
                await message.delete()
        else:
            msg = []
            count = 0
            async for message in event.client.iter_messages(event.chat_id, from_user="me", min_id=event.reply_to_msg_id):
                msg.append(message)
                count += 1
                msg.append(event.reply_to_msg_id)
                if len(msg) == 100:
                    await event.client.delete_messages(event.chat_id, msg)
                    msg = []
            if msg:
                await event.client.delete_messages(event.chat_id, msg)
        done = await event.client.send_message(event.chat_id, f"**Self Purge Completed!!** Purged `{str(count)}` messages.")

        await event.client.send_message(Config.LOGGER_ID, f"#PURGE \nSelf Purged `{str(count)}` messages.")
        await sleep(5)
        await done.delete()

    elif what == "-user":
        count = int(hell.split(" ", 1)[1])
        user_ = (await event.get_reply_message()).from_id.user_id
        user = await event.client.get_entity(user_)
        if not user:
            return await eod(event, "Reply to a user to purge his/her messages.")
        if count:
            i = 1
            async for message in event.client.iter_messages(event.chat_id, from_user=user.id, min_id=event.reply_to_msg_id):
                if i > count + 1:
                    break
                i += 1
                await message.delete()
        else:
            msg = []
            count = 0
            async for message in event.client.iter_messages(event.chat_id, from_user=user.id, min_id=event.reply_to_msg_id):
                msg.append(message)
                count += 1
                msg.append(event.reply_to_msg_id)
                if len(msg) == 100:
                    await event.client.delete_messages(event.chat_id, msg)
                    msg = []
            if msg:
                await event.client.delete_messages(event.chat_id, msg)
        done = await event.client.send_message(event.chat_id, f"**Purge Completed!!** Purged `{str(count)}` messages of [{user.first_name}](tg://user?id={user.id})")

        await event.client.send_message(Config.LOGGER_ID, f"#PURGE \nPurged `{str(count)}` messages of [{user.first_name}]({user.id})")
        await sleep(5)
        await done.delete()

    else:
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
        done = await event.client.send_message(event.chat_id, f"**Purge Completed!** \nPurged `{str(count)}` messages.")
        await event.client.send_message(Config.LOGGER_ID, f"#PURGE\n\nPurged `{str(count)}` messages.")
        await sleep(5)
        await done.delete()


@hell_cmd(pattern="sd$")
@errors_handler
async def selfdestruct(event):
    lg_id = Config.LOGGER_ID
    message = event.text[4:]
    splt = message.split("|")
    counter = int(splt[0])
    text = str(splt[1])
    await event.delete()
    smsg = await event.client.send_message(event.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    await event.client.send_message(
        lg_id,
        f"#SELF_DESTRUCT \n\nSelf Destruct message query done successfully!\n\n**SD Msg :**  `{text}`",
    )


CmdHelp("purger").add_command(
    "purge", "<reply from a msg>", "Purges all the messages from replied message."
).add_command(
    "purge -me", "<count> or <reply>", "Purges the required number of your messages", "purge -me 100"
).add_command(
    "purge -user", "<reply> <count>", "Purges the messages of replied user from replied message.", "purge -user 50"
).add_command(
    "sd", "<time> | <text>", "Sends a self destruct text. Fill time in secs", "sd 10 | hello"
).add_command(
    "del", "<reply>", "Deletes the replied msg."
).add_info(
    "Ninja Techniques"
).add_warning(
    "✅ Harmless Module."
).add()
