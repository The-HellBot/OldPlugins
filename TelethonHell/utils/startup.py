from HellConfig import Config
from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights
from TelethonHell.clients.logger import LOGGER as LOGS
from TelethonHell.DB.gvar_sql import addgvar, gvarstat
from TelethonHell.helpers.int_str import make_int
from TelethonHell.version import __telever__


# Creates the logger group on first deploy and adds the helper bot
async def logger_id(client):
    desc = "A Bot Logger Group For Hellbot. DO NOT LEAVE THIS GROUP!!"
    try:
        grp = await client(
            functions.channels.CreateChannelRequest(
                title="Hellbot Logger", about=desc, megagroup=True
            )
        )
        grp_id = grp.chats[0].id
    except Exception as e:
        LOGS.error(f"{str(e)}")
        return
    
    if not str(grp_id).startswith("-100"):
        grp_id = int("-100" + str(grp_id))
    
    try:
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            manage_call=True,
        )
        grp = await client(functions.messages.ExportChatInviteRequest(peer=grp_id))
        await client(
            functions.channels.InviteToChannelRequest(
                channel=grp_id, users=[Config.BOT_USERNAME]
            )
        )
        await client(
            functions.channels.EditAdminRequest(
                grp_id, Config.BOT_USERNAME, new_rights, "Helper"
            )
        )
    except Exception as e:
        LOGS.error(f"{str(e)}")

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
    if Config.LOGGER_ID == 0:
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

<b><i>Version:</b></i> <code>{version}</code>
<b><i>Clients:</b></i> <code>{str(total)}</code>
<b><i>Sudo:</b></i> <code>{is_sudo}</code>
<b><i>Library:</b></i> <code>Telethon - {__telever__}</code>

<b><i>»» <u><a href='https://t.me/Its_HellBot'>†hê Hêllẞø†</a></u> ««</i></b>
"""
    await client.send_file(
        Config.LOGGER_ID,
        pic,
        caption=text,
        parse_mode="HTML",
        buttons=[[Button.url("HellBot Network", "https://t.me/HellBot_Networks")]],
    )


# Joins the hellbot chat and channel from all clients
async def join_it(client):
    if client:
        try:
            await client(functions.channels.JoinChannelRequest("@Its_HellBot"))
            await client(functions.messages.ImportChatInviteRequest("itu7bWHnA2djNjY1"))
        except BaseException:
            pass


# hellbot
