from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
import html
from telethon import events
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from telethon.events import ChatAction
from hellbot.plugins.sql.gmute_sql import gmute, ungmute, is_gmuted, all_gmuted
from . import *


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
            await eor(event, "**Som3thing W3nt Wr0ng**\n`Can you please provide me a user id`")
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
            return await eor(event, "**Som3thing W3nt Wr0ng**\n", str(err))           
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await eor(event, str(err))
        return None
    return user_obj

@bot.on(hell_cmd(pattern=r"gban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"gban ?(.*)", allow_sudo=True))
async def gban(userbot):
    if userbot.fwd_from:
        return
    ids = userbot
    sender = await ids.get_sender()
    hum = await ids.client.get_me()
    if not sender.id == hum.id:
        hellbot = await eor(ids, "Trying to gban this retard!")
    else:
        hellbot = await eor(ids, "`Ok! Gbaning this piece of shit....`")
    hum = await userbot.client.get_me()
    await hellbot.edit(f"`🔥Global Ban Iz Cumin'💦.... Wait and watch nigga🚶`")
    my_mention = "[{}](tg://user?id={})".format(hum.first_name, hum.id)
    f"@{hum.username}" if hum.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        return await eod(hellbot, f"**Something W3NT Wrong 🤔**")
    if user:
        if str(user.id) in DEVLIST:
            return await eod(hellbot, f"**👨‍💻 This User Can't be Gbanned!! He is my developer**")
        try:
            await userbot.client(BlockRequest(user))
        except:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, view_messages=False)
                a += 1
                await hellbot.edit(f"Gbaning This retard🚶\n\nTotal Chats :- `{a}`")
            except:
                b += 1
    else:
        await eod(hellbot, f"`Either reply to a user or gib me user id/name`")
    try:
        if gmute(user.id) is False:
            return await eod(hellbot, f"**Error! User already gbanned.**")
    except:
        pass
    return await hellbot.edit(
        f"[{user.first_name}](tg://user?id={user.id}) Beta majdur ko khodna aur {hell_mention} ko chodna kabhi sikhana nhi.\n\n**Gban Successful 🔥\nAffected Chats😏 : {a} **"
    )


@bot.on(hell_cmd(pattern=r"ungban ?(.*)"))
@bot.on(sudo_cmd(pattern=r"ungban ?(.*)", allow_sudo=True))
async def gunban(userbot):
    if userbot.fwd_from:
        return
    ids = userbot
    sender = await ids.get_sender()
    hum = await ids.client.get_me()
    if not sender.id == hum.id:
        hellbot = await eor(ids, "`Trying to ungban this kid...`")
    else:
        hellbot = await eor(ids, "`Ungban in progress...`")
    hum = await userbot.client.get_me()
    await hellbot.edit(f"`Trying to ungban this kiddo...`")
    my_mention = "[{}](tg://user?id={})".format(hum.first_name, hum.id)
    f"@{hum.username}" if hum.username else my_mention
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        userbot.chat.title
    try:
        user, reason = await get_full_user(userbot)
    except:
        pass
    try:
        if not reason:
            reason = "Private"
    except:
        pass
        try:
            await userbot.client(UnblockRequest(user))
        except:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await hellbot.edit(f"Ok! Now Ungbaning this kiddo.\nChats:- `{a}`")
            except:
                b += 1
    else:
        await eod(hellbot, "**Reply to a user**")
    try:
        if ungmute(user.id) is False:
            return await eod(hellbot, "**Error! User already ungbanned.**")
    except:
        pass
    return await hellbot.edit(f"**[{user.first_name}](tg://user?id={user.id}) Aur bhai.... Aagya swaad.**\n\nUngban Successful 🔥\nChats :- `{a}`")


@bot.on(hell_cmd(pattern="listgban$"))
@bot.on(sudo_cmd(pattern="listgban$", allow_sudo=True))
async def already(event):
    gbanned_users = all_gmuted()
    GBANNED_LIST = "**Gbanned Users :**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            GBANNED_LIST += f"📍 [{user.sender}](tg://user?id={user.sender})\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await edit_or_reply(event, GBANNED_LIST)


@borg.on(ChatAction)
async def handler(kraken): 
   if kraken.user_joined or kraken.user_added:
       guser = await kraken.get_user()
       gmuted = is_gmuted(guser.id)
       if gmuted:
        for i in gmuted:
            if i.sender == str(guser.id):                                                                         
                chat = await kraken.get_chat()
                admin = chat.admin_rights
                creator = chat.creator   
                if admin or creator:
                 try:
                    await client.edit_permissions(kraken.chat_id, guser.id, view_messages=False)                              
                    await kraken.reply(
                     f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n"                      
                     f"**⚜️ Victim Id ⚜️**:\n[{guser.id}](tg://user?id={guser.id})\n"                   
                     f"**🔥 Action 🔥**  :\n`Banned this piece of shit....` **AGAIN!**")                                                
                 except:       
                    kraken.reply("`Sheit!! No permission to ban users.\n@admins ban this retard.\nGlobally Banned User And A Potential Spammer`\n**Make your group a safe place by cleaning this shit**")                   
                    return


CmdHelp("gban").add_command("gban", "<reply>/<id>/<username>", "Globally Bans the user from all the chats you are admin with ban right.").add_command("ungban", "<reply>/<id>/<username>", "Globally Unbans the user if gbanned previously.").add_command("listgban", None, "Gives the list of all gbanned users!").add_info("Global Ban.").add_warning("✅ Harmless Module.").add()
