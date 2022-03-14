import asyncio
import re

from telethon import events, utils as ut
from telethon.tl import types

from ..sql.filter_sql import get_filter, add_filter, remove_filter, get_all_filters, remove_all_filters
from ..sql.gvar_sql import gvarstat, addgvar, delgvar
from . import *


DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2

global last_triggered_filters_1
last_triggered_filters_1 = {}

global last_triggered_filters_2
last_triggered_filters_2 = {}

global last_triggered_filters_3
last_triggered_filters_3 = {}

global last_triggered_filters_4
last_triggered_filters_4 = {}

global last_triggered_filters_5
last_triggered_filters_5 = {}



@H1.on(events.NewMessage(incoming=True))
async def on_snip(event):
    global last_triggered_filters_1
    name = event.raw_text
    _id = event.chat_id
    ForGo10God, _, _ = await client_id(event)
    if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
        return
    snips = get_all_filters(_id)
    if _id in last_triggered_filters_1:
        if name in last_triggered_filters_1[_id]:
            return False
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference
                    )
                else:
                    media = None
                message_id = event.message.id
                if event.reply_to_msg_id:
                    message_id = event.reply_to_msg_id
                await event.reply(
                    snip.reply,
                    file=media
                )
                if _id not in last_triggered_filters_1:
                    last_triggered_filters_1[_id] = []
                last_triggered_filters_1[_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters_1[_id].remove(name)


if H2:
    @H2.on(events.NewMessage(incoming=True))
    async def on_snip(event):
        global last_triggered_filters_2
        name = event.raw_text
        _id = event.chat_id
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
            return
        snips = get_all_filters(_id)
        if _id in last_triggered_filters_2:
            if name in last_triggered_filters_2[_id]:
                return False
        if snips:
            for snip in snips:
                pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if snip.snip_type == TYPE_PHOTO:
                        media = types.InputPhoto(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    elif snip.snip_type == TYPE_DOCUMENT:
                        media = types.InputDocument(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    else:
                        media = None
                    message_id = event.message.id
                    if event.reply_to_msg_id:
                        message_id = event.reply_to_msg_id
                    await event.reply(
                        snip.reply,
                        file=media
                    )
                    if _id not in last_triggered_filters_2:
                        last_triggered_filters_2[_id] = []
                    last_triggered_filters_2[_id].append(name)
                    await asyncio.sleep(DELETE_TIMEOUT)
                    last_triggered_filters_2[_id].remove(name)


if H3:
    @H3.on(events.NewMessage(incoming=True))
    async def on_snip(event):
        global last_triggered_filters_3
        name = event.raw_text
        _id = event.chat_id
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
            return
        snips = get_all_filters(_id)
        if _id in last_triggered_filters_3:
            if name in last_triggered_filters_3[_id]:
                return False
        if snips:
            for snip in snips:
                pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if snip.snip_type == TYPE_PHOTO:
                        media = types.InputPhoto(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    elif snip.snip_type == TYPE_DOCUMENT:
                        media = types.InputDocument(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    else:
                        media = None
                    message_id = event.message.id
                    if event.reply_to_msg_id:
                        message_id = event.reply_to_msg_id
                    await event.reply(
                        snip.reply,
                        file=media
                    )
                    if _id not in last_triggered_filters_3:
                        last_triggered_filters_3[_id] = []
                    last_triggered_filters_3[_id].append(name)
                    await asyncio.sleep(DELETE_TIMEOUT)
                    last_triggered_filters_3[_id].remove(name)


if H4:
    @H4.on(events.NewMessage(incoming=True))
    async def on_snip(event):
        global last_triggered_filters_4
        name = event.raw_text
        _id = event.chat_id
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
            return
        snips = get_all_filters(_id)
        if _id in last_triggered_filters_4:
            if name in last_triggered_filters_4[_id]:
                return False
        if snips:
            for snip in snips:
                pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if snip.snip_type == TYPE_PHOTO:
                        media = types.InputPhoto(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    elif snip.snip_type == TYPE_DOCUMENT:
                        media = types.InputDocument(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    else:
                        media = None
                    message_id = event.message.id
                    if event.reply_to_msg_id:
                        message_id = event.reply_to_msg_id
                    await event.reply(
                        snip.reply,
                        file=media
                    )
                    if _id not in last_triggered_filters_4:
                        last_triggered_filters_4[_id] = []
                    last_triggered_filters_4[_id].append(name)
                    await asyncio.sleep(DELETE_TIMEOUT)
                    last_triggered_filters_4[_id].remove(name)


if H5:
    @H5.on(events.NewMessage(incoming=True))
    async def on_snip(event):
        global last_triggered_filters_5
        name = event.raw_text
        _id = event.chat_id
        ForGo10God, _, _ = await client_id(event)
        if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
            return
        snips = get_all_filters(_id)
        if _id in last_triggered_filters_5:
            if name in last_triggered_filters_5[_id]:
                return False
        if snips:
            for snip in snips:
                pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    if snip.snip_type == TYPE_PHOTO:
                        media = types.InputPhoto(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    elif snip.snip_type == TYPE_DOCUMENT:
                        media = types.InputDocument(
                            int(snip.media_id),
                            int(snip.media_access_hash),
                            snip.media_file_reference
                        )
                    else:
                        media = None
                    message_id = event.message.id
                    if event.reply_to_msg_id:
                        message_id = event.reply_to_msg_id
                    await event.reply(
                        snip.reply,
                        file=media
                    )
                    if _id not in last_triggered_filters_5:
                        last_triggered_filters_5[_id] = []
                    last_triggered_filters_5[_id].append(name)
                    await asyncio.sleep(DELETE_TIMEOUT)
                    last_triggered_filters_5[_id].remove(name)


@hell_cmd(pattern="filter(?:\s|$)([\s\S]*)")
async def on_snip_save(event):
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    ForGo10God, _, hell_mention = await client_id(event)
    _id = event.chat_id
    if msg:
        snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = ut.get_input_photo(msg.media.photo)
                snip['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = ut.get_input_document(msg.media.document)
                snip['type'] = TYPE_DOCUMENT
            if media:
                snip['id'] = media.id
                snip['hash'] = media.access_hash
                snip['fr'] = media.file_reference
        add_filter(_id, name, snip['text'], snip['type'], snip.get('id'), snip.get('hash'), snip.get('fr'))
        addgvar(f"FILTER_{ForGo10God}_{str(_id)[1:]}", "TRUE")
        await eod(event, f"**Filter Saved!** \n\n__• Client:__ {hell_mention} \n__• Keyword:__ {name}")
    else:
        await eod(event, f"Reply to a message with `{hl}filter keyword` to save the filter")


@hell_cmd(pattern="filters$")
async def on_snip_list(event):
    ForGo10God, _, _ = await client_id(event)
    _id = event.chat_id
    if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
        return await eod(event, f"No filters. Start saving using `{hl}filter`")
    all_snips = get_all_filters(_id)
    OUT_STR = "**Available Filters in the Current Chat :** \n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = f"No Filters. Start Saving using `{hl}filter`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event
            )
            await event.delete()
    else:
        await eor(event, OUT_STR)


@hell_cmd(pattern="stop(?:\s|$)([\s\S]*)")
async def on_snip_delete(event):
    name = event.pattern_match.group(1)
    ForGo10God, _, hell_mention = await client_id(event)
    _id = event.chat_id
    if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
        return await eod(event, "There aren't any filter in chat!")
    try:
        remove_filter(_id, name)
        await eod(event, f"**Filter Deleted!** \n\n__• Client:__ {hell_mention} \n__• Keyword:__ {name}")
    except Exception as e:
        await eod(event, f"**ERROR !!** \n\n`{e}`")


@hell_cmd(pattern="rmallfilters$")
async def on_all_snip_delete(event):
    ForGo10God, _, _ = await client_id(event)
    _id = event.chat_id
    if not gvarstat(f"FILTER_{ForGo10God}_{str(_id)[1:]}"):
        return await eod(event, "No filters in this chat!")
    try:
        delgvar(f"FILTER_{ForGo10God}_{str(_id)[1:]}")
        remove_all_filters(_id)
        await eod(event, f"**All the Filters in current chat deleted successfully**")
    except Exception as e:
        await eod(event, f"**ERORR !!** \n\n{str(e)}")


CmdHelp("filter").add_command(
  "filter", "reply to a msg with keyword", "Saves the replied msg as a reply to keyword. The bot will reply that msg wheneverthe keyword is mentioned."
).add_command(
  "filters", None, "Lists all the filters in chat"
).add_command(
  "rmallfilters", None, "Deletes all the filter saved in a chat."
).add_command(
  "stop", "keyword of saved filter", "Stops reply to the keyword mentioned."
).add_info(
  "Save Filters."
).add_warning(
  "✅ Harmless Module."
).add()
