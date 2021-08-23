import asyncio
import io
import math
import os
import random
import textwrap
import urllib.request
from os import remove

from PIL import Image, ImageDraw, ImageFont
from telethon import events
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import DocumentAttributeFilename, DocumentAttributeSticker, InputStickerSetID, MessageMediaPhoto, InputMessagesFilterDocument
from telethon.utils import get_input_document

from hellbot.sql.gvar_sql import addgvar, gvarstat, delgvar
from . import *

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
    "Hey! That's my sticker. Lemme get it back...",
    "Turn around, Go straight and f*ck off...",
]

hellbot = Config.STICKER_PACKNAME


@bot.on(hell_cmd(outgoing=True, pattern="kang"))
@bot.on(sudo_cmd(pattern="kang", allow_sudo=True))
async def kang(args):
    user = await bot.get_me()
    un = f"@{user.username}" if user.username else user.first_name
    un_ = user.username if user.username else ForGo10God
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            hell = await eor(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            hell = await eor(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            hell = await eor(args, f"`{random.choice(KANGING_STR)}`")
            await bot.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await eod(args, "`Unsupported File!`")
            return
    else:
        await eod(args, "`I can't kang that...`")
        return

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "😎"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        packname = f"Hellbot_{un_}_{pack}"
        packnick = (
            f"{hellbot} Vol.{pack}"
            if hellbot
            else f"{un}'s Hêllẞø† Vol.{pack}"
        )
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with bot.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"HellBot_{un_}_pack_{pack}"
                    packnick = (
                        f"{hellbot} Vol.{pack}"
                        if hellbot
                        else f"{un}'s Hêllẞø† Vol.{pack}"
                    )
                    await hell.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await hell.edit(
                            f"`Sticker added in a Different Pack !\
                            \nThis Pack is Newly created!\
                            \nYour pack can be found [here](t.me/addstickers/{packname})",
                            parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await hell.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await hell.edit("`Preparing a new pack....`")
            async with bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await hell.edit(
                        "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)

        await hell.edit(
            f"⚡** This Sticker iz [kanged](t.me/addstickers/{packname}) successfully to your pack **⚡",
            parse_mode="md",
        )


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


@bot.on(admin_cmd(outgoing=True, pattern="stkrinfo"))
@bot.on(sudo_cmd(pattern="stkrinfo", allow_sudo=True))
async def get_pack_info(event):
    if not event.is_reply:
        await edit_or_reply(event, "`I can't fetch info from black hole!!!`")
        return

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await edit_or_reply(event, "`Reply to a sticker to get the pack details`")
        return

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await edit_or_reply(event, "`Fetching details of the sticker pack, please wait..`")
    except BaseException:
        await edit_or_reply(event, "`This is not a sticker. Reply to a sticker.`")
        return

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        await edit_or_reply(event, "`This is not a sticker. Reply to a sticker.`")
        return

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"🔹 **Sticker Title :** `{get_stickerset.set.title}\n`"
        f"🔸 **Sticker Short Name :** `{get_stickerset.set.short_name}`\n"
        f"🔹 **Official :** `{get_stickerset.set.official}`\n"
        f"🔸 **Archived :** `{get_stickerset.set.archived}`\n"
        f"🔹 **Stickers In Pack :** `{len(get_stickerset.packs)}`\n"
        f"🔸 **Emojis In Pack :**\n{' '.join(pack_emojis)}"
    )

    await edit_or_reply(event, OUTPUT)


@bot.on(hell_cmd(pattern=r"delst ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"delst ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Reply to any user's message.`")
        return
    reply_message = await event.get_reply_message()
    chat = "@Stickers"
    reply_message.sender
    if reply_message.sender.bot:
        await edit_or_reply(event, "`Reply to actual user's message.`")
        return
    await event.edit("🥴 `Deleting sticker...`")
    async with bot.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=429000)
            )
            await conv.send_message("/delsticker")
            await conv.get_response()
            await asyncio.sleep(2)
            await bot.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("Please unblock @Stickers and try again")
            return
        if response.text.startswith("Sorry, I can't do this, it seems that you are not the owner of the relevant pack."):
            await event.edit("**🥴 Nashe me hai kya lawde!!**"
            )
        elif response.text.startswith("You don't have any sticker packs yet. You can create one using the /newpack command."):
            await event.edit("**😪 You don't have any sticker pack to delete stickers.** \n\n@Stickers :- 'Pehle Pack Bna Lamde 🤧'")
        elif response.text.startswith("Please send me the sticker."):
            await event.edit("**😪 Nashe me hai kya lawde**")
        elif response.text.startswith("Invalid pack selected."):
            await event.edit("**😪 Nashe me hai kya lawde**")
        else:
            await event.edit("**😐 Deleted that replied sticker, it will stop being available to Telegram users within about an hour.**")


@bot.on(hell_cmd(pattern=r"editst ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"editst ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Reply to any user's message.`")
        return
    reply_message = await event.get_reply_message()
    hell = event.pattern_match.group(1)
    chat = "@Stickers"
    reply_message.sender
    if reply_message.sender.bot:
        await edit_or_reply(event, "`Reply to actual user's message.`")
        return
    await event.edit("📝 `Editing sticker emoji...`")
    if hell == "":
        await event.edit("**🤧 Nashe me hai kya lawde**")
    else:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=429000)
                )
                await conv.send_message(f"/editsticker")
                await conv.get_response()
                await asyncio.sleep(2)
                await bot.forward_messages(chat, reply_message)
                await conv.get_response()
                await asyncio.sleep(2)
                await conv.send_message(f"{hell}")
                response = await response
            except YouBlockedUserError:
                await event.reply("Please unblock @Stickers and try again")
                return
            if response.text.startswith("Invalid pack selected."):
                await event.edit("**🥴 Nashe me h kya lawde**"
                )
            elif response.text.startswith("Please send us an emoji that best describes your sticker."):
                await event.edit("**🤧 Nashe me hai kya lawde**")
            else:
                await event.edit(f"**😉 Done!! Edited sticker emoji**\n\nNew Emoji(s) :- {hell}")


@bot.on(hell_cmd(pattern="pkang ?(.*)"))
@bot.on(sudo_cmd(pattern="pkang ?(.*)", allow_sudo=True))
async def _(event):
    hel_ = await eor(event, "`Preparing pack kang...`")
    rply = await event.get_reply_message()
    hell = event.text[7:]
    bot_ = Config.BOT_USERNAME
    bot_un = bot_.replace("@", "")
    user = await bot.get_me()
    un = f"@{user.username}" if user.username else user.first_name
    un_ = user.username if user.username else ForGo10God
    if not rply:
        return await eod(hel_, "`Reply to a stciker to kang that pack.`")
    if hell == "":
        pname = f"{un}'s Hêllẞø† Pack"
    else:
        pname = hell
    if rply and rply.media and rply.media.document.mime_type == "image/webp":
        hell_id = rply.media.document.attributes[1].stickerset.id
        hell_hash = rply.media.document.attributes[1].stickerset.access_hash
        got_stcr = await bot(
            functions.messages.GetStickerSetRequest(
                stickerset=types.InputStickerSetID(id=hell_id, access_hash=hell_hash)
            )
        )
        stcrs = []
        for sti in got_stcr.documents:
            inp = get_input_document(sti)
            stcrs.append(
                types.InputStickerSetItem(
                    document=inp,
                    emoji=(sti.attributes[1]).alt,
                )
            )
        try:
            gvarstat("PKANG")
        except BaseException:
            addgvar("PKANG", "0")
        x = gvarstat("PKANG")
        try:
            pack = int(x) + 1
        except BaseException:
            pack = 1
        await hel_.edit("`Starting kang process...`")
        try:
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=ForGo10God,
                    title=pname,
                    short_name=f"hell_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        except PackShortNameOccupiedError:
            await asyncio.sleep(1)
            await hel_.edit("`Pack name already occupied... making new pack`")
            pack += 1
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=ForGo10God,
                    title=pname,
                    short_name=f"hell_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", str(pack))
        await hel_.edit(f"⚡** This Sticker Pack iz [kanged](t.me/addstickers/{create_st.set.short_name}) successfully **⚡")
    else:
        await hel_.edit("Unsupported File. Please Reply to a sticker only.")


@bot.on(hell_cmd(pattern="text (.*)"))
@bot.on(sudo_cmd(pattern="text (.*)", allow_sudo=True))
async def sticklet(event):
    R = random.randint(0, 256)
    G = random.randint(0, 256)
    B = random.randint(0, 256)

    sticktext = event.pattern_match.group(1)
    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = "\n".join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230

    FONT_FILE = await get_font_file(event.client, "@HellFonts")

    font = ImageFont.truetype(FONT_FILE, size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(FONT_FILE, size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(
        ((512 - width) / 2, (512 - height) / 2), sticktext, font=font, fill=(R, G, B)
    )

    image_stream = io.BytesIO()
    image_stream.name = "Hellbot.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)


    await event.client.send_message(
        event.chat_id,
        "{}".format(sticktext),
        file=image_stream,
        reply_to=event.message.reply_to_msg_id,
    )
    try:
        os.remove(FONT_FILE)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id,
        filter=InputMessagesFilterDocument,
        limit=None,
    )
    font_file_message = random.choice(font_file_message_s)

    return await client.download_media(font_file_message)


@bot.on(hell_cmd(pattern="waifu(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="waifu(?: |$)(.*)", allow_sudo=True))
async def waifu(animu):
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await eod(animu, "Give some text... **PRO !!**")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=True if animu.is_reply else False,
        hide_via=True,
    )
    await animu.delete()


CmdHelp("stickers").add_command(
  "kang", "<emoji> <number>", "Adds the sticker to desired pack with a custom emoji of your choice. If emoji is not mentioned then default is 😎. And if number is not mentioned then Pack will go on serial wise. \n  ✓(1 pack = 120 non-animated stickers)\n  ✓(1 pack = 50 animated stickers)"
).add_command(
  "stkrinfo", "<reply to sticker>", "Gets all the infos of the sticker pack"
).add_command(
  "delst", "<reply to sticker>", "Deletes The Replied Sticker from your pack."
).add_command(
  "editst", "<reply to sticker> <new emoji>", "Edits the emoji of replied sticker of your pack."
).add_command(
  "text", "<word>", "Sends the written text in sticker format."
).add_command(
  "waifu", "<word>", "Waifu writes the word for you."
).add_command(
  "pkang", "<reply to a sticker> <pack name>", "Kangs all the stickers in replied pack to your pack. Also supports custom pack name. Just give name after command.", "pkang My kang pack"
).add_info(
  "Everything about Sticker."
).add_warning(
  "✅ Harmless Module."
).add()
