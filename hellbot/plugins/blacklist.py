import re
from telethon import events

from hellbot.sql import blacklist_sql as sq
from . import *


@bot.on(events.NewMessage(incoming=True))
async def on_new_message(event):
    if event.fwd_from:
        return
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = sq.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await event.reply("I do not have DELETE permission in this chat")
                sq.rm_from_blacklist(event.chat_id, snip.lower())
            break


@bot.on(hell_cmd(pattern="addblacklist ((.|\n)*)"))
@bot.on(sudo_cmd(pattern="addblacklist ((.|\n)*)", allow_sudo=True))
async def on_add_black_list(event):
    if event.fwd_from:
        return
    text = event.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    for trigger in to_blacklist:
        sq.add_to_blacklist(event.chat_id, trigger.lower())
    await edit_or_reply(
        event,
        "Added {} triggers to the blacklist in the current chat".format(
            len(to_blacklist)
        ),
    )


@bot.on(hell_cmd(pattern="rmblacklist ((.|\n)*)"))
@bot.on(sudo_cmd(pattern="rmblacklist ((.|\n)*)", allow_sudo=True))
async def on_delete_blacklist(event):
    if event.fwd_from:
        return
    text = event.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )

    successful = sum(
        1
        for trigger in to_unblacklist
        if sq.rm_from_blacklist(event.chat_id, trigger.lower())
    )

    await edit_or_reply(
        event, f"Removed {successful} / {len(to_unblacklist)} from the blacklist"
    )


@bot.on(hell_cmd(pattern="listblacklist$"))
@bot.on(sudo_cmd(pattern="listblacklist$", allow_sudo=True))
async def on_view_blacklist(event):
    if event.fwd_from:
        return
    all_blacklisted = sq.get_chat_blacklist(event.chat_id)
    OUT_STR = "Blacklists in the Current Chat:\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"👉 {trigger} \n"
    else:
        OUT_STR = "No Blacklists found. Start saving using `.addblacklist`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Blacklists in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await edit_or_reply(event, OUT_STR)


CmdHelp("blacklist").add_command(
  "addblacklist", "<word>/<words>", "The given word or words will be added to blacklist in that specific chat if any user sends then the message gets deleted.\n\nNote :- If you are adding more than one word at time via this, then remember that new word must be given in a new line that is not [hi hello]. It must be as [hi \n hello]"
).add_command(
  "rmblacklist", "<word>/<words>", "The given word or words will be removed from blacklist in that specific chat"
).add_command(
  "listblacklist", None, "Shows you the list of blacklist words in that specific chat"
).add_info(
  "Blacklist Words"
).add_warning(
  "✅ Harmless Module."
).add()
