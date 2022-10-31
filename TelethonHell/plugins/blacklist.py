import io
import re

from TelethonHell.DB import blacklist_sql as sq
from TelethonHell.plugins import *


@hell_handler(incoming=True)
async def on_new_message(event):
    name = event.raw_text
    snips = sq.get_chat_blacklist(event.chat_id)
    for snip in snips:
        pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            try:
                await event.delete()
            except Exception:
                await parse_error(event, "I do not have DELETE permission in this chat")
                sq.rm_from_blacklist(event.chat_id, snip.lower())
            break


@hell_cmd(pattern="addblacklist(?:\s|$)([\s\S]*)")
async def on_add_black_list(event):
    text = event.pattern_match.group(1)
    to_blacklist = list({trigger.strip() for trigger in text.split("\n") if trigger.strip()})
    for trigger in to_blacklist:
        sq.add_to_blacklist(event.chat_id, trigger.lower())
    await eor(event, f"__Added__ `{to_blacklist}` __triggers to the blacklist in the current chat.__")


@hell_cmd(pattern="rmblacklist(?:\s|$)([\s\S]*)")
async def on_delete_blacklist(event):
    text = event.pattern_match.group(1)
    to_unblacklist = list({trigger.strip() for trigger in text.split("\n") if trigger.strip()})
    successful = sum(
        1
        for trigger in to_unblacklist
        if sq.rm_from_blacklist(event.chat_id, trigger.lower())
    )
    await eor(event, f"__Removed__ `{successful} / {len(to_unblacklist)}` __from the blacklist.__")


@hell_cmd(pattern="listblacklist$")
async def on_view_blacklist(event):
    all_blacklisted = sq.get_chat_blacklist(event.chat_id)
    if len(all_blacklisted) > 0:
        OUT_STR = "**Blacklists in the Current Chat:**\n"
        for trigger in all_blacklisted:
            OUT_STR += f"👉 `{trigger}` \n"
    else:
        OUT_STR = f"__No Blacklists found. Start saving using__`{hl}addblacklist`"
    if len(OUT_STR) > 4095:
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
        await eor(event, OUT_STR)


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
