from . import *


@hell_cmd(pattern="tweet(?:\s|$)([\s\S]*)")
async def tweet(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Tweeting ...")
    if text:
        tweeter = await event.client.inline_query(
            "TwitterStatusBot", f"{(deEmojify(text))}"
        )
        owo = await tweeter[0].click(Config.LOGGER_ID)
        stcr = await event.client.send_message(kraken.chat_id, owo)
        await hell.delete()
        await owo.delete()
        await unsave_stcr(stcr)
        await unsave_stcr(owo)


@hell_cmd(pattern="trump(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Trump is making a tweet ...")
    tweet = await trumptweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="modi(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Modi is making a tweet ...")
    tweet = await moditweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="mia(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Mia is making a tweet ...")
    tweet = await miatweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="dani(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Dani is making a tweet ...")
    tweet = await dani(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="pappu(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Pappu is making a tweet ...")
    tweet = await papputweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="sunny(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Sunny is making a tweet ...")
    tweet = await sunnytweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="johhny(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Johhny is making a tweet ...")
    tweet = await sinstweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="gandhi(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to tweet.")
    hell = await eor(event, "Gandhi is making a tweet ...")
    tweet = await taklatweet(deEmojify(text))
    await event.client.send_file(event.chat_id, tweet, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="cmm(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to change my mind.")
    hell = await eor(event, "Change my mind ...")
    mind = await changemymind(deEmojify(text))
    await event.client.send_file(event.chat_id, mind, reply_to=reply)
    await hell.delete()


@hell_cmd(pattern="kanna(?:\s|$)([\s\S]*)")
async def nekobot(event):
    lists = event.text.split(" ", 1)
    reply = await event.get_reply_message()
    text = None
    if reply and reply.message:
        text = reply.message()
    elif len(lists) == 2:
        text = lists[1].strip()
    else:
        return await parse_error(event, "No texts were given to kanna.")
    hell = await eor(event, "Kanna is writting ...")
    kanna = await kannagen(deEmojify(text))
    await event.client.send_file(event.chat_id, kanna, reply_to=reply)
    await hell.delete()


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
