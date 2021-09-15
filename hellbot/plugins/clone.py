import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from . import *


@hell_cmd(pattern="clone ?(.*)")
async def _(event):
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    cid = await client_id(event)
    if replied_user is None:
        await eod(event, str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TMP_DOWNLOAD_DIRECTORY)
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌"
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await event.client.upload_file(profile_pic)
    await event.client(
        functions.photos.UploadProfilePhotoRequest(pfile)
    )
    await event.delete()
    await event.client.send_message(
        event.chat_id, "😋 **Hello friend!!**", reply_to=reply_message
    )
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#CLONE \n\n**Successfully Cloned**  [{first_name}](tg://user?id={user_id })",
    )


@hell_cmd(pattern="revert$")
async def _(event):
    name = Config.YOUR_NAME or "『 Ӈєℓℓ 』"
    bio = f"{Config.BIO_MSG}"
    n = 1
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=n)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=f"{bio}"))
    await event.client(functions.account.UpdateProfileRequest(first_name=f"{name}"))
    await eor(event, "Successfully reverted back..")
    await event.client.send_message(Config.LOGGER_ID, f"#REVERT \n\n**Revert Successful**")


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


CmdHelp("clone").add_command(
  "clone", "username/reply to user", "Steals others profile including dp, name, bio."
).add_command(
  "revert", None, "To get back to your profile but it will show ALIVE_NAME instead of your current name and DEFAULT_BIO instead of your current bio"
).add_info(
  "Cloner."
).add_warning(
  "✅ Harmless Module."
).add()
