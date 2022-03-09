from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

from hellbot import LOGS
from hellbot.config import Config
from hellbot.helpers.int_str import make_int
from hellbot.sql.gvar_sql import addgvar, gvarstat


# Creates the logger group on first deploy and adds the helper bot
async def logger_id(client):
    desc = "A Bot Logger Group For Hellbot. DO NOT LEAVE THIS GROUP!!"
    new_rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    try:
        grp = await client(functions.channels.CreateChannelRequest(title="Hellbot Logger", about=desc, megagroup=True))
        grp_id = grp.chats[0].id
        grp = await client(functions.messages.ExportChatInviteRequest(peer=grp_id))
        await client(functions.channels.InviteToChannelRequest(channel=grp_id, users=[Config.BOT_USERNAME]))
        await client(functions.channels.EditAdminRequest(grp_id, Config.BOT_USERNAME, new_rights, "Helper"))
    except Exception as e:
        LOGS.error(f"{str(e)}")
    if not str(grp_id).startswith("-100"):
        grp_id = int("-100" + str(grp_id))
    return grp_id


# Updates sudo cache on every restart
async def update_sudo():
    Sudo = Config.SUDO_USERS
    sudo = gvarstat("SUDO_USERS")
    if sudo:
        int_list = await make_int(gvarstat("SUDO_USERS"))
        for x in int_list:
            Sudo.append(x)


# Checks for logger group.
async def logger_check(bot):
    if Config.LOGGER_ID is None:
        if gvarstat("LOGGER_ID") is None:
            grp_id = await logger_id(bot)
            addgvar("LOGGER_ID", grp_id)
            Config.LOGGER_ID = grp_id
        Config.LOGGER_ID = int(gvarstat("LOGGER_ID"))


# Sends the startup message to logger group
async def start_msg(client, pic, version, total):
    is_sudo = "True" if Config.SUDO_USERS else "False"
    text = f"""
#START

<b><i>Version :</b></i> <code>{version}</code>
<b><i>Clients :</b></i> <code>{str(total)}</code>
<b><i>Sudo :</b></i> <code>{is_sudo}</code>

<b><i>»» <u><a href='https://t.me/Its_HellBot'>†hê Hêllẞø†</a></u> ««</i></b>
"""
    await client.send_file(
        Config.LOGGER_ID,
        pic,
        caption=text,
        parse_mode="HTML",
        buttons=[[Button.url("HellBot Network", "https://t.me/HellBot_Network")]],
    )


# Joins the hellbot chat and channel from all clients
async def join_it(client):
    if client:
        try:
            await client(functions.channels.JoinChannelRequest("@Its_HellBot"))
            await client(functions.messages.ImportChatInviteRequest('bZxlmdNFp1NjMDNh'))
        except BaseException:
            pass

# hellbot
