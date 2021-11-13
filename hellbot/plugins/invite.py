from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from . import *

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
            await event.reply("`Invalid channel/group`")
            return None
        except ChannelPrivateError:
            await event.reply(
                "`This is a private channel/group or I am banned from there`"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Channel or supergroup doesn't exist`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Invalid channel/group`")
            return None
    return chat_info


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


@hell_cmd(pattern="inviteall(?:\s|$)([\s\S]*)")
async def get_users(event):
    hel_ = event.text[11:]
    hell_chat = hel_.lower()
    restricted = ["@hellbot_chat", "@its_hellbot"]
    hell = await eor(event, f"__Inviting members from__ {hel_}")
    if hell_chat in restricted:
        await hell.edit("You can't Invite Members from there.")
        await event.client.send_message(-1001496036895, "Sorry for inviting members from here.")
        return
    kraken = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await hell.edit("`Sorry, Cant add users here`")
    s = 0
    f = 0
    error = "None"
    await hell.edit("**INVITING USERS !!**")
    async for user in event.client.iter_participants(kraken.full_chat.id):
        try:
            await event.client(
                InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s += 1
            await hell.edit(
                f"**INVITING USERS.. **\n\n**Invited :**  `{s}` users \n**Failed to Invite :**  `{f}` users.\n\n**×Error :**  `{error}`"
            )
        except Exception as e:
            error = str(e)
            f += 1
    return await hell.edit(
        f"**INVITING FINISHED** \n\n**Invited :**  `{s}` users \n**Failed :**  `{f}` users."
    )


@hell_cmd(pattern="add(?:\s|$)([\s\S]*)")
async def _(event):
    if (
        "addsudo" in event.raw_text.lower()
        or "addblacklist" in event.raw_text.lower()
    ):
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await eod(event, f"Use `{hl}add` users to a chat, not to a Private Message")
    else:
        logger.info(to_add_users)
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await eor(event, "Invited User...")
        else:
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await eod(event, "Added user to the chat..")


CmdHelp("invite").add_command(
  "add", "<username/id>", "Adds the given user to the group"
).add_command(
  "inviteall", "<group username>", "Scraps user from the targeted group to your group. Basically Kidnapps user from one chat to another"
).add_info(
  "Invite them."
).add_warning(
  "✅ Harmless Module."
).add()
