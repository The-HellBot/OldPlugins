import os

from TelethonHell.plugins import *


@hell_cmd(pattern="unpack$")
async def _(event):
    hell = await eor(event, "**Unpacking...**")
    reply = await event.get_reply_message()
    b = await event.client.download_media(reply)
    a = open(b, "r")
    c = a.read()
    a.close()
    if len(c) > 4095:
        try:
            x = await event.client.send_message(event.chat_id, f"{c[:4095]}", parse_mode=None, reply_to=reply)
            await x.respond(f"{c[4095:]}", parse_mode=None)
        except:
            pass
    else:
        await event.client.send_message(event.chat_id, f"{c}", parse_mode=None, reply_to=reply)
        await hell.delete()
    os.remove(b)


@hell_cmd(pattern="pack(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.text[6:]
    hell = await eor(event, f"Packing into `{input_str}`")
    a = await event.get_reply_message()
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    await hell.edit(f"Uploading `{input_str}`")
    await event.client.send_file(event.chat_id, input_str, reply_to=a)
    await hell.delete()
    os.remove(input_str)


CmdHelp("packer").add_command(
    "unpack", "<reply to a file>", "Read contents of file and send as a telegram message."
).add_command(
    "pack", "<reply to text> <filename . extension>", "Packs the text and sends as a file of given extension", "pack <reply to text> example.py"
).add_info(
    "Packer Iz Here !"
).add_warning(
    "✅ Harmless Module."
).add()
