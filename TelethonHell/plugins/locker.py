from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
from TelethonHell.plugins import *


def lock(event):
    if event == "all":
        rights = ChatBannedRights(
            until_date=None,
            send_messages=True,
            invite_users=True,
            pin_messages=True,
            change_info=True,
        )
    elif event == "msg":
        rights = ChatBannedRights(
            until_date=None,
            send_messages=True,
        )
    elif event == "media":
        rights = ChatBannedRights(
            until_date=None,
            send_media=True,
        )
    elif event == "sticker":
        rights = ChatBannedRights(
            until_date=None,
            send_stickers=True,
        )
    elif event == "gif":
        rights = ChatBannedRights(
            until_date=None,
            send_gifs=True,
        )
    elif event == "game":
        rights = ChatBannedRights(
            until_date=None,
            send_games=True,
        )
    elif event == "inline":
        rights = ChatBannedRights(
            until_date=None,
            send_inline=True,
        )
    elif event == "poll":
        rights = ChatBannedRights(
            until_date=None,
            send_polls=True,
        )
    elif event == "invite":
        rights = ChatBannedRights(
            until_date=None,
            invite_users=True,
        )
    elif event == "pin":
        rights = ChatBannedRights(
            until_date=None,
            pin_messages=True,
        )
    elif event == "info":
        rights = ChatBannedRights(
            until_date=None,
            change_info=True,
        )
    return rights


def unlock(event):
    if event == "all":
        rights = ChatBannedRights(
            until_date=None,
            send_messages=False,
            invite_users=False,
            pin_messages=False,
            change_info=False,
        )
    elif event == "msg":
        rights = ChatBannedRights(
            until_date=None,
            send_messages=False,
        )
    elif event == "media":
        rights = ChatBannedRights(
            until_date=None,
            send_media=False,
        )
    elif event == "sticker":
        rights = ChatBannedRights(
            until_date=None,
            send_stickers=False,
        )
    elif event == "gif":
        rights = ChatBannedRights(
            until_date=None,
            send_gifs=False,
        )
    elif event == "game":
        rights = ChatBannedRights(
            until_date=None,
            send_games=False,
        )
    elif event == "inline":
        rights = ChatBannedRights(
            until_date=None,
            send_inline=False,
        )
    elif event == "poll":
        rights = ChatBannedRights(
            until_date=None,
            send_polls=False,
        )
    elif event == "invite":
        rights = ChatBannedRights(
            until_date=None,
            invite_users=False,
        )
    elif event == "pin":
        rights = ChatBannedRights(
            until_date=None,
            pin_messages=False,
        )
    elif event == "info":
        rights = ChatBannedRights(
            until_date=None,
            change_info=False,
        )
    return rights


@hell_cmd(pattern="lock(?:\s|$)([\s\S]*)")
async def _(event):
    text = event.text[6:]
    cid = await client_id(event)
    hell_mention = cid[2]
    hell = await eor(event, f"Trying to lock `{text}`")
    if text == "":
        return await parse_error(hell, "Nothing given to lock in chat.")
    locker = lock(text)
    if not locker:
        return await eod(
            hell,
            f"**🤐 Invalid lock type:** {text} \nDo `{hl}ltype` to get all lock types.",
        )
    await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, locker))
    await event.client.send_file(
        event.chat_id,
        restlo,
        caption=f"{hell_mention} Locked `{text}` \n__Cause its Rest Time !!__",
    )
    await hell.delete()


@hell_cmd(pattern="unlock(?:\s|$)([\s\S]*)")
async def _(event):
    text = event.text[8:]
    cid = await client_id(event)
    hell_mention = cid[2]
    hell = await eor(event, f"Trying to unlock `{text}`")
    if text == "":
        return await parse_error(hell, "Nothing given to unlock in chat.")
    unlocker = unlock(text)
    if not unlocker:
        return await eod(
            hell,
            f"**🤐 Invalid unlock type:** {text} \nDo `{hl}ltype` to get all unlock types.",
        )
    await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, unlocker))
    await event.client.send_file(
        event.chat_id, shuru, caption=f"**{hell_mention} unlocked** `{text}`"
    )
    await hell.delete()


@hell_cmd(pattern="ltype$")
async def _(event):
    await eor(
        event,
        "**Following are the lock types :** \n\n• all\n• msg\n• media\n• sticker\n• gif\n• game\n• inline\n• poll\n• invite\n• pin\n• info\n",
    )


CmdHelp("locker").add_command(
    "lock", "<lock type>", "Locks the mentioned lock type in current chat. You can Get all lock type by using '.ltype'."
).add_command(
    "unlock", "<lock type>", "Unlocks the mentioned lock type in current chat. You can Get all lock types by using '.ltype'."
).add_command(
    "ltype", None, "Use this to get the list of lock types..."
).add_info(
    "Chat Locker."
).add_warning(
    "✅ Harmless Module."
).add()
