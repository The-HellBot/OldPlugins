from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    MessageActionChannelMigrateFrom,
    MessageEntityMentionName,
)
from telethon.utils import pack_bot_file_id, get_input_location
from datetime import datetime
from math import sqrt
from os import remove
import emoji
from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
    ChatAdminRequiredError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.tl.functions.channels import (
    GetFullChannelRequest,
    GetParticipantsRequest,
    LeaveChannelRequest,
)
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
import html
from . import *
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(hell_cmd(pattern="recognize ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="recognize ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await eod(event, "Reply to any user's media message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await eod(event, "reply to media file")
        return
    chat = "@Rekognition_Bot"
    reply_message.sender
    if reply_message.sender.bot:
        await eod(event, "Reply to actual users message.")
        return
    hell = await eor(event, "recognizeing this media")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            first = await event.client.forward_messages(chat, reply_message)
            second = await response
        except YouBlockedUserError:
            await event.reply("unblock @Rekognition_Bot and try again")
            await hell.delete()
            return
        if second.text.startswith("See next message."):
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            third = await response
            hell = third.message.message
            await eor(event, hell)
            await bot.delete_messages(
            	conv.chat_id, [first.id, second.id, third.id]
            )

        else:
            await eod(event, "sorry, I couldnt find it")


@bot.on(hell_cmd(pattern="info ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="info ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
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
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("Last Name not found")
    )
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "`Need a Profile Picture to check **this**`"
        str(e)
    caption = """<b>Extracted User info From Telegram<b>
    
<b>🆔️ User ID</b>: <code>{}</code>
<b>📎 Link To Profile</b>: <a href='tg://user?id={}'>Click Here🚪</a>
<b>🗣️ First Name</b>: <code>{}</code>
<b>🗣️ Second Name</b>: <code>{}</code>
<b>👨🏿‍💻 BIO</b>: {}
<b>🌐 DC ID</b>: {}
<b>📸 NO OF PSS</b> : {}
<b>🧐 RESTRICTED</b>: {}
<b>✅ VERIFIED</b>: {}
<b>🤖 BOT</b>: {}
<b>👥 Groups in Common</b>: {}

<b>⚡ <a href='https://t.me/its_hellbot'>From DataBase of HellBot</a> ⚡ </b>
""".format(
        user_id,
        user_id,
        first_name,
        last_name,
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
        link_preview=False,
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


@bot.on(hell_cmd(pattern="chatinfo(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="chatinfo(?: |$)(.*)", allow_sudo=True))
async def info(event):
    if event.fwd_from:
        return
    hell = await eor(event, "`Analysing the chat...`")
    chat = await get_chatinfo(event)
    caption = await fetch_info(chat, event)
    try:
        await hell.edit(caption, parse_mode="html")
    except Exception as e:
        print("Exception:", e)
        await eod(hell, "`An unexpected error has occurred.`")
    return


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await edit_or_reply(event, "`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await edit_or_reply(event, 
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await edit_or_reply(event, "`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError) as err:
            await edit_or_reply(event, str(err))
            return None
    return chat_info


async def fetch_info(chat, event):
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = "⚠️"
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )
    # Same for msg_info.users
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and type(msg_info.messages[0].action) is MessageActionChannelMigrateFrom
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "Unknown"
        str(e)

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "No"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "No"
    )
    verified = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "No"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None, works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "🔰 <b>CHAT INFO</b> 🔰\n"
    caption += f"🆔 ID : <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"🚀 {chat_type} Name : {chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"✳️ Former name : {former_title}\n"
    if username is not None:
        caption += f"🔸 {chat_type} type : Public\n"
        caption += f"Link : {username}\n"
    else:
        caption += f"🔸 {chat_type} type : Private\n"
    if creator_username is not None:
        caption += f"👑 Creator : {creator_username}\n"
    elif creator_valid:
        caption += (
            f'👑 Creator : <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
        )
    if created is not None:
        caption += f"🆕 Created : <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"🆕 Created : <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"🌐 DataCentre ID : {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"🔅 {chat_type} level : <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"🗨️ Viewable messages : <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"💬 Messages sent : <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"💬 Messages sent : <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"👪 Members : <code>{members}</code>\n"
    if admins is not None:
        caption += f"⚜️ Administrators : <code>{admins}</code>\n"
    if bots_list:
        caption += f"🤖 Bots : <code>{bots}</code>\n"
    if members_online:
        caption += f"👨‍💻 Currently online : <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"🚫 Restricted users : <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"❌ Banned users : <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'😋 {chat_type} stickers : <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"🐢 Slow mode : {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
    if not broadcast:
        caption += f"🏬 Supergroup : {supergroup}\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"⚠️ Restricted : {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platform: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Reason: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Text: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "📍 Scam : <b>Yes</b>\n\n"
    if hasattr(chat_obj_info, "verified"): 
        caption += f"💟 Verified by Telegram : {verified}\n\n"
    if description:
        caption += f"📝 Description : \n<code>{description}</code>\n"
    return caption


@bot.on(hell_cmd(pattern=r"users ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"users ?(.*)", allow_sudo=True))
async def get_users(show):
    if show.fwd_from:
        return
    if not show.is_group:
        await eod(show, "Are you sure this is a group?")
        return
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await edit_or_reply(show, mentions)
    except MessageTooLongError:
        await edit_or_reply(show, "Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="Users in {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


@bot.on(hell_cmd(pattern="admins ?(.*)"))
@bot.on(sudo_cmd(pattern="admins ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**⚜️ Admins in this Group ⚜️**: \n"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions_heading = "Admins in {} Group: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await edit_or_reply(event, str(e))
            return None
    else:
        chat = to_write_chat
        if not event.is_group:
            await eod(event, "I dont think this is a group🚶")
            return
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted and isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n 🔰 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            else:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n 🔸 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if reply_message:
        await reply_message.reply(mentions)
    else:
        await event.client.send_message(event.chat_id, mentions)
    await event.delete()


@bot.on(hell_cmd(pattern="bots ?(.*)"))
@bot.on(sudo_cmd(pattern="bots ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "🤖 **Bots in this Group**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "Bots in {} group: \n".format(input_str)
        try:
            chat = await borg.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in borg.iter_participants(chat, filter=ChannelParticipantsBots):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.edit(mentions)
    
    
@bot.on(hell_cmd(pattern="id$"))
@bot.on(sudo_cmd(pattern="id$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    hell = await eor(event, "Fetching Ids...")
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await hell.edit(
                "🔸 **Current Chat ID:** `{}`\n\n🔰 **From User ID:** `{}`\n\n🤖 **Bot API File ID:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id), bot_api_file_id
                )
            )
        else:
            await hell.edit(
                "🔸 **Current Chat ID:** `{}`\n\n🔰 **From User ID:** `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                )
            )
    else:
        await hell.edit("🔸 **Current Chat ID:** `{}`".format(str(event.chat_id)))


CmdHelp("infos").add_command(
  "admins", None, "Gets the list of admins in current chat along with the crator"
).add_command(
  "id", "<reply>", "Gets the user id of the replied user."
).add_command(
  "bots", None, "Gets the list of all the bots in the chat."
).add_command(
  "info", "<reply / username>", "Fetches the information of the user"
).add_command(
  "whois", "<reply / username>", "Same as info"
).add_command(
  "chatinfo", "<username of group>", "Shows you the total information of the required chat"
).add_command(
  "users", "<name of member> (optional)", "Retrives all the (or mentioned) users in the chat"
).add_command(
  "recognize", "<reply to photo>", "Sends you the details of that replied picture."
).add_info(
  "Basic Cmds for groups."
).add_warning(
  "✅ Harmless Module."
).add()
