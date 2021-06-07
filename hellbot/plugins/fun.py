import random
from random import choice
import time
import re
import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from . import *


@bot.on(hell_cmd(pattern="slap ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="slap ?(.*)", allow_sudo=True))
async def who(event):
    if event.fwd_from:
        return
    replied_user = await get_user(event)
    caption = await slap(replied_user, event)
    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await edit_or_reply(event, caption)

    except:
        await edit_or_reply(event, "`Can't slap this nibba !!`")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.sender_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await edit_or_reply(event, "`I don't slap strangers !!`")
            return None

    return replied_user


async def slap(replied_user, event):
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username
    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)

    caption = temp.format(
        user1=hell_mention, user2=slapped, item=item, hits=hit, throws=throw
    )

    return caption

@bot.on(hell_cmd(pattern=f"randi$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"randi$", allow_sudo=True))
async def rendi(e):
   txt = random.choice(RENDISTR)
   await eor(e, txt)
   
   
@bot.on(hell_cmd(pattern=f"habuse$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"habuse$", allow_sudo=True))
async def thenus(e):
   txt = random.choice(THANOS_STRINGS)
   await eor(e, txt)
   
   
@bot.on(hell_cmd(pattern=f"fuk$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"fuk$", allow_sudo=True))
async def tapatap(e):
   txt = random.choice(FUK_STRINGS)
   await eor(e, txt)
   
   
@bot.on(hell_cmd(pattern=f"chu$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"chu$", allow_sudo=True))
async def chut(e):
   txt = random.choice(CHU_STRINGS)
   await eor(e, txt)
   
   
@bot.on(hell_cmd(pattern=f"noob$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"noob$", allow_sudo=True))
async def nub(e):
   txt = random.choice(NOOBSTR)
   await eor(e, txt)


@bot.on(hell_cmd(pattern=f"run$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"run$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(RUNSREACTS)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"gali$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gali$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(GAALI_STR)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"rape$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"rape$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(RAPE_STRINGS)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"abuse$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"abuse$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(ABUSE_STRINGS)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"gey$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gey$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(GEY_STRINGS)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"piro$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"piro$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(PRO_STRINGS)
    await eor(e, txt)


@bot.on(hell_cmd(pattern=f"insult$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"insult$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(INSULT_STRINGS)
    await eor(e, txt)

@bot.on(hell_cmd(pattern=f"hiabuse$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"hiabuse$", allow_sudo=True))
async def metoo(e):
    txt = random.choice(HIABUSE_STR)
    await eor(e, txt)

@bot.on(hell_cmd(pattern="cry$", outgoing=True))
@bot.on(sudo_cmd(pattern="cry$", allow_sudo=True))
async def cry(e):
        await eor(e, random.choice(CRI))

@bot.on(hell_cmd(pattern="cp(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="cp(?:|$)(.*)", allow_sudo=True))
async def copypasta(cp_e):
    if not cp_e.text[0].isalpha() and cp_e.text[0] not in ("/", "#", "@", "!"):
        textx = await cp_e.get_reply_message()
        message = cp_e.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await edit_or_reply(cp_e, "`😂🅱️IvE👐sOME👅text👅for✌️Me👌tO👐MAkE👀iT💞funNy!💦`")
            return
        reply_text = random.choice(EMOJIS)
        b_char = random.choice(
            message
        ).lower()  # choose a random character in the message to be substituted with 🅱️
        for owo in message:
            if owo == " ":
                reply_text += random.choice(EMOJIS)
            elif owo in EMOJIS:
                reply_text += owo
                reply_text += random.choice(EMOJIS)
            elif owo.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += owo.upper()
                else:
                    reply_text += owo.lower()
        reply_text += random.choice(EMOJIS)
        await edit_or_reply(cp_e, reply_text)

@bot.on(hell_cmd(pattern="owo(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="owo(?: |$)(.*)", allow_sudo=True))
async def faces(owo):
    """ UwU """
    if not owo.text[0].isalpha() and owo.text[0] not in ("/", "#", "@", "!"):
        textx = await owo.get_reply_message()
        message = owo.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await edit_or_reply(owo, "` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await edit_or_reply(owo, reply_text)

@bot.on(hell_cmd(pattern="react$", outgoing=True))
@bot.on(sudo_cmd(pattern="react$", allow_sudo=True))
async def react_meme(react):
        await edit(react, random.choice(FACEREACTS))

@bot.on(hell_cmd(pattern="clap(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="clap(?: |$)(.*)", allow_sudo=True))
async def claptext(memereview):
    """ Praise people! """
    if not memereview.text[0].isalpha() and memereview.text[0] not in (
        "/",
        "#",
        "@",
        "!",
    ):
        textx = await memereview.get_reply_message()
        message = memereview.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await edit_or_reply(memereview, "`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await edit_or_reply(memereview, reply_text)


CmdHelp("fun").add_command(
  "insult", None, "Sends some random insulting lines"
).add_command(
  "piro", None, "Sends some random lines for 'piro' guys"
).add_command(
  "gey", None, "Sends some random lines for geys (°^°)"
).add_command(
  "abuse", None, "Abuse the cunts"
).add_command(
  "rape", None, "No offence. Use and see -_-"
).add_command(
  "gali", None, "You know what this cmd is"
).add_command(
  "run", None, "Chala jaa bhosdike"
).add_command(
  "hiabuse", None, "Abuses in Hindi as well as English OwO"
).add_command(
  "randi", None, "Are you rendi?"
).add_command(
  "habuse", None, "Some of the abusive shayris"
).add_command(
  "fuk", None, "Use and see bruh"
).add_command(
  "chu", None, "Use and see"
).add_command(
  "noob", None, "Fuckin Noobs"
).add_command(
  "slap", "<reply>", "Slaps the replied user."
).add_command(
  "cry", None, "Y u do dis! I cri ebrytyme ಥ‿ಥ"
).add_command(
  "cp", "<text> or <reply>", "😂🅱️IvE👐sOME👅text👅for✌️Me👌tO👐MAkE👀iT💞funNy!💦"
).add_command(
  "owo", "<text> or <reply>", "OwO Try it yourself."
).add_command(
  "react", None, "Reacts randomly."
).add_command(
  "clap", "<reply> or <text>", "That kid needs clapping"
).add_info(
  "Bakchodi Hai Bass."
).add_warning(
  "✅ Harmless Module."
).add()
