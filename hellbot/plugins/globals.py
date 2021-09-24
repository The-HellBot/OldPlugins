import asyncio
import random

from telethon import events
from telethon.tl.types import ChatAdminRights, ChannelParticipantsAdmins, ChatBannedRights, MessageEntityMentionName, MessageMediaPhoto
from telethon.errors.rpcerrorlist import UserIdInvalidError, MessageTooLongError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest

from hellbot.sql.gban_sql import is_gbanned, gbaner, ungbaner, all_gbanned
from hellbot.sql.gvar_sql import gvarstat
from hellbot.sql import gmute_sql as gsql
from . import *

clients = 0
if H1:
    clients += 1
if H2:
    clients += 1
if H3:
    clients += 1
if H4:
    clients += 1
if H5:
    clients += 1


async def get_full_user(event):  
    args = event.pattern_match.group(1).split(':', 1)
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
            await eor(event, "Need a user to do this...")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await eor(event, f"**ERROR !!**\n\n`{str(err)}`")           
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



@hell_cmd(pattern="gpro ?(.*)")
async def _(event):
    i = 0
    sender = await event.get_sender()
    me = await event.client.get_me()
    hell = await eor(event, "`Promoting globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
       k = await hell.edit("You can't promote yourself...")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await hell.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await event.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=False,
                               invite_users=True,
                                change_info=False,
                                 ban_users=True,
                                  delete_messages=True,
                                   pin_messages=True)
        for x in telchanel:
          try:
             await event.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await hell.edit(f"**Promoting User in :**  `{i}` Chats...")
          except:
             pass
    else:
        await hell.edit(f"**Reply to a user !!**")
    await hell.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Promoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(Config.LOGGER_ID, f"#GPROMOTE \n\n**Globally Promoted User :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@hell_cmd(pattern="gdem ?(.*)")
async def _(event):
    i = 0
    sender = await event.get_sender()
    me = await event.client.get_me()
    hell = await eor(event, "`Demoting Globally...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
       k = await hell.edit("You can't Demote yourself !!")
       return
    try:
        if not rank:
            rank = "ㅤ"
    except:
        return await hell.edit("**ERROR !!**")
    if user:
        telchanel = [d.entity.id
                     for d in await event.client.get_dialogs()
                     if (d.is_group or d.is_channel)
                     ]
        rgt = ChatAdminRights(add_admins=None,
                               invite_users=None,
                                change_info=None,
                                 ban_users=None,
                                  delete_messages=None,
                                   pin_messages=None)
        for x in telchanel:
          try:
             await event.client(EditAdminRequest(x, user, rgt, rank))
             i += 1
             await hell.edit(f"**Demoting Globally In Chats :** `{i}`")
          except:
             pass
    else:
        await hell.edit(f"**Reply to a user !!**")
    await hell.edit(
        f"[{user.first_name}](tg://user?id={user.id}) **Was Demoted Globally In** `{i}` **Chats !!**"
    )
    await event.client.send_message(Config.LOGGER_ID, f"#GDEMOTE \n\n**Globally Demoted :** [{user.first_name}](tg://user?id={user.id}) \n\n**Total Chats :** `{i}`")


@hell_cmd(pattern="gban ?(.*)")
async def _(event):
    hell = await eor(event, f"`Gbanning from {clients} Clients...")
    reason = ""
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await eod(hell, "**To gban a user i need a userid or reply to his/her message!!**")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(hell, "🥴 **Nashe me hai kya lawde ‽**")
    if str(userid) in DEVLIST:
        return await eod(hell, "😑 **GBan my creator ?¿ Really‽**")
    if is_gbanned(userid):
        return await eod(
            hell,
            "This kid is already gbanned and added to my **Gban Watch!!**",
        )
    if H1:
        async for gfuck1 in H1.iter_dialogs():
            if gfuck1.is_group or gfuck1.is_channel:
                try:
                    await event.client.edit_permissions(gfuck1.id, userid, view_messages=False)
                    chats +=1
                except BaseException:
                    pass

    if H2:
        await hell.edit(f"**Gbanned from Client 1 !!** \n**Total Chats :** __{chats}__ \n\nImplementing Gban in Client 2...")
        async for gfuck2 in H2.iter_dialogs():
            if gfuck2.is_group or gfuck2.is_channel:
                try:
                    await H2.edit_permissions(gfuck2.id, userid, view_messages=False)
                    chats +=1
                except BaseException:
                    pass

    if H3:
        await hell.edit(f"**Gbanned!!** \n**Total Chats :** __{chats}__ \n\nImplementing Gban in Client 3...")
        async for gfuck3 in H3.iter_dialogs():
            if gfuck3.is_group or gfuck3.is_channel:
                try:
                    await H3.edit_permissions(gfuck3.id, userid, view_messages=False)
                    chats +=1
                except BaseException:
                    pass

    if H4:
        await hell.edit(f"**Gbanned!!** \n**Total Chats :** __{chats}__ \n\nImplementing Gban in Client 4...")
        async for gfuck4 in H4.iter_dialogs():
            if gfuck4.is_group or gfuck4.is_channel:
                try:
                    await H4.edit_permissions(gfuck4.id, userid, view_messages=False)
                    chats +=1
                except BaseException:
                    pass

    if H5:
        await hell.edit(f"**Gbanned!!** \n**Total Chats :** __{chats}__ \n\nImplementing Gban in Client 5...")
        async for gfuck5 in H5.iter_dialogs():
            if gfuck5.is_group or gfuck5.is_channel:
                try:
                    await H5.edit_permissions(gfuck5.id, userid, view_messages=False)
                    chats +=1
                except BaseException:
                    pass

    gbaner(userid)
    a = gvarstat("BAN_PIC")
    if a is not None:
        b = a.split(" ")
        c = []
        for d in b:
            c.append(d)
        gbpic = random.choice(c)
    else:
        gbpic = cjb
    cid = await client_id(event)
    hell_mention = cid[2]
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **beta majdur ko khodna 😪 aur** {hell_mention} **ko chodna... Kabhi sikhana nhi!! 😏**\n\n📍 Added to Gban Watch!!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    ogmsg = f"[{name}](tg://user?id={userid}) **Is now GBanned by** {hell_mention} **in**  `{chats}`  **Chats!! 😏**\n\n**📍 Also Added to Gban Watch!!**"
    if reason != "":
        ogmsg += f"\n**🔰 Reason :**  `{reason}`"
    if Config.ABUSE == "ON":
        await event.client.send_file(event.chat_id, gbpic, caption=gmsg)
        await hell.delete()
    else:
        await hell.edit(ogmsg)


@hell_cmd(pattern="ungban ?(.*)"))
async def _(event):
    hell = await eor(event, "`Ungban in progress...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(hell, "`Reply to a user or give their userid... `")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(hell, "`User is not gbanned.`")
    if H1:
        await hell.edit(f"Ungbaning in client 1... \n**Unbanned in :** `{chats}`")
        async for gfuck1 in H1.iter_dialogs():
            if gfuck1.is_group or gfuck1.is_channel:
                try:
                    await H1.edit_permissions(gfuck1.id, userid, view_messages=True)
                    chats += 1
                except BaseException:
                    pass
    if H2:
        await hell.edit(f"Ungbaning in client 2... \n**Unbanned in :** `{chats}`")
        async for gfuck2 in H2.iter_dialogs():
            if gfuck2.is_group or gfuck2.is_channel:
                try:
                    await H2.edit_permissions(gfuck2.id, userid, view_messages=True)
                    chats += 1
                except BaseException:
                    pass
    if H3:
        await hell.edit(f"Ungbaning in client 3... \n**Unbanned in :** `{chats}`")
        async for gfuck3 in H3.iter_dialogs():
            if gfuck3.is_group or gfuck3.is_channel:
                try:
                    await H3.edit_permissions(gfuck3.id, userid, view_messages=True)
                    chats += 1
                except BaseException:
                    pass
    if H4:
        await hell.edit(f"Ungbaning in client 4... \n**Unbanned in :** `{chats}`")
        async for gfuck4 in H4.iter_dialogs():
            if gfuck4.is_group or gfuck4.is_channel:
                try:
                    await H4.edit_permissions(gfuck4.id, userid, view_messages=True)
                    chats += 1
                except BaseException:
                    pass
    if H5:
        await hell.edit(f"Ungbaning in client 5... \n**Unbanned in :** `{chats}`")
        async for gfuck5 in H5.iter_dialogs():
            if gfuck5.is_group or gfuck5.is_channel:
                try:
                    await H5.edit_permissions(gfuck5.id, userid, view_messages=True)
                    chats += 1
                except BaseException:
                    pass

    ungbaner(userid)
    await hell.edit(
        f"📍 [{name}](tg://user?id={userid}) **is now Ungbanned from `{chats}` chats and removed from Gban Watch!!**",
    )


@hell_cmd(pattern="listgban$")
async def already(event):
    hmm = await eor(event, "`Fetching Gbanned users...`")
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            hel = user.chat_id
            hell = int(hel)
            try:
                tity = await event.client.get_entity(hell)
                name = tity.first_name
            except ValueError:
                name = "User"
            GBANNED_LIST += f"📍 [{name}](tg://user?id={hell}) (`{hell}`)\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await hmm.edit(GBANNED_LIST)


@H1.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await H1.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                except BaseException:
                    pass
            else:
                gban_watcher += f"Reported to @admins"
        await event.reply(gban_watcher)

if H2:
    @H2.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H2.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)

if H3:
    @H3.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H3.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)

if H4:
    @H4.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H4.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)

if H5:
    @H5.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim Id :**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H5.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)


@hell_cmd(pattern="gkick ?(.*)")
async def gkick(event):
    hell = await eor(event, f"`Kicking globally from {clients} clients...`")
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await eod(hell, "`Reply to some msg or add their id.`")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == ForGo10God:
        return await eod(hell, "**🥴 Nashe me hai kya lawde!!**")
    if str(userid) in DEVLIST:
        return await eod(hell, "**😪 I'm not going to gkick my developer!!**")
    if H1:
        await hell.edit("**Kicking globally in client 1...**")
        async for gkick1 in H1.iter_dialogs():
            if gkick1.is_group or gkick1.is_channel:
                try:
                    await H1.kick_participant(gkick1.id, userid)
                    chats += 1
                except BaseException:
                    pass
    if H2:
        await hell.edit(f"**Kicking globally in client 2...** \n\n**Chats :** `{chats}`")
        async for gkick2 in H2.iter_dialogs():
            if gkick2.is_group or gkick2.is_channel:
                try:
                    await H2.kick_participant(gkick2.id, userid)
                    chats += 1
                except BaseException:
                    pass
    if H3:
        await hell.edit(f"**Kicking globally in client 3...** \n\n**Chats :** `{chats}`")
        async for gkick3 in H3.iter_dialogs():
            if gkick3.is_group or gkick3.is_channel:
                try:
                    await H3.kick_participant(gkick3.id, userid)
                    chats += 1
                except BaseException:
                    pass
    if H4:
        await hell.edit(f"**Kicking globally in client 4...** \n\n**Chats :** `{chats}`")
        async for gkick4 in H4.iter_dialogs():
            if gkick4.is_group or gkick4.is_channel:
                try:
                    await H4.kick_participant(gkick4.id, userid)
                    chats += 1
                except BaseException:
                    pass
    if H5:
        await hell.edit(f"**Kicking globally in client 5...** \n\n**Chats :** `{chats}`")
        async for gkick5 in H5.iter_dialogs():
            if gkick5.is_group or gkick5.is_channel:
                try:
                    await H5.kick_participant(gkick5.id, userid)
                    chats += 1
                except BaseException:
                    pass

    a = gvarstat("BAN_PIC")
    if a is not None:
        b = a.split(" ")
        c = []
        for d in b:
            c.append(d)
        gbpic = random.choice(c)
    else:
        gbpic = cjb
    gkmsg = f"🏃 **Globally Kicked** [{name}](tg://user?id={userid})'s butts in {clients} clients!! \n\n📝 **Chats :**  `{chats}`"
    if Config.ABUSE == "ON":
        await event.client.send_file(event.chat_id, gbpic, caption=gkmsg, reply_to=reply)
        await hell.delete()
    else:
        await hell.edit(gkmsg)


@hell_cmd(pattern="gmute ?(.*)")
async def gm(event):
    private = False
    if event.is_private:
        await eor(event, "`Trying to gmute user...`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(event, "Need a user to gmute. Reply or give userid to gmute them..")
    name = (await event.client.get_entity(userid)).first_name
    event.chat_id
    await event.get_chat()
    if gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "This kid is already Gmuted.")
    if str(userid) in DEVLIST:
        return await eod(event, "**Sorry I'm not going to gmute them..**")
    try:
        gsql.gmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        if Config.ABUSE == "ON":
            await event.client.send_file(event.chat_id, shhh, caption=f"**(~‾▿‾)~ Chup [Madarchod](tg://user?id={userid}) ....**", reply_to=reply)
            await event.delete()
        else:
            await eor(event, "**Globally Muted [{name}](tg://user?id={userid}) !!**\n\n__Kid struggling to speak__ ♪～(´ε｀ )")


@hell_cmd(pattern="ungmute ?(.*)")
async def endgmute(event):
    private = False
    if event.is_private:
        await eor(event, "`Trying to ungmute !!`")
        await asyncio.sleep(2)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await eod(event,"Please reply to a user or add their into the command to ungmute them.")
    name = (await event.client.get_entity(userid)).first_name
    event.chat_id
    if not gsql.is_gmuted(userid, "gmute"):
        return await eod(event, "I don't remember I gmuted him...")
    try:
        gsql.ungmute(userid, "gmute")
    except Exception as e:
        await eod(event, "Error occured!\nError is " + str(e))
    else:
        await eor(event, f"**Unmuted [{name}](tg://user?id={userid}) Globally !!**")


@hell_cmd(incoming=True)
async def watcher(event):
    try:
        if gsql.is_gmuted(event.sender_id, "gmute"):
            await event.delete()
    except Exception as e:
        LOGS.info(str(e))


CmdHelp("globals").add_command(
  "gban", "<reply>/<userid>", "Globally Bans the mentioned user in 'X' chats you are admin with ban permission."
).add_command(
  "ungban", "<reply>/<userid>", "Globally Unbans the user in 'X' chats you are admin!"
).add_command(
  "listgban", None, "Gives the list of all GBanned Users."
).add_command(
  "gkick", "<reply>/<userid>", "Globally Kicks the user in 'X' chats you are admin!"
).add_command(
  "gmute", "<reply> or <userid>", "Globally Mutes the User."
).add_command(
  "ungmute", "<reply> or <userid>", "Globally Unmutes the gmutes user."
).add_command(
  "gpro", "<reply> or <username>", "Globally Promotes the mentioned user in all the chats you are admin with Add Admins permission."
).add_command(
  "gdem", "<reply> or <username>", "Globally Demotes the mentioned user in all the chats you have rights to demoted that user."
).add_info(
  "Global Admin Tool."
).add_warning(
  "✅ Harmlesss Module."
).add()
