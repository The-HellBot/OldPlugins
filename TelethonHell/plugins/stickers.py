import asyncio
import io
import os
import random
import textwrap
import urllib.request

from PIL import Image, ImageDraw, ImageFont
from telethon import Button
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import DocumentAttributeSticker, InputStickerSetID
from telethon.utils import get_input_document
from TelethonHell.DB.gvar_sql import addgvar, gvarstat
from TelethonHell.plugins import *


@hell_cmd(pattern="kang(?:\s|$)([\s\S]*)")
async def kang(event):
    hell = await eor(event, "__**Starting sticker kang process ...**__")
    reply = await event.get_reply_message()
    lists = event.text.split(" ", 2)
    Sticker = STICKER()
    if len(lists) == 3:
        if lists[1].isdigit():
            Sticker.pack = int(lists[1])
            Sticker.emoji = lists[2]
        else:
            Sticker.emoji = lists[1]
            Sticker.pack = int(lists[2])
    elif len(lists) == 2:
        if lists[1].isdigit():
            Sticker.pack = int(lists[1])
        else:
            Sticker.emoji = lists[1]

    user = await event.client.get_me()
    ForGo10God, HELL_USER, _ = await client_id(event)
    nick = f"@{user.username}" if user.username else HELL_USER
    name = user.username if user.username else ForGo10God
    custompack = gvarstat("STICKER_PACKNAME")
    packname = f"HellBot_{name}_{Sticker.pack}"
    packnick = f"{custompack}" if custompack else f"{nick}'s Hêllẞø† Vol.{Sticker.pack}"
    is_sta = False
    is_ani = False
    is_vid = False
    photo = None

    if reply and reply.media:
        if reply.photo:
            photo = io.BytesIO()
            photo = await event.client.download_media(reply.photo, photo)
            is_sta = True
        elif "image" in reply.media.document.mime_type.split("/"):
            photo = io.BytesIO()
            await event.client.download_file(reply.media.document, photo)
            is_sta = True
        elif "tgsticker" in reply.media.document.mime_type:
            await event.client.download_file(reply.media.document, "AnimatedSticker.tgs")
            is_ani = True
            photo = 1
        elif "video" in reply.media.document.mime_type.split("/"):
            if reply.media.document.mime_type == "video/webm":
                await hell.edit("__Oow! A video sticker ...__ **[ ENCODING ]**")
                attributes = reply.media.document.attributes
                for attribute in attributes:
                    if isinstance(attribute, DocumentAttributeSticker):
                        if reply.media.document.size > 261120:
                            await VSticker(event, reply)
                        else:
                            await event.client.download_media(reply.media.document, "VideoSticker.webm")
            else:
                await hell.edit("__Oow! A video ...__ **[ CONVERTING ]**")
                await VSticker(event, reply)
            is_vid = True
            photo = 1
        else:
            return await eod(hell, "__Can't kang that 🔪__")
    else:
        return await eod(hell, "__Can't kang that 🔪__")
    await hell.edit("__**Adding this sticker to your pack...**__")

    cmd = "/newpack"
    file = io.BytesIO()
    if is_vid:
        cmd = "/newvideo"
        packname += "_vid"
        packnick += " (Video)"
    elif is_ani:
        cmd = "/newanimated"
        packname += "_ani"
        packnick += " (Animated)"
    else:
        image = await resize_photo(photo)
        file.name = "sticker.png"
        image.save(file, "PNG")

    response = urllib.request.urlopen(urllib.request.Request(f"http://t.me/addstickers/{packname}"))
    htmlstr = response.read().decode("utf8").split("\n")
    if (
        "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
        not in htmlstr
    ):
        async with event.client.conversation("@Stickers") as conv:
            try:
                await conv.send_message("/addsticker")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                resp = await conv.get_response()
                while ("50" in resp.message) or ("120" in resp.message) or is_vid:
                    if is_vid:
                        await conv.send_file("VideoSticker.webm")
                        resp = await conv.get_response()
                        if "50 video stickers" in resp.message:
                            await conv.send_message("/addsticker")
                        else:
                            break
                    try:
                        Sticker.pack += 1
                    except ValueError:
                        Sticker.pack = 1
                    packname = f"HellBot_{name}_{Sticker.pack}"
                    packnick = f"{custompack}" if custompack else f"{nick}'s Hêllẞø† Vol.{Sticker.pack}"
                    await hell.edit(f"__**Switching pack due to insufficient space ...**__ \n__Pack:__ `{Sticker.pack}`")
                    await conv.send_message(packname)
                    resp = await conv.get_response()
                    if resp.message == "Invalid set selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        if is_vid:
                            await conv.send_file("VideoSticker.webm")
                        elif is_ani:
                            await conv.send_file("AnimatedSticker.tgs")
                            os.remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        rsp = await conv.get_response()
                        if "Sorry, the file type is invalid." in rsp.text:
                            return await eod(hell, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                        await conv.send_message(Sticker.emoji)
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_ani:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await event.client.send_read_acknowledge(conv.chat_id)
                        await hell.edit(
                            f"**Sticker added in a Different Pack !**\nThis Pack is Newly created!\nYour pack can be found [here](t.me/addstickers/{packname})"
                        )
                        return
                if is_vid:
                    os.remove("VideoSticker.webm")
                    rsp = resp
                elif is_ani:
                    await conv.send_file("AnimatedSticker.tgs")
                    os.remove("AnimatedSticker.tgs")
                    rsp = await conv.get_response()
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await eod(hell, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
                await conv.send_message(Sticker.emoji)
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await parse_error(hell, "__Unblock @Stickers and try again.__", False)
    else:
        await hell.edit("__**Preparing a new pack....**__")
        async with event.client.conversation("@Stickers") as conv:
            await conv.send_message(cmd)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message(packnick)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if is_vid:
                await conv.send_file("VideoSticker.webm")
            elif is_ani:
                await conv.send_file("AnimatedSticker.tgs")
                os.remove("AnimatedSticker.tgs")
            else:
                file.seek(0)
                await conv.send_file(file, force_document=True)
            rsp = await conv.get_response()
            if "Sorry, the file type is invalid." in rsp.text:
                return await eod(hell, "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`")
            await conv.send_message(Sticker.emoji)
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.get_response()
            await conv.send_message("/publish")
            if is_ani:
                await conv.get_response()
                await conv.send_message(f"<{packnick}>")
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.send_message("/skip")
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.get_response()
            await conv.send_message(packname)
            await event.client.send_read_acknowledge(conv.chat_id)
            await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if is_vid and os.path.exists("./VideoSticker.webm"):
                os.remove("VideoSticker.webm")
    await tbot.send_message(
        Config.LOGGER_ID,
        f"#KANG #STICKER \n\nA sticker has been kanged into the pack of {HELL_USER}. Click below to see the pack!",
        buttons=[
          [Button.url("View Pack", f"t.me/addstickers/{packname}")],
          [Button.url(HELL_USER, f"tg://user?id={ForGo10God}")],
        ],
        parse_mode=None,
    )
    await eod(
        hell,
        f"⚡** This Sticker iz [kanged](t.me/addstickers/{packname}) successfully to your pack **⚡",
        20
    )


@hell_cmd(pattern="pkang(?:\s|$)([\s\S]*)")
async def _(event):
    hell = await eor(event, "`Preparing pack kang...`")
    reply = await event.get_reply_message()
    ForGo10God, HELL_USER, _ = await client_id(event)
    lists = event.text.split(" ", 1)
    bot_ = Config.BOT_USERNAME
    bot_un = bot_.replace("@", "")
    to_del = await event.client.send_message(bot_, "/start")
    user = await event.client.get_me()
    un = f"@{user.username}" if user.username else HELL_USER
    un_ = user.username if user.username else ForGo10God
    if not reply:
        return await eod(hell, "`Reply to a stciker to kang that pack.`")
    if len(lists) == 1:
        pname = f"{un}'s Hêllẞø† Pack"
    else:
        pname = lists[1].strip()
    if reply and reply.media and reply.media.document.mime_type == "image/webp":
        hell_id = reply.media.document.attributes[1].stickerset.id
        hell_hash = reply.media.document.attributes[1].stickerset.access_hash
        got_stcr = await event.client(
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
        x = gvarstat("PKANG")
        if x is None:
            addgvar("PKANG", 0)
            x = gvarstat("PKANG")
            pack = int(x) + 1
        else:
            pack = int(x) + 1
        await hell.edit("`Starting kang process...`")
        try:
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=ForGo10God,
                    title=pname,
                    short_name=f"hell_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", pack)
        except PackShortNameOccupiedError:
            await asyncio.sleep(1)
            await hell.edit("`Pack name already occupied... making new pack`")
            pack = int(pack) + 1
            create_st = await tbot(
                functions.stickers.CreateStickerSetRequest(
                    user_id=ForGo10God,
                    title=pname,
                    short_name=f"hell_{un_}_V{pack}_by_{bot_un}",
                    stickers=stcrs,
                )
            )
            addgvar("PKANG", pack)
        await tbot.send_message(
            Config.LOGGER_ID,
            f"#PKANG #STICKER \n\nA sticker pack has been kanged by {HELL_USER}. Click below to see the pack!",
            buttons=[
                [Button.url("View Pack", f"t.me/addstickers/{create_st.set.short_name}")],
                [Button.url(HELL_USER, f"tg://user?id={ForGo10God}")],
            ],
            parse_mode=None,
        )
        await eod(
            hell,
            f"⚡** This Sticker Pack iz [kanged](t.me/addstickers/{create_st.set.short_name}) successfully **⚡",
        )
    else:
        await hell.edit("Unsupported File. Please Reply to a sticker only.")
    await to_del.delete()


@hell_cmd(pattern="stkrinfo$")
async def get_pack_info(event):
    reply = await event.get_reply_message()
    if not reply and not reply.document:
        return await eod(event, "Reply to a sticker to get info.")
    try:
        stickerset_attr = reply.document.attributes[1]
        hell = await eor(event, "`Fetching details of the sticker pack, please wait..`")
    except BaseException:
        return await parse_error(event, "Replied media is not a sticker.")

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await parse_error(event, "Replied media is not a sticker.")

    get_stickerset = await event.client(
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
        f"<b><i>◈ Sticker Title:</b></i> <code>{get_stickerset.set.title}</code>\n"
        f"<b><i>◈ Sticker Short Name:</b></i> <code>{get_stickerset.set.short_name}</code>\n"
        f"<b><i>◈ Official:</b></i> <code>{get_stickerset.set.official}</code>\n"
        f"<b><i>◈ Archived:</b></i> <code>{get_stickerset.set.archived}</code>\n"
        f"<b><i>◈ Stickers In Pack:</b></i> <code>{len(get_stickerset.packs)}</code>\n"
        f"<b><i>◈ Emojis In Pack:</b></i> {' '.join(pack_emojis)}"
    )

    await hell.edit(OUTPUT, parse_mode='HTML')


@hell_cmd(pattern="delst(?:\s|$)([\s\S]*)")
async def _(event):
    reply = await event.get_reply_message()
    if not reply:
        return await eod(event, "Reply to a sticker to delete it.")
    hell = await eor(event, "🥴 `Deleting sticker...`")
    async with event.client.conversation("@Stickers") as conv:
        try:
            first = await conv.send_message("/delsticker")
            second = await conv.get_response()
            await asyncio.sleep(1)
            third = await event.client.forward_messages("@Stickers", reply)
            fourth = await conv.get_response()
        except YouBlockedUserError:
            return await parse_error(hell, "__Unblock @Stickers and try again.__", False)
        await hell.edit(fourth.text)


@hell_cmd(pattern="editst(?:\s|$)([\s\S]*)")
async def _(event):
    reply = await event.get_reply_message()
    if not reply:
        return await eod(event, "Reply to a sticker to edit its emoji.")
    lists = event.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(event, "No emoji given to change into.")
    emoji = lists[1].strip()
    hell = await eor(event, f"📝 `Editing sticker emoji to {emoji}`")
    async with event.client.conversation("@Stickers") as conv:
        try:
            first = await conv.send_message("/editsticker")
            second = await conv.get_response()
            await asyncio.sleep(1)
            third = await event.client.forward_messages("@Stickers", reply)
            fourth = await conv.get_response()
            if fourth.text.startswith("Current emoji:"):
                fifth = await conv.send_message(emoji)
                sixth = await conv.get_response()
            else:
                return await eod(hell, "That's not your sticker!")
        except YouBlockedUserError:
            return await parse_error(hell, "__Unblock @Stickers and try again.__", False)
        await hell.edit(f"{sixth.text}")


@hell_cmd(pattern="text(?:\s|$)([\s\S]*)")
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


@hell_cmd(pattern="waifu(?:\s|$)([\s\S]*)")
async def waifu(event):
    text = event.pattern_match.group(1)
    if not text:
        if event.is_reply:
            text = (await event.get_reply_message()).message
        else:
            await eod(event, "Give some text... **PRO !!**")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await event.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        event.chat_id,
        reply_to=event.reply_to_msg_id,
        silent=True if event.is_reply else False,
        hide_via=True,
    )
    await event.delete()


CmdHelp("stickers").add_command(
    "kang", "<emoji> <number>", "Adds the sticker to desired pack with a custom emoji of your choice. If emoji is not mentioned then default is 😎. And if number is not mentioned then Pack will go on serial wise. \n  ✓(1 pack = 120 static stickers)\n  ✓(1 pack = 50 animated & video stickers)"
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
