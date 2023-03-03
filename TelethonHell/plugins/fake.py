import asyncio
import os

import requests
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins
from TelethonHell.plugins import *


@hell_cmd(pattern="fpic$")
async def _(event):
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "`Creating a fake face...`")
    url = "https://thispersondoesnotexist.com/image"
    response = requests.get(url)
    if response.status_code == 200:
        with open("HELLBOT.jpg", "wb") as f:
            f.write(response.content)
    else:
        return await parse_error(hell, "Failed to create Fake Face! Try again later.")
    await event.client.send_file(
        event.chat_id,
        "HELLBOT.jpg",
        caption=f"**Fake Image By {hell_mention}**",
        force_document=False,
    )
    await hell.delete()
    os.system("HELLBOT.jpg")


@hell_cmd(pattern="fake(?:\s|$)([\s\S]*)")
async def _(event):
    await event.delete()
    input_str = event.pattern_match.group(1)
    action = "typing"
    if input_str:
        action = input_str
    async with event.client.action(event.chat_id, action):
        await asyncio.sleep(86400)


@hell_cmd(pattern="gbam$")
async def gbun(event):
    gbunVar = event.text
    gbunVar = gbunVar[6:]
    mentions = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\n`"
    no_reason = "**Reason:**  __Madarchod Saala__"
    hell = await eor(event, "** Nikal Lawde❗️⚜️☠️**")
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(reply_message.sender_id))
        firstname = replied_user.users[0].first_name
        usname = replied_user.user.username
        idd = reply_message.sender_id
        if idd == 1432756163:
            await hell.edit(
                "`Wait a second, This is my master!`\n**How dare you threaten to ban my master nigger!**\n\n__Your account has been hacked! Pay 69$ to my master__ [HellBoy](https://t.me/ForGo10God) __to release your account__😏",
                link_preview=False,
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
            await hell.edit(jnl)
    else:
        mention = "`Warning!! User 𝙂𝘽𝘼𝙉𝙉𝙀𝘿 By Admin...\nReason: Not Given `"
        await hell.edit(mention)


CmdHelp("fake").add_command(
    "fake", "<action>", "This shows the fake action in the group. The actions are typing, contact, game, location, voice, round, video, photo, document."
).add_command(
    "gbam", "<reason> (optional)", "Fake gban. Just for fun🤓"
).add_command(
    "picgen", None, "Gives a fake face image"
).add_info(
    "Fake Actions."
).add_warning(
    "✅ Harmless Module."
).add()
