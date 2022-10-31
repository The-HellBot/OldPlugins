import datetime
import os
import time

from TelethonHell.plugins import *

from github import Github


@hell_cmd(pattern="commit(?:\s|$)([\s\S]*)")
async def download(event):
    if Config.GITHUB_ACCESS_TOKEN is None:
        await parse_error(event, "`GITHUB_ACCESS_TOKEN` not configured.", False)
        return
    if Config.GIT_REPO_NAME is None:
        await parse_error(event, "`GIT_REPO_NAME` not configured.", False)
        return
    txts = event.text[8:]
    splt = txts.split("|")
    path = splt[0]
    branch = splt[1] or "master"
    hellbot = await eor(event, "Processing ...")
    if not os.path.isdir("./github/"):
        os.makedirs("./github/")
    start = datetime.datetime.now()
    reply_message = await event.get_reply_message()
    try:
        print("Downloading to TEMP directory")
        downloaded_file_name = await event.client.download_media(
            reply_message.media, "./github/"
        )
    except Exception as e:
        await parse_error(hellbot, e)
    else:
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await hellbot.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        await hellbot.edit("Committing to Github....")
        await git_commit(downloaded_file_name, path, branch, hellbot)


async def git_commit(file_name, path, branch, hellbot):
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
    path = path
    file_name = file_name
    if create_file == True:
        file_name = file_name.replace("./github/", "")
        print(file_name)
        try:
            repo.create_file(
                path,
                f"Uploaded file {file_name} by Hêllẞø†",
                commit_data,
                branch=branch,
            )
            print("Committed File")
            ccess = Config.GIT_REPO_NAME
            ccess = ccess.strip()
            await hellbot.edit(
                f"`Commited On Your Github Repo`\n\n[Your Commit](https://github.com/{ccess}/tree/{branch}/)"
            )
        except:
            print("Cannot Create Plugin")
            await parse_error(hellbot, "Cannot Upload File")
    else:
        return await parse_error(hellbot, "Committed Suicide")


git_user = """
**◈ {gh_type}:** [{name}]({html_url})

**◈ Blog:** __{blog}__
**◈ Repo:** __{public_repos}__
**◈ Company:** __{company}__
**◈ Location:** __{location}__
**◈ Followers:** __{followers}__
**◈ Following:** __{following}__
**◈ Created at:** __{created_at}__
**◈ Bio:** __{bio}__
"""

@hell_cmd(pattern="github(?:\s|$)([\s\S]*)")
async def _(event):
    username = event.text[8:].strip()
    r = requests.get(f"https://api.github.com/users/{username}")
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        bio = b["bio"]
        blog = b["blog"]
        company = b["company"]
        created_at = b["created_at"]
        followers = b["followers"]
        following = b["following"]
        gh_type = b["type"]
        html_url = b["html_url"]
        location = b["location"]
        name = b["name"]
        public_repos = b["public_repos"]
        git_text = git_user.format(
            gh_type=gh_type,
            name=name,
            html_url=html_url,
            blog=blog,
            public_repos=public_repos,
            company=company,
            location=location,
            followers=followers,
            following=following,
            created_at=created_at,
            bio=bio,
        )
        await event.client.send_file(
            event.chat_id,
            caption=git_text,
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event,
        )
        await event.delete()
    else:
        await parse_error(event, f"**{username}:** `{r.text}`", False)


CmdHelp("github").add_command(
    "commit", "<reply to a file> <path>|<branch>", "Uploads the file on github repo as provided in Heroku Config GIT_REPO_NAME. In short makes a commit to git repo from Userbot", "commit ./hellbot/plugins/example.py|master"
).add_command(
    "github", "<git username>", "Fetches the details of the given git username"
).add_info(
    "Github Hecks.."
).add_warning(
    "✅ Harmless Module."
).add()
