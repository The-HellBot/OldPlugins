from telethon.tl import functions
from telethon.tl.types import MessageEntityMentionName
from TelethonHell.plugins import *


@hell_cmd(pattern="create (b|g|c) ([\s\S]*)")
async def _(event):
    type_of_group = event.pattern_match.group(1)
    group_name = event.pattern_match.group(2)
    hell = await eor(event, "Creating ...")
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
            await parse_error(hell, e)
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
            await parse_error(hell, e)
    else:
        await hell.edit(f"Read `{hl}plinfo create` to know how to use me")


@hell_cmd(pattern="link ([\s\S]*)")
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await eor(
            mention, f"[{custom}](tg://user?id={user.id}) \n\n\n  ☝️ Tap To See ☝️"
        )
    else:
        tag = (
            user.first_name.replace("\u2060", "") if user.first_name else user.username
        )
        await eor(mention, f"[{tag}](tg://user?id={user.id}) \n\n\n ☝️ Tap to See ☝️")


CmdHelp("create").add_command(
    "create b", "Name of your grp", "Creates a super and send you link"
).add_command(
    "create g", "Name of your grp", "Creates a private grp and send you link"
).add_command(
    "create c", "Name of your channel", "Creates a channel and sends you link"
).add_command(
    "link", "<reply> <text>", "Makes a permanent link of tagged user with a custom text"
).add_info(
    "Creates Groups"
).add_warning(
    "✅ Harmless Module"
).add()
