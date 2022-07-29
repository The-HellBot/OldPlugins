import time

from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

from . import *


@hell_cmd(pattern="stats$")
async def stats(event):
    hell = await eor(event, "`Collecting stats...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1
            elif entity.megagroup:
                groups += 1
                if entity.creator or entity.admin_rights:
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1
        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    ForGo10God, HELL_USER, _ = await client_id(event)
    hell_mention = f"<a href='tg://user?id={ForGo10God}'>{HELL_USER}</a>"
    response = f"<b><i><u>♛ Stats for {hell_mention} ♛</b></i></u>\n\n"
    response += f"<b>◈ Private Chats:</b> <code>{private_chats}</code> \n"
    response += f"    <i>○ Users:</i> <code>{private_chats - bots}</code> \n"
    response += f"    <i>○ Bots:</i> <code>{bots}</code> \n"
    response += f"<b>◈ Groups:</b> <code>{groups}</code> \n"
    response += f"<b>◈ Channels:</b> <code>{broadcast_channels}</code> \n"
    response += f"<b>◈ Admin Groups:</b> <code>{admin_in_groups}</code> \n"
    response += f"    <i>○ Creator:</i> <code>{creator_in_groups}</code> \n"
    response += f"    <i>○ Admin Rights:</i> <code>{admin_in_groups - creator_in_groups}</code> \n"
    response += f"<b>◈ Admin Channels:</b> <code>{admin_in_broadcast_channels}</code> \n"
    response += f"    <i>○ Creator:</i> <code>{creator_in_channels}</code> \n"
    response += f"    <i>○ Admin Rights:</i> <code>{admin_in_broadcast_channels - creator_in_channels}</code> \n"
    response += f"<b>◈ Unread:</b> <code>{unread}</code> \n"
    response += f"<b>◈ Unread Mentions:</b> <code>{unread_mentions}</code> \n\n"
    response += f"<b><i>⊶ Time Taken: {stop_time:.02f}s ⊷</b></i> \n"
    await hell.edit(response, parse_mode="HTML", link_preview=False)


CmdHelp("stats").add_command(
    "stats", None, "Shows you the count of your groups, channels, private chats, etc."
).add_info(
    "Statistics Of Account"
).add_warning(
    "✅ Harmless Module."
).add()
