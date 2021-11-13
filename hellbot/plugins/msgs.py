import string

from telethon.tl.types import Channel

from . import *

global msg_cache
global groupsid
msg_cache = {}
groupsid = []


async def all_groups_id(hell):
    hellgroups = []
    async for dialog in hell.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            hellgroups.append(entity.id)
    return hellgroups


@hell_cmd(pattern="frwd$")
async def _(event):
    if Config.LOGGER_ID is None:
        await eod(event, "Please set the required config `LOGGER_ID` for this plugin to work")
        return
    try:
        e = await event.client.get_entity(Config.LOGGER_ID)
    except Exception as e:
        await eor(event, str(e))
    else:
        re_message = await event.get_reply_message()
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        await event.delete()


@hell_cmd(pattern="resend$")
async def _(event):
    m = await event.get_reply_message()
    if not m:
        return
    await event.respond(m)
    await event.delete()


@hell_cmd(pattern="copy$")
async def _(event):
    m = await event.get_reply_message()
    if not m:
        return
    await event.client.send_message(event.chat_id, m, reply_to=m.id)
    await event.delete()


@hell_cmd(pattern="fpost(?:\s|$)([\s\S]*)")
async def _(event):
    global groupsid
    global msg_cache
    await event.delete()
    text = event.text[7:]
    destination = await event.get_input_chat()
    if len(groupsid) == 0:
        groupsid = await all_groups_id(event)
    for c in text.lower():
        if c not in string.ascii_lowercase:
            continue
        if c not in msg_cache:
            async for msg in event.client.iter_messages(event.chat_id, search=c):
                if msg.raw_text.lower() == c and msg.media is None:
                    msg_cache[c] = msg
                    break
        if c not in msg_cache:
            for i in groupsid:
                async for msg in event.client.iter_messages(event.chat_id, search=c):
                    if msg.raw_text.lower() == c and msg.media is None:
                        msg_cache[c] = msg
                        break
        await event.client.forward_messages(destination, msg_cache[c])


CmdHelp("msgs").add_command(
  "fpost", "<your msg>", "Checks all your groups and sends the msg matching the given keyword"
).add_command(
  "frwd", "<reply to a msg>", "Enables seen counter in replied msg. To know how many users have seen your msg."
).add_command(
  "resend", "<reply to a msg>", "Just resends the replied msg"
).add_command(
  "copy", "<reply to a msg>", "Resends the replied msg by replying to the original msg."
).add_info(
  "Messages tools."
).add_warning(
  "✅ Harmless Module."
).add()
