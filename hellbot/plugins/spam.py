import asyncio
import base64
import os

from telethon import functions, types
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import *

SUDO_WALA = Config.SUDO_USERS
lg_id = Config.LOGGER_ID

@bot.on(hell_cmd(pattern="spam (.*)"))
@bot.on(sudo_cmd(pattern="spam (.*)", allow_sudo=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:8])
        spam_message = str(e.text[8:])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        await e.client.send_message(
            lg_id, f"#SPAM \n\nSpammed  `{counter}`  messages!!"
        )


@bot.on(hell_cmd(pattern="bigspam"))
@bot.on(sudo_cmd(pattern="bigspam", allow_sudo=True))
async def bigspam(hell):
    if not hell.text[0].isalpha() and hell.text[0] not in ("/", "#", "@", "!"):
        hell_msg = hell.text
        hellbot_count = int(hell_msg[9:13])
        reply_msg = await hell.get_reply_message()
        if reply_msg:
            hell_spam = reply_msg
        else:
            hell_spam = str(hell.text[13:])
        for i in range(1, hellbot_count):
            await hell.respond(hell_spam)
        await hell.delete()
        await hell.client.send_message(
                lg_id, f"#BIGSPAM \n\nBigspammed  `{hell_count}`  messages !!"
        )


@bot.on(hell_cmd("dspam (.*)"))
@bot.on(sudo_cmd(pattern="dspam (.*)", allow_sudo=True))
async def spammer(e):
    if e.fwd_from:
        return
    input_str = "".join(e.text.split(maxsplit=1)[1:])
    spamDelay = float(input_str.split(" ", 2)[0])
    counter = int(input_str.split(" ", 2)[1])
    spam_message = str(input_str.split(" ", 2)[2])
    await e.delete()
    for _ in range(counter):
        await e.respond(spam_message)
        await asyncio.sleep(spamDelay)


@bot.on(hell_cmd(pattern="uspam ?(.*)"))
@bot.on(sudo_cmd(pattern="uspam ?(.*)", allow_sudo=True))
async def _(event):
    reply_msg = await event.get_reply_message()
    hell = event.pattern_match.group(1)
    if reply_msg:
        input_str = reply_msg
    else:
        input_str = hell
    await bot.send_message(lg_id, f"#UNLIMITED_SPAM \n\nStarted Unlimited Spam. Will spam till floodwait. Do `{hl}restart` to stop.")
    x = 0
    while x < 69:
        await bot.send_message(event.chat_id, input_str)


# Special Break Spam Module For HellBot Made By Chirag Bhargava.
# Team HellBot
@bot.on(hell_cmd(pattern="bspam ?(.*)"))
@bot.on(sudo_cmd(pattern="bspam ?(.*)", allow_sudo=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[7:11])
        reply_msg = await e.get_reply_message()
        if reply_msg:
            spam_message = reply_msg
        else:
            spam_message = str(e.text[12:])
        rd = int(counter % 100)
        tot = int((counter - rd )/100)
        a = 30
        for q in range(tot):
            for p in range(100):
                await asyncio.wait([e.respond(spam_message)])
            a = a + 2
            await asyncio.sleep(a)

        await e.delete()
        await e.client.send_message(
            lg_id, f"#BREAK_SPAM \n\nSpammed  {counter}  messages!!"
        )


@bot.on(hell_cmd(pattern="mspam (.*)"))
@bot.on(sudo_cmd(pattern="mspam (.*)", allow_sudo=True))
async def tiny_pic_spam(e):
    sender = await e.get_sender()
    me = await e.client.get_me()
    try:
        await e.delete()
    except:
        pass
    try:
        counter = int(e.pattern_match.group(1).split(" ", 1)[0])
        reply_message = await e.get_reply_message()
        if (
            not reply_message
            or not e.reply_to_msg_id
            or not reply_message.media
            or not reply_message.media
        ):
            return await e.edit("```Reply to a pic/sticker/gif/video message```")
        message = reply_message.media
        for i in range(1, counter):
            await e.client.send_file(e.chat_id, message)
    except:
        return await e.reply(
            f"**Error**\nUsage `{hl}mspam <count> reply to a sticker/gif/photo/video`"
        )


CmdHelp("spam").add_command(
  "spam", "<number> <text>", "Sends the text 'X' number of times.", "spam 99 Hello"
).add_command(
  "mspam", "<reply to media> <number>", "Sends the replied media (gif/ video/ sticker/ pic) 'X' number of times", "mspam 100 <reply to media>"
).add_command(
  "dspam", "<delay> <spam count> <text>", "Sends the text 'X' number of times in 'Y' seconds of delay", "dspam 5 100 Hello"
).add_command(
  "uspam", "<reply to a msg> or <text>", "Spams the message unlimited times until you get floodwait error.", "uspam Hello"
).add_command(
  "bspam", "<count> <text or reply>", "Spams the message X times without floodwait. Breaks the spam count to avoid floodwait.", "bspam 9999 Hello"
).add_command(
  "bigspam", "<count> <text>", "Sends the text 'X' number of times. This what hellbot iz known for. The Best BigSpam Ever", "bigspam 5000 Hello"
).add_info(
  "Spammers Commands"
).add_warning(
  "❌ May Get Floodwait Error Or Limit Your Account"
).add()
