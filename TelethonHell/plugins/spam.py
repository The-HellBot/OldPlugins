import asyncio
from curses.ascii import isdigit
from typing import Any

from TelethonHell.plugins import *

Spam = SPAM()


async def spam(event, msg, count, reply_to, delay, bspam, uspam, media):
    # chat = (await event.get_chat()).title
    if media:
        what = "MEDIA_SPAM"
        for i in range(count):
            if Spam.spam == True:
                await event.client.send_file(event.chat_id, media)
            else:
                break
        Spam.spam = False
    elif uspam:
        what = "UNLIMITED_SPAM"
        while Spam.spam == True:
            await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
            count += 1
        Spam.spam = False
    elif bspam:
        what = "BREAK_SPAM"
        x = int(count % 100)
        y = int((count - x) / 100)
        a = 30
        for i in range(y):
            for j in range(100):
                if Spam.spam == True:
                    await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
                    a += 2
                    await asyncio.sleep(a)
                else:
                    break
        Spam.spam = False
    elif delay:
        what = "DELAY_SPAM"
        for i in range(count):
            if Spam.spam == True:
                await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
                await asyncio.sleep(delay)
            else:
                break
        Spam.spam = False
    else:
        what = "SPAM"
        for i in range(count):
            if Spam.spam == True:
                await event.client.send_message(event.chat_id, msg, reply_to=reply_to)
            else:
                break
        Spam.spam = False

    await event.client.send_message(
        Config.LOGGER_ID,
        f"#{what} \n\n**Spammed** `{count}` **messages in** {Spam.spam}",
    )


@hell_cmd(pattern="spam(?:\s|$)([\s\S]*)")
async def spammer(event):
    reply_to = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    if len(lists) < 2:
        return await parse_error(event, "Nothing given to spam!")
    elif len(lists) == 2:
        if str(lists[1]).isdigit():
            count = int(lists[1])
            msg = reply_to.text
        else:
            return await parse_error(event, "Spam count not given!")
    else:
        if str(lists[1]).isdigit():
            count = int(lists[1])
            msg = str(lists[2])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    Spam.spam = True
    await spam(event, msg, count, reply_to, None, None, None, None)


@hell_cmd(pattern="dspam(?:\s|$)([\s\S]*)")
async def dspam(event):
    reply_to = await event.get_reply_message()
    lists = event.text.split(" ", 3)
    if len(lists) < 3:
        return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    elif len(lists) == 3:
        if str(lists[1]).isdigit():
            delay = int(lists[1])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
        if str(lists[2]).isdigit():
            count = int(lists[2])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
        msg = reply_to.text
    else:
        if str(lists[1]).isdigit():
            delay = int(lists[1])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
        if str(lists[2]).isdigit():
            count = int(lists[2])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
        msg = str(lists[3])
    Spam.spam = True
    await spam(event, msg, count, reply_to, delay, None, None, None)


@hell_cmd(pattern="uspam(?:\s|$)([\s\S]*)")
async def uspam(event):
    reply_to = await event.get_reply_message()
    lists = event.text.split(" ", 1)
    if len(lists) < 2:
        if reply_to:
            msg = reply_to.text
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    else:
        msg = str(lists[1])
    Spam.spam = True
    await spam(event, msg, 0, reply_to, None, None, True, None)


@hell_cmd(pattern="bspam(?:\s|$)([\s\S]*)")
async def bspam(event):
    reply_to = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    if len(lists) < 2:
        return await parse_error(event, "Nothing given to spam!")
    elif len(lists) == 2:
        if str(lists[1]).isdigit():
            count = int(lists[1])
            msg = reply_to.text
        else:
            return await parse_error(event, "Spam count not given!")
    else:
        if str(lists[1]).isdigit():
            count = int(lists[1])
            msg = str(lists[2])
        else:
            return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    Spam.spam = True
    await spam(event, msg, count, reply_to, None, True, None, None)


@hell_cmd(pattern="mspam(?:\s|$)([\s\S]*)")
async def mspam(event):
    reply_to = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    if len(lists) < 2:
        return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    if not str(lists[1]).isdigit():
        return await parse_error(event, "Wrong spam syntax. Checkout help menu!")
    if not reply_to and not reply_to.media:
        return await parse_error(event, "Reply to a pic/gif/video/sticker to spam.")
    media = reply_to.media
    count = int(lists[1])
    Spam.spam = True
    await spam(event, None, count, reply_to, None, None, None, media)


@hell_cmd(pattern="endspam$")
async def spamend(event):
    if Spam.spam == True:
        Spam.spam = False
        Spam.chat = None
        await eod(event, "**Spam Terminated !!**")
    else:
        await eod(event, "**Nothing is spamming !!**")


CmdHelp("spam").add_command(
    "spam", "<number> <text>", "Sends the text 'X' number of times.", "spam 99 Hello"
).add_command(
    "mspam", "<reply to media> <number>", "Sends the replied media (gif/ video/ sticker/ pic) 'X' number of times", "mspam 100 <reply to media>"
).add_command(
    "dspam", "<delay> <spam count> <text>", "Sends the text 'X' number of times in 'Y' seconds of delay", "dspam 5 100 Hello"
).add_command(
    "uspam", "<reply to a msg> or <text>", "Spams the message unlimited times until you get floodwait error or stop it manually.", "uspam Hello"
).add_command(
    "bspam", "<count> <text or reply>", "Spams the message X times without floodwait. Breaks the spam count to avoid floodwait.", "bspam 9999 Hello"
).add_command(
    "endspam", None, "Terminates the ongoing spam."
).add_info(
    "Spammers Commands"
).add_warning(
    "❌ May Get Floodwait Error Or Limit Your Account"
).add()
