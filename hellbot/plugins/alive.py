from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

hell_pic = "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
alive_c = f"__**🔥🔥ɦɛʟʟɮօt ɨs օռʟɨռɛ🔥🔥**__\n\n"
alive_c += f"__↼ Øwñêr ⇀__ : 『 {hell_mention} 』\n\n"
alive_c += f"•♦• Telethon     :  `{tel_ver}` \n"
alive_c += f"•♦• Hêllẞø†       :  __**{hell_ver}**__\n"
alive_c += f"•♦• Sudo            :  `{is_sudo}`\n"
alive_c += f"•♦• Channel      :  {hell_channel}\n"

#-------------------------------------------------------------------------------

@bot.on(hell_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(hell):
    if hell.fwd_from:
        return
    await hell.get_chat()
    await hell.delete()
    await bot.send_file(hell.chat_id, hell_pic, caption=alive_c)
    await hell.delete()

msg = f"""

""" # Soon
botname = Config.BOT_USERNAME

@bot.on(hell_cmd(pattern="hell$"))
@bot.on(sudo_cmd(pattern="hell$", allow_sudo=True))
async def hell_a(event):
    try:
        hell = await bot.inline_query(botname, "alive")
        await hell[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "hell", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "✅ Harmless Module"
).add()
