from telethon import events
from TelethonHell.DB.gvar_sql import addgvar, delgvar, gvarstat
from TelethonHell.DB.welcome_sql import (add_welcome, get_current_welcome,
                                         rm_welcome, update_welcome)
from TelethonHell.plugins import *


@bot.on(events.ChatAction)
async def _(event):
    ForGo10God, _, _ = await client_id(event)
    if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
        return
    cws = get_current_welcome(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = chat.title or "this chat"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws.reply:
                current_saved_welcome_message = cws.reply
        current_message = await event.reply(
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
        )
        update_welcome(event.chat_id, current_message.id)


if H2:
    @H2.on(events.ChatAction)
    async def _(event):
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
            return
        cws = get_current_welcome(event.chat_id)
        if (
            cws
            and (event.user_joined or event.user_added)
            and not (await event.get_user()).bot
        ):
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()
            title = chat.title or "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "<a href='tg://user?id={}'>{}</a>".format(
                a_user.id, a_user.first_name
            )
            my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
            first = a_user.first_name
            last = a_user.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws:
                if cws.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id)
                    )
                    file_media = msg_o.media
                    current_saved_welcome_message = msg_o.message
                elif cws.reply:
                    current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                parse_mode="html",
            )
            update_welcome(event.chat_id, current_message.id)


if H3:
    @H3.on(events.ChatAction)
    async def _(event):
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
            return
        cws = get_current_welcome(event.chat_id)
        if (
            cws
            and (event.user_joined or event.user_added)
            and not (await event.get_user()).bot
        ):
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()
            title = chat.title or "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "<a href='tg://user?id={}'>{}</a>".format(
                a_user.id, a_user.first_name
            )
            my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
            first = a_user.first_name
            last = a_user.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws:
                if cws.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id)
                    )
                    file_media = msg_o.media
                    current_saved_welcome_message = msg_o.message
                elif cws.reply:
                    current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                parse_mode="html",
            )
            update_welcome(event.chat_id, current_message.id)


if H4:

    @H4.on(events.ChatAction)
    async def _(event):
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
            return
        cws = get_current_welcome(event.chat_id)
        if (
            cws
            and (event.user_joined or event.user_added)
            and not (await event.get_user()).bot
        ):
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()
            title = chat.title or "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "<a href='tg://user?id={}'>{}</a>".format(
                a_user.id, a_user.first_name
            )
            my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
            first = a_user.first_name
            last = a_user.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws:
                if cws.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id)
                    )
                    file_media = msg_o.media
                    current_saved_welcome_message = msg_o.message
                elif cws.reply:
                    current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                parse_mode="html",
            )
            update_welcome(event.chat_id, current_message.id)


if H5:
    @H5.on(events.ChatAction)
    async def _(event):
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
            return
        cws = get_current_welcome(event.chat_id)
        if (
            cws
            and (event.user_joined or event.user_added)
            and not (await event.get_user()).bot
        ):
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()
            title = chat.title or "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "<a href='tg://user?id={}'>{}</a>".format(
                a_user.id, a_user.first_name
            )
            my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
            first = a_user.first_name
            last = a_user.last_name
            fullname = f"{first} {last}" if last else first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            my_fullname = f"{my_first} {my_last}" if my_last else my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws:
                if cws.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id)
                    )
                    file_media = msg_o.media
                    current_saved_welcome_message = msg_o.message
                elif cws.reply:
                    current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                parse_mode="html",
            )
            update_welcome(event.chat_id, current_message.id)


@hell_cmd(pattern="savewelcome(?:\s|$)([\s\S]*)")
async def save_welcome(event):
    reply = await event.get_reply_message()
    ForGo10God, _, _ = await client_id(event)
    lists = event.text.split(" ", 1)
    string = None
    if len(lists) == 2:
        string = lists[1].strip()
    msg_id = None
    if not string and not reply:
        return await parse_error(event, "Nothing given to add in welcome.")
    elif reply and reply.media and not string:
        await event.client.send_message(
            Config.LOGGER_ID,
            f"#WELCOME\
            \n**Group id:** {event.chat_id}\
            \nThe msg below is welcome note in {event.chat.title}\
            \nDont delete this msg else welcome won't work.",
        )
        msg_o = await event.client.forward_messages(
            entity=Config.LOGGER_ID, messages=reply, from_peer=event.chat_id, silent=True
        )
        msg_id = msg_o.id
    elif reply and not string:
        string = reply.text
    success = "`Welcome note {} for this chat.`"
    if add_welcome(event.chat_id, 0, string, msg_id) is True:
        addgvar(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}", "TRUE")
        return await eor(event, success.format("saved"))
    rm_welcome(event.chat_id)
    delgvar(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}")
    if add_welcome(event.chat_id, 0, string, msg_id) is True:
        addgvar(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}", "TRUE")
        return await eor(event, success.format("updated"))
    await eod(event, "Error while setting welcome in this group")


@hell_cmd(pattern="cleanwelcome$")
async def del_welcome(event):
    ForGo10God, _, _ = await client_id(event)
    if gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
        if rm_welcome(event.chat_id) is True:
            delgvar(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}")
            await eod(event, "Welcome Message deleted for this chat")
        else:
            await eod(event, "To delete a welcome note you need to save one first.")
    else:
        await eod(event, "To delete a welcome note you need to save one first.")


@hell_cmd(pattern="showwelcome$")
async def getwelcome(event):
    ForGo10God, _, _ = await client_id(event)
    if not gvarstat(f"WELCOME_{ForGo10God}_{str(event.chat_id)[1:]}"):
        return await eod(event, "No welcome notes here!")
    cws = get_current_welcome(event.chat_id)
    if not cws:
        return await eod(event, "`No welcome message saved here.`")
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=Config.LOGGER_ID, ids=int(cws.f_mesg_id))
        await eor(event, "Welcome note in this chat is...")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await eor(event, "Welcome note in this chat is...")
        await event.reply(cws.reply)


@hell_cmd(pattern="welcome_note$")
async def note(event):
    await eor(event, WELCOME_FORMAT)


CmdHelp("welcome").add_command(
    "savewelcome", "<reply>/<text>", "Sets the replied message as welcome note of that group"
).add_command(
    "cleanwelcome", None, "Cleans the current welcome message of that chat."
).add_command(
    "showwelcome", None, "Gets your current welcome message for that chat."
).add_command(
    "welcome_note", None, "Gives you a message containing all the formatting of welcome message."
).add_info(
    "Welcome Greetings."
).add_warning(
    "✅ Harmless Module."
).add()
