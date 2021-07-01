import asyncio
import os
import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins

from . import *

@bot.on(hell_cmd(pattern="picgen"))
@bot.on(sudo_cmd(pattern="picgen", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    url = "https://thispersondoesnotexist.com/image"
    response = requests.get(url)
    await eor(event, "`Creating a fake face...`")
    if response.status_code == 200:
      with open("HELLBOT.jpg", 'wb') as f:
        f.write(response.content)
    
    captin = f"Fake Image By {hell_mention}"
    fole = "HELLBOT.jpg"
    await bot.send_file(event.chat_id, fole, caption=captin)
    await event.delete()
    os.system("rm /root/hellbot/HELLBOT.jpg ")


@bot.on(hell_cmd(pattern="fake ?(.*)"))
@bot.on(sudo_cmd(pattern="fake ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with borg.action(event.chat_id, action):
        await asyncio.sleep(86400)  # type for 10 seconds

@bot.on(hell_cmd(pattern="gbam$"))
@bot.on(sudo_cmd(pattern="gbam$", allow_sudo=True))
async def gbun(event):
    if event.fwd_from:
        return
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n`"
    no_reason = "**Reason:**  __Madarchod Saala__"
    await event.edit("** Nikal Lawde❗️⚜️☠️**")
    asyncio.sleep(3.5)
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.sender_id))
        firstname = replied_user.user.first_name
        usname = replied_user.user.username
        idd = reply_message.sender_id
        # make meself invulnerable cuz why not xD
        if idd == 1432756163:
            await reply_message.reply(
                "`Wait a second, This is my master!`\n**How dare you threaten to ban my master nigger!**\n\n__Your account has been hacked! Pay 69$ to my master__ [HellBoy](https://t.me/ForGo10God) __to release your account__😏"
            )
        else:
            jnl = (
                "`Warning!! `"
                "[{}](tg://user?id={})"
                "` 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n\n`"
                "**Person's Name: ** __{}__\n"
                "**ID : ** `{}`\n"
            ).format(firstname, idd, firstname, idd)
            if usname == None:
                jnl += "**Victim Nigga's username: ** `Doesn't own a username!`\n"
            elif usname != "None":
                jnl += "**Victim Nigga's username** : @{}\n".format(usname)
            if len(gbunVar) > 0:
                gbunm = "`{}`".format(gbunVar)
                gbunr = "**Reason: **" + gbunm
                jnl += gbunr
            else:
                jnl += no_reason
            await reply_message.reply(jnl)
    else:
        mention = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\nReason: Not Given `"
        await event.reply(mention)
    await event.delete()


CmdHelp("fake").add_command(
  'fake', '<action>', 'This shows the fake action in the group  the actions are typing, contact, game ,location, voice, round, video, photo, document.'
).add_command(
  'gbam', '<reason> (optional)', 'Fake gban. Just for fun🤓'
).add_command(
  'picgen', None, 'Gives a fake face image'
).add_info(
  'Fake Actions.'
).add_warning(
  '✅ Harmless Module.'
).add()
