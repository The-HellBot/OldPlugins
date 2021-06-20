import os
import urllib

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from . import *

# ====================== CONSTANT ===============================
INVALID_MEDIA = "⚠️ Targeted Media **Invalid !!**"
PP_CHANGED = "**📍 Profile picture changed successfully.**"
PP_TOO_SMOL = "🖼️ Image size is small. Use a bigger picture."
PP_ERROR = "🥴 Failure occured while processing image."
BIO_SUCCESS = "🌟 Bio Message Edited Successfully."
NAME_OK = "~~Kimi No Nawa~~ **Your Name Changed to**  {}.."
USERNAME_SUCCESS = "🌝 Successfully Changed Your Username."
USERNAME_TAKEN = "😬 This Username is already taken. Try another one."
OFFLINE_TAG = "[ • OFFLINE • ]"
ONLINE_TAG = "[ • ONLINE • ]"
PROFILE_IMAGE = "https://telegra.ph/file/9f0638dbfa028162a8682.jpg"
# ===============================================================

@bot.on(hell_cmd(pattern="offline$", outgoing=True)) 
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await eod(event, "**Already in Offline Mode.**")
        return
    await eor(event, "**Changing Profile to Offline...**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    urllib.request.urlretrieve(
        "https://telegra.ph/file/249f27d5b52a87babcb3f.jpg", "donottouch.jpg"
    )
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:
            await eod(event, str(e))
        else:
            await eod(event, "**Changed profile to OffLine.**")
    try:
        os.system("rm -fr donottouch.jpg")
    except Exception as e:
        logger.warn(str(e))
    last_name = ""
    first_name = OFFLINE_TAG
    try:
        await bot(
            functions.account.UpdateProfileRequest(
                last_name=last_name, first_name=first_name
            )
        )
        result = "**`{} {}`\nI am Offline now.**".format(first_name, last_name)
        await eod(event, result)
    except Exception as e:
        await eod(event, str(e))


@bot.on(hell_cmd(pattern="online$", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await eor(event, "**Changing Profile to Online...**")
    else:
        await eod(event, "**Already Online.**")
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    urllib.request.urlretrieve(PROFILE_IMAGE, "donottouch.jpg")
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:
            await eod(event, str(e))
        else:
            await eod(event, "**Changed profile to Online.**")
    try:
        os.system("rm -fr donottouch.jpg")
    except Exception as e:
        logger.warn(str(e))
    first_name = ONLINE_TAG
    last_name = ""
    try:
        await bot(
            functions.account.UpdateProfileRequest(
                last_name=last_name, first_name=first_name
            )
        )
        result = "**`{} {}`\nI am Online !**".format(first_name, last_name)
        await eod(event, result)
    except Exception as e:
        await eod(event, str(e))

@bot.on(hell_cmd(pattern="pbio (.*)"))
async def _(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await bot(
            functions.account.UpdateProfileRequest(about=bio)
        )
        await eod(event, BIO_SUCCESS)
    except Exception as e:
        await event.edit(str(e))


@bot.on(hell_cmd(pattern="pname (.*)"))
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "-" in names:
        first_name, last_name = names.split("-", 1)
    try:
        await bot(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await eod(event, NAME_OK.format(names))
    except Exception as e:
        await event.edit(str(e))


@bot.on(hell_cmd(pattern="ppic"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("Downloading Profile Picture to my local ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await bot.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("now, Uploading to @Telegram ...")
            file = await bot.upload_file(photo)
            try:
                await bot(
                    functions.photos.UploadProfilePhotoRequest(
                        file
                    )
                )
            except Exception as e:
                await event.edit(str(e))
            else:
                await eod(event, PP_CHANGED)
    try:
        os.remove(photo)
    except Exception as e:
        logger.warn(str(e))


@bot.on(hell_cmd(outgoing=True, pattern="username (.*)"))
async def update_username(username):
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await eod(username, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await eod(username, USERNAME_TAKEN)


@bot.on(hell_cmd(outgoing=True, pattern="count$"))
async def count(event):
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`Processing..`")
    dialogs = await bot.get_dialogs(limit=None, ignore_migrated=True)
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

    result += f"**🙋🏻‍♂️ Users :**  `{u}`\n\n"
    result += f"**🏙️ Groups :**  `{g}`\n\n"
    result += f"**🌇 Super Groups :**  `{c}`\n\n"
    result += f"**📺 Channels :**  `{bc}`\n\n"
    result += f"**👾 Bots :**  `{b}`"

    await event.edit(result)


@bot.on(hell_cmd(outgoing=True, pattern=r"delpfp"))
async def remove_profilepic(delpfp):
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
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
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await eod(delpfp, f"🗑️ **Successfully deleted**  `{len(input_photos)}`  **profile picture(s).**")


@bot.on(hell_cmd(pattern="myusernames$"))
async def _(event):
    if event.fwd_from:
        return
    result = await bot(GetAdminedPublicChannelsRequest())
    output_str = ""
    for channel_obj in result.chats:
        output_str += f"- {channel_obj.title} @{channel_obj.username} \n"
    await event.edit(output_str)


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
  "kickme", None, "Gets out of the grp..."
).add_info(
  "🌝 Managing Profile was never so easy."
).add_warning(
  "✅ Harmless Module."
).add()
