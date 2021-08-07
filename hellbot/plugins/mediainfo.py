import os

from . import *


@bot.on(hell_cmd(pattern="mediainfo$"))
@bot.on(sudo_cmd(pattern="mediainfo$", allow_sudo=True))
async def mediainfo(event):
    HELL_MEDIA = None
    reply = await event.get_reply_message()
    if not reply:
        return await eod(event, "Reply to a media to fetch info...")
    if not reply.media:
        return await eod(event, "Reply to a media file to fetch info...")
    hell = await eor(event, "`Fetching media info...`")
    HELL_MEDIA = reply.file.mime_type
    if not HELL_MEDIA:
        return await hell.edit("Reply to a media file to fetch info...")
    elif HELL_MEDIA.startswith(("text")):
        return await hell.edit("Reply to a media file to fetch info ...")
    hel_ = await mediadata(reply)
    file_path = await reply.download_media(Config.TMP_DOWNLOAD_DIRECTORY)
    out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Unknown Format !!"
    paster = f"""
<h2>📃 MEDIA INFO 📃</h2>
<code>
{hel_}
</code>
<h2>🧐 MORE DETAILS 🧐</h2>
<code>
{out} 
</code>"""
    paste = await telegraph_paste(f"{HELL_MEDIA}", paster)
    await hell.edit(f"📌 Fetched  Media Info Successfully !! \n\n**Check Here :** [{HELL_MEDIA}]({paste})")
    os.remove(file_path)

CmdHelp("mediainfo").add_command(
  "mediainfo", "<reply to a media>", "Fetches the detailed information of replied media."
).add_info(
  "Everything About That Media."
).add_warning(
  "✅ Harmless Module."
).add()
