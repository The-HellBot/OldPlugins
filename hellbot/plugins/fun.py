import random
from random import choice

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
).add_info(
  "Bakchodi Hai Bass."
).add_warning(
  "✅ Harmless Module."
).add()
