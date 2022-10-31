import asyncio
import datetime
import os
import shutil
import tarfile
import time
import zipfile

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo
from TelethonHell.plugins import *


@hell_cmd(pattern="zip$")
async def _(event):
    if not event.is_reply:
        await parse_error(event, "Reply to a file to compress it.")
        return
    hell = await eor(event, "Zipping ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
            )
            directory_name = downloaded_file_name
            await eod(hell, downloaded_file_name)
        except Exception as e:
            await parse_error(hell, e)
    zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
        directory_name
    )
    await event.client.send_file(
        event.chat_id,
        directory_name + ".zip",
        caption="**Zipped!**",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )


@hell_cmd(pattern="tar(?:\s|$)([\s\S]*)")
async def _(event):
    input_str = event.pattern_match.group(1)
    hell = await eor(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
            directory_name = downloaded_file_name
            await hell.edit("Finished downloading to my local")
            to_upload_file = directory_name
            output = await create_archive(to_upload_file)
            is_zip = False
            if is_zip:
                check_if_file = await create_archive(to_upload_file)
                if check_if_file is not None:
                    to_upload_file = check_if_file
            await event.client.send_file(
                event.chat_id,
                output,
                caption="TAR By HellBot",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(output)
            except:
                pass
            await eod(hell, "Task Completed")
        except Exception as e:
            await parse_error(hell, e)


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        compressed_file_name += ".tar.gz"
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}",
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except:
                pass
            return_name = compressed_file_name
    return return_name


@hell_cmd(pattern="unzip$")
async def _(event):
    hell = await eor(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if not event.reply_to_msg_id:
        return await parse_error(hell, "Reply to zip file!")
    else:
        start = datetime.datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:
            await parse_error(hell, e)
        else:
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await hell.edit("Stored the zip to `{}` in {} seconds.".format(downloaded_file_name, ms))
        extracted = "./extracted"
        with zipfile.ZipFile(downloaded_file_name, "r") as zip_ref:
            zip_ref.extractall(extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        await hell.edit("Unzipping now")
        for single_file in filename:
            if os.path.exists(single_file):
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(Config.THUMB_IMG):
                        metadata = extractMetadata(createParser(Config.THUMB_IMG))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"UnZipped `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, hell, c_time, "Uploading ...")
                        ),
                    )
                    await eod(hell, "DONE!!!")
                except Exception as e:
                    await event.client.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id,
                    )
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


@hell_cmd(pattern="untar$")
async def _(event):
    hell = await eor(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    extracted = Config.TMP_DOWNLOAD_DIRECTORY + "extracted/"
    if not os.path.isdir(extracted):
        os.makedirs(extracted)
    thumb_image_path = Config.THUMB_IMG
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, hell, c_time, "Downloading ...")
                ),
            )
        except Exception as e:
            await parse_error(hell, e)
        else:
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await hell.edit(f"Stored the tar to `{downloaded_file_name}` in {ms} seconds.")
        with tarfile.TarFile.open(downloaded_file_name, "r") as tar_file:
            def is_within_directory(directory, target):
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
                prefix = os.path.commonprefix([abs_directory, abs_target])
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
                tar.extractall(path, members, numeric_owner=numeric_owner) 
            safe_extract(tar_file, path=extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        await hell.edit("Untarring now")
        for single_file in filename:
            if os.path.exists(single_file):
                caption_rts = os.path.basename(single_file)
                force_document = False
                supports_streaming = True
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"Untared `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, hell, c_time, "Uploading ...")
                        ),
                    )
                    await eod(hell, "DONE!!!")
                except Exception as e:
                    await event.client.send_message(
                        event.chat_id,
                        f"{caption_rts} caused `{str(e)}`",
                        reply_to=event.message.id,
                    )
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


CmdHelp("archiver").add_command(
    "zip", "Reply to file/media", "It will zip the file/media"
).add_command(
    "tar", "Reply to file/media", "It will tar the file/media"
).add_command(
    "unzip", "Reply to zip file", "It will unzip the zip file"
).add_command(
    "untar", "Reply to tar file", "It will untar the tar file"
).add_command(
    "compress", "Reply to file/media", "It will compress the replied media/file"
).add_info(
    "Better Archiver"
).add_warning(
    "✅ Harmless Module."
).add()
