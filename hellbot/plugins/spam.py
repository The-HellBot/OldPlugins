import asyncio
import os

from telethon import functions, types

from . import *

lg_id = Config.LOGGER_ID


@hell_cmd(pattern="spam ?(.*)")
async def spammer(event):
    msg_ = event.text[6:]
    counter = int(msg_.split(" ")[0])
    spam_message = msg_.replace(str(counter), "")
    reply_message = await event.get_reply_message()
    if counter > 100:
        return await eor(event, f"To spam more than 100 times use: \n`{hl}bigspam {counter} {spam_message}`")
    hell = await eor(event, f"Spamming {counter} times...")
    for i in range(counter):
        await event.client.send_message(event.chat_id, spam_message, reply_to=reply_message)
    await hell.delete()
    await event.client.send_message(lg_id, f"#SPAM \n\nSpammed  `{counter}`  messages!!")

@hell_cmd(pattern="bigspam ?(.*)")
async def bigspam(event):
    msg_ = event.text[9:]
    hellbot_count = int(msg_.split(" ")[0])
    reply_msg = await event.get_reply_message()
    if reply_msg:
        hell_spam = reply_msg
    else:
        hell_spam = msg_.replace(str(hellbot_count), "")
    for i in range(hellbot_count):
        await event.client.send_message(event.chat_id, hell_spam)
    await event.delete()
    await event.client.send_message(lg_id, f"#BIGSPAM \n\nBigspammed  `{hell_count}`  messages !!")

@hell_cmd("dspam (.*)")
async def spammer(event):
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    spamDelay = float(input_str.split(" ", 2)[0])
    counter = int(input_str.split(" ", 2)[1])
    spam_message = str(input_str.split(" ", 2)[2])
    await event.delete()
    for i in range(counter):
        await event.client.send_message(event.chat_id, spam_message)
        await asyncio.sleep(spamDelay)
    await event.client.send_message(lg_id, f"#DELAYSPAM \n\nSpammed `{counter}`  messages with delay of `{spamDelay}` seconds!!")

@hell_cmd(pattern="uspam ?(.*)")
async def _(event):
    reply_msg = await event.get_reply_message()
    hell = event.text[7:]
    if reply_msg:
        input_str = reply_msg
    else:
        input_str = hell
    await event.client.send_message(lg_id, f"#UNLIMITED_SPAM \n\nStarted Unlimited Spam. Will spam till floodwait. Do `{hl}restart` to stop.")
    x = 0
    while x < 69:
        await event.client.send_message(event.chat_id, input_str)

# Special Break Spam Module For HellBot Made By Chirag Bhargava.
# Team HellBot
@hell_cmd(pattern="bspam ?(.*)")
async def spammer(event):
    msg_ = event.text[7:]
    counter = int(msg_.split(" ")[0])
    reply_msg = await event.get_reply_message()
    if reply_msg:
        spam_message = reply_msg
    else:
        spam_message = msg_.replace(str(counter), "")
    rd = int(counter % 100)
    tot = int((counter - rd )/100)
    a = 30
    for q in range(tot):
        for p in range(100):
            await event.client.send_message(event.chat_id, spam_message)
        a = a + 2
        await asyncio.sleep(a)
    await event.delete()
    await event.client.send_message(lg_id, f"#BREAK_SPAM \n\nSpammed  {counter}  messages!!")

@hell_cmd(pattern="mspam (.*)")
async def tiny_pic_spam(event):
    try:
        counter = int(event.pattern_match.group(1).split(" ", 1)[0])
        reply_message = await event.get_reply_message()
        if (
            not reply_message
            or not event.reply_to_msg_id
            or not reply_message.media
            or not reply_message.media
        ):
            return await event.edit("```Reply to a pic/sticker/gif/video message```")
        message = reply_message.media
        for i in range(counter):
            await event.client.send_file(event.chat_id, message)
    except:
        return await event.reply(f"**Error**\nUsage `{hl}mspam <count> reply to a sticker/gif/photo/video`")
    await event.delete()


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
  "bigspam", "<count> <text>", "Sends the text 'X' number of times. This what hellbot iz known for. The Best BigSpam Ever", "bigspam 9999 Hello"
).add_info(
  "Spammers Commands"
).add_warning(
  "❌ May Get Floodwait Error Or Limit Your Account"
).add()
