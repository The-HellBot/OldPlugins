from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

hell_pic = Config.ALIVE_PIC or "https://telegra.ph/file/ea9e11f7c9db21c1b8d5e.mp4"
alive_c = f"__**🔥🔥𝕊𝕄𝕆𝕂𝔼ℝ𝔹𝕆𝕋 𝕀𝕊 𝕆ℕ𝕃𝕀ℕ𝔼🔥🔥**__\n\n"

 ┏━━━━━━━━━━━━━━━━
 ┣ ✪ **𝐌𝐚𝐬𝐭𝐞𝐫** ✪
 ┣
 ┣『 {hell_mention} 』
 ┣
 ┗━━━━━━━━━━━━━━━━  
┏━━━━━━━━━━━━━━━━
┣ ➤ **𝐓𝐞𝐥𝐞𝐭𝐨𝐧** 
┣      ┗ ⌜{tel_ver}⌟
┣━━━━━━━━━━━━━━━━
┣ ➤ **𝐒𝐦𝐨𝐤𝐞𝐫 𝐕𝐞𝐫𝐬𝐢𝐨𝐧**
┣      ┗ ⌜{hell_ver}⌟
┣━━━━━━━━━━━━━━━━
┣ ➤ **𝐒𝐮𝐝𝐨** 
┣      ┗ ⌜{is_sudo}⌟
┣━━━━━━━━━━━━━━━━
┣ ➤ **𝐂𝐡𝐚𝐧𝐧𝐞𝐥** 
┣      ┗  ⌜ [ᴊᴏɪɴ](https://t.me/SMOKER_UB) ⌟
┣━━━━━━━━━━━━━━━━
┣ ➤ **[𝐂𝐫𝐞𝐚𝐭𝐨𝐫]**(https://t.me/S_M_O_K_E_R_R)
┗━━━━━━━━━━━━━━━━
"""

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
**⚡ 𝐒𝐦𝐨𝐤𝐞𝐫𝐁𝐨𝐭 𝐈𝐬 𝐎𝐧𝐥𝐢𝐧𝐞 ⚡**
{Config.ALIVE_MSG}
**🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅**
**Telethon :**  `{tel_ver}`
**𝐒𝐦𝐨𝐤𝐞𝐫𝐁𝐨𝐭  :**  **{hell_ver}**
**Abuse    :**  **{abuse_m}**
**Sudo      :**  **{is_sudo}**
"""
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
