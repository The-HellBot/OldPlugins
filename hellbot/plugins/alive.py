from telethon import events, version
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User

from . import *

#-------------------------------------------------------------------------------

hell_pic = "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
alive_c = f"__**🔥🔥ɦɛʟʟɮօt ɨs օռʟɨռɛ🔥🔥**__\n\n"
alive_c += f"__↼ Øwñêr ⇀__ : 『 {hell_mention} 』\n\n"
alive_c += f"•♦• Telethon     :  `{version.__version__}` \n"
alive_c += f"•♦• Hêllẞø†       :  __**{hell_ver}**__\n"
alive_c += f"•♦• Sudo            :  `{is_sudo}`\n"
alive_c += f"•♦• Channel      :  {hell_channel}\n"


@bot.on(hell_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(hell):
    if hell.fwd_from:
        return
    await hell.get_chat()
    await hell.delete()
    await bot.send_file(hell.chat_id, hell_pic, caption=alive_c)
    await hell.delete()


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_info(
  "Check If Bot Is Alive"
).add_warning(
  "Harmless Module. No warnings."
).add()
