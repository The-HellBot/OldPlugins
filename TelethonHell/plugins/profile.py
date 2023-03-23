import os
import time
import urllib

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.custom import Dialog
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          GetUserPhotosRequest)
from telethon.tl.types import Channel, Chat, InputPhoto, User
from TelethonHell.plugins import *


@hell_cmd(pattern="offline$")
async def _(event):
    ForGo10God, HELL_USER, _ = await client_id(event)
    user = await event.client.get_entity(ForGo10God)
    if HELL_USER.startswith("[ • OFFLINE • ]"):
        return await eod(event, "**Already in Offline Mode.**")
    hell = await eor(event, "**Changing Profile to Offline...**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    urllib.request.urlretrieve(
        "https://te.legra.ph/file/249f27d5b52a87babcb3f.jpg", "donottouch.jpg"
    )
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:
            return await parse_error(hell, e)
        else:
            await eor(hell, "**Changed profile to OffLine.**")
    try:
        os.remove("donottouch.jpg")
    except Exception as e:
        LOGS.warn(str(e))
    last_name = ""
    first_name = "[ • OFFLINE • ]"
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                last_name=last_name, first_name=first_name
            )
        )
        result = "**`{} {}`\nI am Offline now.**".format(first_name, last_name)
        await eor(hell, result)
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="online$")
async def _(event):
    ForGo10God, HELL_USER, _ = await client_id(event)
    user = await event.client.get_entity(ForGo10God)
    if HELL_USER.startswith("[ • OFFLINE • ]"):
        hell = await eor(event, "**Changing Profile to Online...**")
    else:
        return await eod(event, "**Already Online.**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    urllib.request.urlretrieve("https://telegra.ph/file/9f0638dbfa028162a8682.jpg", "donottouch.jpg")
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:
            return await parse_error(hell, e)
        else:
            await eor(hell, "**Changed profile to Online.**")
    try:
        os.remove("donottouch.jpg")
    except Exception as e:
        LOGS.warn(str(e))
    first_name = "[ • ONLINE • ]"
    last_name = ""
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                last_name=last_name, first_name=first_name
            )
        )
        result = "**`{} {}`\nI am Online !**".format(first_name, last_name)
        await eor(hell, result)
    except Exception as e:
        await parse_error(hell, e)


@hell_cmd(pattern="pbio(?:\s|$)([\s\S]*)")
async def _(event):
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Nothing given to update bio in profile.")
    bio = lists[1].strip()
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await eor(event, "🌟 Bio Message Edited Successfully.")
    except Exception as e:
        await parse_error(event, e)


@hell_cmd(pattern="pname(?:\s|$)([\s\S]*)")
async def _(event):
    lists = event.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(event, "Nothing given to update name in profile.")
    names = lists[1].strip().split("|", 1)
    first_name = ""
    last_name = ""
    if len(names) == 2:
        first_name = names[0].strip()
        last_name = names[1].strip()
    else:
        first_name = names[0].strip()
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await eor(event, f"**✅ Profile name changed!** \n\n__First Name:__ {first_name} \n__Last Name:__ {last_name}")
    except Exception as e:
        await parse_error(event, e)


@hell_cmd(pattern="ppic$")
async def _(event):
    reply = await event.get_reply_message()
    hell = await eor(event, "Changing profile picture ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(reply, Config.TMP_DOWNLOAD_DIRECTORY)
    except Exception as e:
        await parse_error(hell, e)
    else:
        if photo:
            file = await event.client.upload_file(photo)
            try:
                await event.client(functions.photos.UploadProfilePhotoRequest(file))
            except Exception as e:
                await parse_error(hell, e)
            else:
                await eod(hell, "**📍 Profile picture changed successfully.**")
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.warn(str(e))


@hell_cmd(pattern="username(?:\s|$)([\s\S]*)")
async def update_username(event):
    lists = event.text.split(" ", 2)
    if len(lists) < 2:
        return await parse_error(event, "Nothing given to change username.")
    newusername = lists[1].strip()
    try:
        await event.client(UpdateUsernameRequest(newusername))
        await eod(event, "🌝 Successfully Changed Your Username.")
    except UsernameOccupiedError:
        await eod(event, "😬 This Username is already taken. Try another one.")
    except Exception as e:
        await parse_error(event, e)


@hell_cmd(pattern="count$")
async def count(event):
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    hell = await eor(event, "`Processing..`")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)
    result = "<b><i><u>My Stats Count</b></i></u>\n\n"
    result += f"<b><i>🙋🏻‍♂️ Users :</b></i> <code>{u}</code>\n"
    result += f"<b><i>🏙️ Groups :</b></i>  <code>{g}</code>\n"
    result += f"<b><i>🌇 Super Groups :</b></i>  <code>{c}</code>\n"
    result += f"<b><i>📺 Channels :</b></i>  <code>{bc}</code>\n"
    result += f"<b><i>👾 Bots :</b></i>  <code>{b}</code>"

    await hell.edit(result, parse_mode="HTML")


@hell_cmd(pattern="delpfp(?:\s|$)([\s\S]*)")
async def remove_profilepic(event):
    group = event.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    ForGo10God, _, _ = await client_id(event)
    pfplist = await event.client(
        GetUserPhotosRequest(user_id=ForGo10God, offset=0, max_id=0, limit=lim)
    )
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(
                id=sep.id,
                access_hash=sep.access_hash,
                file_reference=sep.file_reference,
            )
        )
    await event.client(DeletePhotosRequest(id=input_photos))
    await eod(
        event,
        f"🗑️ **Deleted Profile Picture(s)!** \n\n__Total:__ `{len(input_photos)}`",
    )


@hell_cmd(pattern="myusernames$")
async def _(event):
    _, _, hell_mention = await client_id(event)
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = f"**Usernames reserved by:** {hell_mention}\n\n"
    for channel_obj in result.chats:
        output_str += f"• {channel_obj.title} ~ @{channel_obj.username} \n"
    await eor(event, output_str)


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
    ForGo10God, HELL_USER, hell_mention = await client_id(event, is_html=True)
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


CmdHelp("profile").add_command(
    "count", None, "Counts your groups, chats, bots etc..."
).add_command(
    "myusernames", None, "Shows usernames reserved by you. That is public groups or channels created by you"
).add_command(
    "delpfp", "<count> or all", "Deletes your Telegram profile picture(s)."
).add_command(
    "pbio", "<text>", "Changes your Telegram bio", ".pbio Hello there, This iz my bio"
).add_command(
    "ppic", "<reply to image>", "Changes your Telegram profie picture with the one you replied to"
).add_command(
    "pname", "<firstname> or <firstname | lastname>", "Changes Your Telegram account name"
).add_command(
    "username", "<new username>", "Changes your Telegram Account Username"
).add_command(
    "online", None, "Remove Offline Tag from your name and change profile pic to vars PROFILE_IMAGE."
).add_command(
    "offline", None, "Add an offline tag in your name and change profile pic to black."
).add_command(
    "stats", None, "Shows you the count of your groups, channels, private chats, etc."
).add_info(
    "🌝 Managing Profile was never so easy."
).add_warning(
    "✅ Harmless Module."
).add()
