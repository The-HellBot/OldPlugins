import io

from TelethonHell.DB import snip_sql as sq
from TelethonHell.plugins import *


@hell_cmd(pattern=r"\#(\S+)")
async def incom_note(event):
    if Config.LOGGER_ID == 0:
        return
    try:
        if not (await event.get_sender()).bot:
            notename = event.text[1:]
            notename = notename.lower()
            note = sq.get_note(notename)
            message_id_to_reply = await reply_id(event)
            if note:
                if note.f_mesg_id:
                    msg_o = await event.client.get_messages(
                        entity=Config.LOGGER_ID, ids=int(note.f_mesg_id)
                    )
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        msg_o,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
                elif note.reply:
                    await event.delete()
                    await event.client.send_message(
                        event.chat_id,
                        note.reply,
                        reply_to=message_id_to_reply,
                        link_preview=False,
                    )
    except AttributeError:
        pass


@hell_cmd(pattern="snip(?:\s|$)([\s\S]*)")
async def add_snip(event):
    if Config.LOGGER_ID == 0:
        return await eod(event, "You need to setup  `LOGGER_ID`  to save snips...")
    trigger = event.pattern_match.group(1)
    stri = event.text.partition(trigger)[2]
    cht = await event.get_reply_message()
    cht_id = None
    trigger = trigger.lower()
    if cht and not stri:
        await event.client.send_message(
            Config.LOGGER_ID,
            f"#NOTE \n\nAdded Note with  `#{trigger}`. Below message is the output. \n**DO NOT DELETE IT**",
        )
        cht_o = await event.client.forward_messages(
            entity=Config.LOGGER_ID, messages=cht, from_peer=event.chat_id, silent=True
        )
        cht_id = cht_o.id
    elif cht:
        return await parse_error(event, f"Nothing given to add in snip.")
    if not cht:
        if stri:
            await event.client.send_message(
                Config.LOGGER_ID,
                f"#NOTE \n\nAdded Note with  `#{trigger}`. Below message is the output. \n**DO NOT DELETE IT**",
            )
            cht_o = await event.client.send_message(Config.LOGGER_ID, stri)
            cht_id = cht_o.id
            stri = None
        else:
            return await eod(
                event,
                f"Invalid Syntax. Check  `{hl}plinfo snips`  to get proper Syntax.",
            )
    success = "**Successfully {} snip with trigger**  `#{}` "
    if sq.add_note(trigger, stri, cht_id) is False:
        sq.rm_note(trigger)
        if sq.add_note(trigger, stri, cht_id) is False:
            return await eod(event, f"Error Adding Snip..")
        return await eor(event, success.format("updated", trigger))
    return await eor(event, success.format("added", trigger))


@hell_cmd(pattern="rmsnip(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = (event.pattern_match.group(1)).lower()
    if not input_str:
        return await eod(event, "I need a snip name to remove...")
    if input_str.startswith("#"):
        input_str = input_str.replace("#", "")
    try:
        sq.rm_note(input_str)
        await eod(event, "Removed  `#{}`  from snips..".format(input_str))
    except:
        await eod(event, "No snip saved with this trigger.")


@hell_cmd(pattern="listsnip$")
async def lsnote(event):
    all_snips = sq.get_notes()
    OUT_STR = "Available Snips:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 #{a_snip.keyword} \n"
    else:
        OUT_STR = f"No Snips. Start Saving using `{hl}snip`"
    if len(OUT_STR) > 4000:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "snips.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Snips",
                reply_to=event,
            )
            await event.delete()
    else:
        await eor(event, OUT_STR)


CmdHelp("snips").add_command(
    "snip","<reply> <trigger>", "Saves the replied message as a note with given trigger."
).add_command(
    "rmsnip", "<trigger>", "Removes the snip from your database."
).add_command(
    "listsnip", None, "Get the list of all of the available snips."
).add_info(
    "Sniped Notes."
).add_warning(
    "✅ Harmless Module."
).add()
