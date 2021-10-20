from . import *


@hell_cmd(pattern=r"gdl")
async def g_download(event):
    hell = await eor(event, "Accessing gdrive...")
    drive_link = event.text[5:]
    await hell.edit(f"**Drive Link :** `{drive_link}`")
    file_id = await get_id(drive_link)
    await hell.edit("Downloading requested file from G-Drive...")
    file_name = await download_file_from_google_drive(file_id)
    await hell.edit(f"**File Downloaded !!**\n\n__Name :__ `{str(file_name)}`")

CmdHelp("gdrive").add_command(
  "gdl", "<gdrive link>", f"Downloads the file from gdirve to HellBot's local storage. Use {hl}upload <path> to upload it."
).add_info(
  "Google Drive Downloader"
).add_warning(
  "✅ Harmless Module."
).add()
