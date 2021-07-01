import html
import logging

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from . import *


@bot.on(hell_cmd(pattern="getpic ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="getpic ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await eor(event, "Getting profile photo..")
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await edit_or_reply(event, str(error_i_a))
        return False
    replied_user_profile_photos = await bot(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Need a Profile Picture to check **this**"
        str(e)
    caption = """Profile Pics (◠‿◕)
Person: <a href='tg://user?id={}'>{}</a>
""".format(
        user_id,
        user_id,
        first_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats,
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await bot.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await event.delete()


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
        if event.message.entities is not None:
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

name = "Profile Photos"

@bot.on(hell_cmd(pattern="poto ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="poto ?(.*)", allow_sudo=True))
async def potocmd(event):
    uid = "".join(event.raw_text.split(maxsplit=1)[1:])
    user = await event.get_reply_message()
    chat = event.input_chat
    if user:
        photos = await event.client.get_profile_photos(user.sender)
        u = True
    else:
        photos = await event.client.get_profile_photos(chat)
        u = False
    if uid.strip() == "":
        uid = 1
        if int(uid) <= (len(photos)):
            send_photos = await event.client.download_media(photos[uid - 1])
            await event.client.send_file(event.chat_id, send_photos)
        else:
            await eod(
                event, "No photo found of this NIBBA. Now u Die!"
            )
            await asyncio.sleep(2)
            return
    elif uid.strip() == "all":
        if len(photos) > 0:
            await event.client.send_file(event.chat_id, photos)
        else:
            try:
                if u is True:
                    photo = await event.client.download_profile_photo(user.sender)
                else:
                    photo = await event.client.download_profile_photo(event.input_chat)
                await event.client.send_file(event.chat_id, photo)
            except a:
                await eod(event, "**This user has no photos!**")
                return
    else:
        try:
            uid = int(uid)
            if uid <= 0:
                await eod(
                    event, "```number Invalid!``` **Are you komedy Me ?**"
                )
                return
        except BaseException:
            await eod(event, "Are you komedy me ?")
            return
        if int(uid) <= (len(photos)):
            send_photos = await event.client.download_media(photos[uid - 1])
            await event.client.send_file(event.chat_id, send_photos)
        else:
            await eod(
                event, "No photo found of this NIBBA. Now u Die!"
            )
            await asyncio.sleep(2)
            return


CmdHelp("getpfp").add_command(
  "poto", "<all> / <desired pp number>", "Reply to user to get his/her profile pic. Use .poto <number> to get desired profile pic else use .poto all to get all profile pic(s). If you dont reply to a user then it gets group pics."
).add_command(
  "getpic", "<reply> <username>", "Gets the user's 1st profile pic. But this time with a caption. Try it yourself..."
).add_info(
  "Steal Profile Pictures."
).add_warning(
  "✅ Harmless Module."
).add()
