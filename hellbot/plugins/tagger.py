from telethon import custom, events
from telethon.tl.types import Channel
from telethon.utils import get_display_name

from . import *

if Config.TAG_LOGGER:
    tagger = int(Config.TAG_LOGGER)

if Config.TAG_LOGGER:
    @hell_handler(func=lambda e: (e.mentioned))
    async def all_messages_catcher(event):
        await event.forward_to(tagger)
        ammoca_message = ""
        __, _, hell_men = await client_id(event)
        kraken = await event.client.get_entity(event.sender_id)
        if kraken.bot or kraken.verified or kraken.support:
            return
        krakenm = f"[{get_display_name(kraken)}](tg://user?id={kraken.id})"
        where_ = await event.client.get_entity(event.chat_id)
        where_m = get_display_name(where_)
        button_text = "See the tag 📬"
        if isinstance(where_, Channel):
            message_link = f"https://t.me/c/{where_.id}/{event.id}"
        else:
            message_link = f"tg://openmessage?chat_id={where_.id}&message_id={event.id}"
        ammoca_message += f"👆 #TAG\n\n**• Tag By :** {krakenm} \n**• Tag For :** {hell_men} \n**• Chat :** [{where_m}]({message_link})"
        if tagger is not None:
            await tbot.send_message(
                entity=tagger,
                message=ammoca_message,
                link_preview=False,
                buttons=[[custom.Button.url(button_text, message_link)]],
                silent=True,
            )
        else:
            return


@hell_cmd(pattern="tagall (.*)")
async def _(event):
    mentions = event.text[8:]
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 50):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.client.send_message(event.chat_id, mentions)
    await event.delete()


CmdHelp("tagger").add_command(
  "tagall", "<text>", "Tags recent 100 users in the group."
).add_info(
  "Tagger."
).add_warning(
  "✅ Harmless Module."
).add()
