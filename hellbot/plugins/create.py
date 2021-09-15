from telethon.tl import functions
from telethon.tl.types import MessageEntityMentionName

from . import *


@hell_cmd(pattern="create (b|g|c) (.*)")
async def _(event):
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    hell = await eor(event, "Creating wait sar.....")
    if type_of_group == "b":
        try:
            result = await event.client(
                functions.messages.CreateChatRequest(
                    users=["@MissRose_Bot"],
                    title=group_name,
                )
            )
            created_chat_id = result.chats[0].id
            await event.client(
                functions.messages.DeleteChatUserRequest(
                    chat_id=created_chat_id, user_id="@MissRose_Bot"
                )
            )
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await hell.edit(
                "Group `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:
            await hell.edit(str(e))
    elif type_of_group in ["g", "c"]:
        try:
            r = await event.client(
                functions.channels.CreateChannelRequest(
                    title=group_name,
                    about="Created By Hêllẞø†",
                    megagroup=type_of_group != "c",
                )
            )

            created_chat_id = r.chats[0].id
            result = await event.client(
                functions.messages.ExportChatInviteRequest(
                    peer=created_chat_id,
                )
            )
            await hell.edit(
                "Channel `{}` created successfully. Join {}".format(
                    group_name, result.link
                )
            )
        except Exception as e:
            await event.edit(str(e))
    else:
        await hell.edit(f"Read `{hl}plinfo create` to know how to use me")


@hell_cmd(pattern="link ?(.*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await eor(mention, f"[{custom}](tg://user?id={user.id}) \n\n\n  ☝️ Tap To See ☝️")
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await eor(mention, f"[{tag}](tg://user?id={user.id}) \n\n\n ☝️ Tap to See ☝️")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
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
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


CmdHelp("create").add_command(
  'create b', 'Name of your grp', 'Creates a super and send you link'
).add_command(
  'create g', 'Name of your grp', 'Creates a private grp and send you link'
).add_command(
  'create c', 'Name of your channel', 'Creates a channel and sends you link'
).add_command(
  'link', '<reply> <text>', 'Makes a permanent link of tagged user with a custom text'
).add_info(
  'Creates Groups'
).add_warning(
  '✅ Harmless Module'
).add()
