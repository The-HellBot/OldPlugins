import asyncio
import io
import math
import os
import random
import textwrap
import urllib.request
from os import remove

from PIL import Image, ImageDraw, ImageFont
from telethon import Button, events
from telethon.errors import PackShortNameOccupiedError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (DocumentAttributeFilename, DocumentAttributeSticker,
                               InputMessagesFilterDocument, InputStickerSetID)
from telethon.utils import get_input_document

from TelethonHell.DB.gvar_sql import addgvar, gvarstat
from . import *


@hell_cmd(pattern="kang(?:\s|$)([\s\S]*)")
async def kang(event):
    await eor(event, "to do")
    # TO-DO


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
            third = await event.client.forward_messages("@Stickers", reply_message)
            fourth = await conv.get_response()
            if fourth.text.startswith("Current emoji:"):
                fifth = await conv.send_message(emoji)
                sixth = await conv.get_response()
            else:
                return await eod(hell, "That's not your sticker!")
        except YouBlockedUserError:
            return await parse_error(hell, "__Unblock @Stickers and try again.__", False)
        await hell.edit(f"{sixth.text}")


@hell_cmd(pattern="pkang(?:\s|$)([\s\S]*)")
async def _(event):
    # TO-DO
    await eor(event, "to do")


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
