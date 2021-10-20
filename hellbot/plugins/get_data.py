import io
import string

from . import *
       
@hell_cmd(pattern="yaml$")
async def _(event):
    msg = await event.message.get_reply_message()
    yaml_text = yaml_format(msg)
    await eor(event, yaml_text, parse_mode=parse_pre)


@hell_cmd(pattern="json$")
async def _(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    if len(the_real_message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await eor(event, "`{}`".format(the_real_message))


CmdHelp("get_data").add_command(
  "yaml", "<reply>", "Gives out Data of replied msg."
).add_command(
  "json", "<reply>", "Gets the json data of the replied msg/media from a user/bot/channel"
).add_info(
  "Data Snatch in YAML & JSON"
).add_warning(
  "✅ Harmless Module."
).add()
