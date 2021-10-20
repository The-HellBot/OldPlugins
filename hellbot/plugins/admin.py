from asyncio import sleep

from telethon import functions
from telethon.errors import BadRequestError, ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights, ChannelParticipantsAdmins, MessageEntityMentionName, MessageMediaPhoto

from . import *
from hellbot.sql.mute_sql import is_muted, mute, unmute


lg_id = Config.LOGGER_ID
PP_TOO_SMOL = "🥴 The image is too small. Just like your crush's feelings"
PP_ERROR = "😕 Failure while processing the image. Just like your proposal to your crush."
NO_ADMIN = "😪 I am not an admin here! Chutiya sala"
NO_PERM = "😐 Lack of Permissions. Just like your crush's feelings for you."
CHAT_PP_CHANGED = "😉 Chat Picture Changed Successfully"
INVALID_MEDIA = "🥴 Invalid media Extension. This is insane bruh. Grow some brain."


BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@hell_cmd(pattern="setgpic$")
@errors_handler
async def set_group_photo(event):
    if not event.is_group:
        await eor(event, "`I don't think this is a group.`")
        return
    replymsg = await event.get_reply_message()
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await event.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await event.client.download_file(replymsg.media.document)
        else:
            await eor(event, INVALID_MEDIA)
    kraken = None
    if photo:
        try:
            await event.client(
                EditPhotoRequest(event.chat_id, await event.client.upload_file(photo))
            )
            await eor(event, CHAT_PP_CHANGED)
            kraken = True
        except PhotoCropSizeSmallError:
            await eor(event, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await eor(event, PP_ERROR)
        except Exception as e:
            await eor(event, f"**Error : **`{str(e)}`")
        if kraken:
            await event.client.send_message(
                lg_id,
                "#GROUPPIC\n"
                f"\nGroup profile pic changed "
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@hell_cmd(pattern="promote(?: |$)(.*)")
@errors_handler
async def promote(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    hellevent = await eor(event, "`Promoting User...`")
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "ǟɖʍɨռ"
    if not user:
        return
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await hellevent.edit(f"**🔥 Promoted  [{user.first_name}](tg://user?id={user.id})  Successfully In**  `{event.chat.title}`!! \n**Admin Tag :**  `{rank}`")
    except BadRequestError:
        await hellevent.edit(NO_PERM)
        return
    await event.client.send_message(
        lg_id,
        "#PROMOTE\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {event.chat.title}(`{event.chat_id}`)",
    )


@hell_cmd(pattern="demote(?: |$)(.*)")
@errors_handler
async def demote(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    hellevent = await eor(event, "`Demoting User...`")
    rank = "ǟɖʍɨռ"
    user = await get_user_from_event(event)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
        manage_call=None,
    )
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await hellevent.edit(NO_PERM)
        return
    await hellevent.edit(f"**😪 Demoted  [{user.first_name}](tg://user?id={user.id})  Successfully In**  `{event.chat.title}`")
    await event.client.send_message(
        lg_id,
        "#DEMOTE\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {event.chat.title}(`{event.chat_id}`)",
    )


@hell_handler()
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@hell_cmd(pattern=r"mute ?(.*)")
async def muth(event):
    x = await client_id(event)
    ForGo10God = x[0]
    if event.is_private:
        await eor(event, "**Enough of your bullshit  !!**")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "Nigga is already muted here 🥴"
            )
        if event.chat_id == ForGo10God:
            return await eod(event, "Nashe me hai kya lawde 🥴")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await eor(event, f"**Error **\n`{str(e)}`")
        else:
            await eor(event, "**Chup Reh Lawde 🥴\n`**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
    elif event.is_group:
        eventevent = await eor(event, "`Muting...`")
        input_str = event.pattern_match.group(1)
        chat = await event.get_chat()
        admin_ = []
        async for admins in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            x = admins.id
            admin_.append(x)
        if event.reply_to_msg_id:
            userid = (await event.get_reply_message()).sender_id
            name = (await event.client.get_entity(userid)).first_name
        elif input_str:
            if input_str.isdigit():
                try:
                    userid = input_str
                    name = (await event.client.get_entity(userid)).first_name
                except ValueError as ve:
                    return await eventevent.edit(str(ve))
            else:
                userid = (await event.client.get_entity(input_str)).id
                name = (await event.client.get_entity(userid)).first_name
        else:
            return await eod(eventevent, "I Need a user to mute!!")
        if userid == ForGo10God:
            return await eod(eventevent, "Nashe me hai kya lawde")
        if str(userid) in DEVLIST:
            return await eod(eventevent, "**Error Muting God**", 7)
        if ForGo10God not in admin_:
            return await eod(eventevent, NO_PERM)
        if userid in admin_:
            if is_muted(userid, event.chat_id):
                return await eventevent.edit("Admin already muted ♪～(´ε｀ )")
            try:
                mute(userid, event.chat_id)
            except Exception as e:
                await eventevent.edit(f"**Error :** \n\n`{e}`")
            else:
                return await eventevent.edit(f"**🌝 Muted admin** [{name}](tg://user?id={userid}) **in** `{chat.title}` (~‾▿‾)~")
        try:
            await event.client.edit_permissions(
                chat.id,
                userid,
                until_date=None,
                send_messages=False,
            )
            await eor(
                eventevent,
                f"**Successfully Muted**  [{name}](tg://user?id={userid}) **in**  `{chat.title}`",
            )
        except BaseException as be:
            await eor(eventevent, f"`{str(be)}`")
        await event.client.send_message(
            lg_id,
            "#MUTE\n"
            f"\nUSER:  [{name}](tg://user?id={userid})\n"
            f"CHAT:  {chat.title}",
        )


@hell_cmd(pattern="unmute ?(.*)")
async def nomuth(event):
    x = await client_id(event)
    ForGo10God = x[0]
    if event.is_private:
        await eor(event, "Talk bich..")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await eor(event,
                "Not even muted !!"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await eor(event, f"**Error **\n`{str(e)}`")
        else:
            await eor(event,
                "Abb boll bsdk."
            )
    elif event.is_group:
        hellevent = await eor(event, "`Unmuting...`")
        input_str = event.pattern_match.group(1)
        chat = await event.get_chat()
        admin_ = []
        async for admins in event.client.iter_participants(chat, filter=ChannelParticipantsAdmins):
            x = admins.id
            admin_.append(x)
        if event.reply_to_msg_id:
            userid = (await event.get_reply_message()).sender_id
            name = (await event.client.get_entity(userid)).first_name
        elif input_str:
            if input_str.isdigit():
                try:
                    userid = input_str
                    name = (await event.client.get_entity(userid)).first_name
                except ValueError as ve:
                    return await hellevent.edit(str(ve))
            else:
                userid = (await event.client.get_entity(input_str)).id
                name = (await event.client.get_entity(userid)).first_name
        else:
            return await eod(hellevent, "I need a user to unmute!!")
        if ForGo10God not in admin_:
            return await eod(hellevent, NO_PERM)
        if userid in admin_:
            if not is_muted(userid, event.chat_id):
                return await hellevent.edit("Not even muted.")
            try:
                unmute(userid, event.chat_id)
            except Exception as e:
                await hellevent.edit(f"**Error :** \n\n`{e}`")
            else:
                return await hellevent.edit("**Successfully Unmuted** [{name}](tg://user?id={userid}) **in** `{chat.title}`")
        try:
            await event.client.edit_permissions(
                chat.id,
                userid,
                until_date=None,
                send_messages=True,
            )
            await eor(
                hellevent,
                f"**Successfully Unmuted**  [{name}](tg://user?id={userid}) **in**  `{chat.title}`",
            )
        except BaseException as be:
            await eor(hellevent, f"`{str(be)}`")
        await event.client.send_message(
            lg_id,
            "#UNMUTE\n"
            f"\nUSER:  [{name}](tg://user?id={userid})\n"
            f"CHAT:  {chat.title}",
        )


@hell_cmd(pattern="ban(?: |$)(.*)")
@errors_handler
async def ban(event):
    hellevent = await eor(event, "`Banning Nigga...`")
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    user, reason = await get_user_from_event(event)
    if not user:
        return await hellevent.edit("`Reply to a user or give username!!`")
    if str(user.id) in DEVLIST:
        return await hellevent.edit("**Say again? Ban my creator??**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await hellevent.edit(NO_PERM)
        return
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await hellevent.edit(f"**Banned  [{user.first_name}](tg://user?id={user.id})  in** `[{event.chat.title}]` !!\n\nMessage Nuking : **False**")
        return
    if reason:
        await hellevent.edit(f"**Bitch** [{user.first_name}](tg://user?id={user.id}) **is now banned in**  `[{event.chat.title}]` !!\n**Reason :** `{reason}`")
    else:
        await hellevent.edit(f"**Bitch** [{user.first_name}](tg://user?id={user.id}) **is now banned in**  `[{event.chat.title}]`!!")
    await event.client.send_message(
        lg_id,
        "#BAN\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {event.chat.title}(`{event.chat_id}`)",
    )


@hell_cmd(pattern="unban(?: |$)(.*)")
@errors_handler
async def nothanos(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    hellevent = await eor(event, "`Unbanning...`")
    user = await get_user_from_event(event)
    user = user[0]
    if not user:
        return
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await hellevent.edit(f"[{user.first_name}](tg://user?id={user.id}) **Is Now Unbanned in**  `{event.chat.title}` !!")
        await event.client.send_message(
            lg_id,
            "#UNBAN\n"
            f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )
    except UserIdInvalidError:
        await hellevent.edit("Invalid UserId!! Please Recheck it!!")


@hell_cmd(pattern="pin($| (.*))")
@errors_handler
async def pin(event):
    chat = await event.get_chat()
    ms_l = await event.client.get_entity(event.chat_id)
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    to_pin = event.reply_to_msg_id
    if not to_pin:
        await eor(event, "🥴 Reply to a message to pin it.")
        return
    options = event.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await event.client.pin_message(event.to_id, to_pin, notify=is_silent)
    except BadRequestError:
        await eor(event, NO_PERM)
        return
    if not event.is_private:
        await eod(event, f"📌 **Pinned  [this message](https://t.me/c/{ms_l.id}/{to_pin})  Successfully!**")
        user = await get_user_from_id(event.sender_id, event)
        await event.client.send_message(
            lg_id,
            "#PIN\n"
            f"\nADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )
    elif event.is_private:
        await eod(event, "**📍 Pinned successfully !!**")


@hell_cmd(pattern="unpin ?(.*)")
async def unpin(event):
    chat = await event.get_chat()
    rply = event.reply_to_msg_id
    ms_l = await event.client.get_entity(event.chat_id)
    options = event.pattern_match.group(1)
    if not rply and options != "all":
        return await eod(event, f"Reply to a msg to unpin it. Do `{hl}unpin all` to unpin all pinned msgs.")
    try:
        if rply and not options:
            await event.client.unpin_message(event.chat_id, rply)
            if event.is_private:
                await eod(event, "**Unpinned this message successfully !**")
            else:
                await eod(event, f"**Unpinned [this message](https://t.me/c/{ms_l.id}/{rply}) successfully !!**")
                await event.client.send_message(lg_id, f"#UNPIN \n\n**Chat :** {event.chat.title} (`{event.chat_id}`) \n**Message :** [Here](https://t.me/c/{ms_l.id}/{rply})")
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
            await eod(event, f"**Unpinned all pinned msgs.**")
            if not event.is_private:
                await event.client.send_message(lg_id, f"#UNPIN \n\n**Chat :** {event.chat.title} (`{event.chat_id}`) \n**Messages :** __All__")
        else:
            return await eod(event, f"Reply to a msg to unpin it. Do `{hl}unpin all` to unpin all pinned msgs.")
    except BadRequestError:
        return await eod(event, NO_PERM)
    except Exception as e:
        return await eod(event, f"**ERROR !!** \n\n`{e}`")


@hell_cmd(pattern="kick(?: |$)(.*)")
@errors_handler
async def kick(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    user, reason = await get_user_from_event(event)
    if not user:
        return await eor(event, "`Couldn't fetch user info...`")
    if str(user.id) in DEVLIST:
        return await eor(event, "**Turn back, Go straight and fuck off!!**")
    hellevent = await eor(event, "`Kicking...`")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await hellevent.edit(NO_PERM + f"\n`{str(e)}`")
        return
    if reason:
        await hellevent.edit(
            f"**🏃 Kicked**  [{user.first_name}](tg://user?id={user.id})'s **Butt from** `{event.chat.title}!`\nReason: `{reason}`"
        )
    else:
        await hellevent.edit(f"**🏃 Kicked**  [{user.first_name}](tg://user?id={user.id})'s **Butt from** `{event.chat.title}!`")
    await event.client.send_message(
        lg_id,
        "#KICK\n"
        f"\nUSER: [{user.first_name}](tg://user?id={user.id})\n"
        f"CHAT: {event.chat.title}(`{event.chat_id}`)\n",
    )


@hell_cmd(pattern=f"zombies ?(.*)")
async def rm_deletedacc(event):
    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No zombies or deleted accounts found in this group, Group is clean`"
    if con != "clean":
        event = await eor(
            event, "**Searching For Zombies...**"
        )
        async for user in event.client.iter_participants(event.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**🆘 ALERT !!**\n\n`{del_u}`  **Zombies detected ☣️\nClean them by using**  `{hl}zombies clean`"
        await event.edit(del_status)
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eod(event, NO_ADMIN)
        return
    event = await eor(
        event, "🧹 Purging out zombies from this group..."
    )
    del_u = 0
    del_a = 0
    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client.kick_participant(event.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_or_reply(event, "`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**Zombies Purged!!**\n\n**Zombies Killed :**  `{del_u}`"
    if del_a > 0:
        del_status = f"**Zombies Killed**  `{del_u}`\n\n`{del_a}`  **Zombies Holds Immunity!!**"
    await edit_or_reply(event, del_status)
    await event.client.send_message(
        lg_id,
        f"#ZOMBIES\
        \n{del_status}\
       \nCHAT: {event.chat.title}(`{event.chat_id}`)",
    )


@hell_cmd(pattern="undlt$")
async def _(event):
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await event.client.get_admin_log(
            event.chat_id, limit=5, edit=False, delete=True
        )
        deleted_msg = "Deleted message in this group:"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await eor(event, deleted_msg)
    else:
        await eor(
            event, "`You need administrative permissions in order to do this command`"
        )
        await sleep(3)
        try:
            await event.delete()
        except:
            pass


async def get_user_from_event(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Could not fetch info of that user.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if event.fwd_from:
        return
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CmdHelp("admins").add_command(
  "setgpic", "<reply to image>", "Changes the groups display picture"
).add_command(
  "promote", "<username/reply> <custom rank (optional)>", "Provides admins right to a person in the chat."
).add_command(
  "demote", "<username/reply>", "Revokes the person admin permissions in the chat."
).add_command(
  "ban", "<username/reply> <reason (optional)>", "Bans the person off your chat."
).add_command(
  "unban", "<username/reply>", "Removes the ban from the person in the chat."
).add_command(
  "mute", "<reply>/<userid or username>", "Mutes mentioned user in current PM/Group. Mutes non-admins by restricting their rights and mutes admins by deleting their new messages."
).add_command(
  "unmute", "<reply>/<userid or username>", "Unmutes the person muted in that PM/Group."
).add_command(
  "pin", "<reply> loud", "Pins the replied message in Group", "pin loud"
).add_command(
  "unpin", "<reply> or 'all'", "Unpins the replied message or unpins all pinned messages.", "unpin all/<reply>"
).add_command(
  "kick", "<username/reply>", "kick the person off your chat"
).add_command(
  "zombies", None, "Check If The Group is Infected By Zombies."
).add_command(
  "zombies clean", None, "Clears all the zombies in the group."
).add_command(
  "undlt", None, "display last 5 deleted messages in group."
).add_info(
  "Admins Things!"
).add_warning(
  "✅ Harmless Module."
).add()
