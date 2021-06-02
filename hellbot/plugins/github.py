import os
import time
from datetime import datetime

from github import Github

from . import *

GIT_TEMP_DIR = "./userbot/temp/"

@bot.on(hell_cmd(pattern=r"commit"))
@bot.on(sudo_cmd(pattern=r"commit"))
async def download(event):
    if event.fwd_from:
        return
    if Config.GITHUB_ACCESS_TOKEN is None:
        await eod(event, "`Please ADD Proper Access Token from github.com`")
        return
    if Config.GIT_REPO_NAME is None:
        await eod(event, "`Please ADD Proper Github Repo Name of HellBot`")
        return
    hellbot = await eor(event, "Processing ...")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        time.time()
        print("Downloading to TEMP directory")
        downloaded_file_name = await bot.download_media(
            reply_message.media, GIT_TEMP_DIR
        )
    except Exception as e:
        await eod(hellbot, str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await hellbot.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        await hellbot.edit("Committing to Github....")
        await git_commit(downloaded_file_name, hellbot)


async def git_commit(file_name, hellbot):
    content_list = []
    access_token = Config.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding="utf-8")
    commit_data = file.read()
    repo = g.get_repo(Config.GIT_REPO_NAME)
    print(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        print(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await hellbot.edit("`File Already Exists`")
            create_file = False
    file_name = "hellbot/plugins/" + file_name
    if create_file == True:
        file_name = file_name.replace("./userbot/temp/", "")
        print(file_name)
        try:
            repo.create_file(
                file_name, "Uploaded New Plugin", commit_data, branch="master"
            )
            print("Committed File")
            ccess = Config.GIT_REPO_NAME
            ccess = ccess.strip()
            await hellbot.edit(
                f"`Commited On Your Github Repo`\n\n[Your STDPLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)"
            )
        except:
            print("Cannot Create Plugin")
            await eod(hellbot, "Cannot Upload Plugin")
    else:
        return await eod(hellbot, "`Committed Suicide`")


@bot.on(hell_cmd(pattern="github (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="github (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await bot.send_file(
            event.chat_id,
            caption="""Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}""".format(
                name, html_url, gh_type, company, blog, location, bio, created_at
            ),
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event,
        )
        await event.delete()
    else:
        await eor(event, "`{}`: {}".format(input_str, r.text))


CmdHelp("github").add_command(
  "commit", "<reply to a file>", "Uploads the file on github repo as provided in Heroku Config GIT_REPO_NAME. In short makes a commit to git repo from Userbot"
).add_command(
  "github", "<git username>", "Fetches the details of the given git username"
).add_info(
  "Github Hecks.."
).add_warning(
  "✅ Harmless Module."
).add()
