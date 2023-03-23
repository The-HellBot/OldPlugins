import asyncio
import os
import sys

import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from TelethonHell.plugins import *

hellbot_info = "https://raw.githubusercontent.com/The-HellBot/Plugins/master/hellbot-info.json"
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH
UPSTREAM_REPO_URL = Config.UPSTREAM_REPO
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def hell_info(hellbot_info):
    infos = requests.get(hellbot_info).json()
    _version = infos["HELLBOT-INFO"]["version"]
    _release = infos["HELLBOT-INFO"]["release-date"]
    _branch = infos["HELLBOT-INFO"]["branch"]
    _author = infos["HELLBOT-INFO"]["author"]
    _coauthor = infos["HELLBOT-INFO"]["co-author"]
    return _version, _release, _branch, _author, _coauthor


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"🔥 **New UPDATE available for [{ac_br}]:\n\n📑 CHANGELOG:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await eor(event, "`Changelog is too big, view the file to see it.`")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
            thumb=hell_logo,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt")
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await eor(
        event,
        "✅ Successfully updated Hêllẞø†!\n\nBot is restarting please wait for a minute.",
    )
    args = [sys.executable, "-m", "hellbot"]
    os.execle(sys.executable, *args, os.environ)
    return


@hell_cmd(pattern="update(| now)$")
async def upstream(event):
    lists = event.text.split(" ", 1)
    conf = None
    if len(lists) == 2:
        conf = lists[1].strip()
    hell = await eor(event, "`Checking for new updates...`")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await parse_error(hell, "`HEROKU_API_KEY` __or__ `HEROKU_APP_NAME` __is not configured.__", False)
    txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await hell.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await hell.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await hell.edit(
                f"__The directory does not seem to be a git repository. Fix that by force updating!\n\nDo__ `{hl}update now`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await hell.edit(f"__Looks like you are using your own custom git branch__ `{ac_br}`. __Please checkout to official branch that is__ `{UPSTREAM_REPO_BRANCH}`")
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    _, _, hell_mention = await client_id(event)
    if changelog == "" and not force_update:
        _version, _release, _branch, _author, _coauthor = await hell_info(hellbot_info)
        output_ = f"**◈ Your Bot Version:** `{hellbot_version}` \n**◈ Owner:** {hell_mention} \n\n**◈ HellBot Global Version:** `{_version}` \n**◈ Release Date:** `{_release}` \n**◈ Official Repo Branch:** `{_branch}` \n**◈ Update By:** [{_author}](https://github.com/{_author}), [{_coauthor}](https://github.com/{_coauthor})"
        if str(_version) != str(hellbot_version):
            output_ += f"\n\n__Do__ `{hl}update build` __to update your HellBot to latest version.__"
        else:
            output_ += "\n\n__You are already on latest version.__"
        await hell.edit(output_)
        return repo.__del__()
    if not conf and not force_update:
        await print_changelogs(event, ac_br, changelog)
        return await hell.edit(f"🌚 Do `{hl}update build` to update your **Hêllẞø†** !!")
    if force_update:
        await hell.edit(f"**⥼ Synced Repo ⥽** \n\n__Do__ `{hl}update` __again to start updating ...__")


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        _, _, hell_mention = await client_id(event)
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if HEROKU_APP_NAME is None:
            await parse_error(event, "`HEROKU_APP_NAME` __is not configured.__", False)
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await parse_error(event, f"{txt}__Invalid Heroku Vars.__", False)
            return repo.__del__()
        _version, _release, _branch, _author, _coauthor = await hell_info(hellbot_info)
        await event.edit(
            f"<b><i>Hêllẞø† Docker Build In Progress !!!</b></i> \n\n<b><i><u>Update Information:</b></i></u> \n<b>• Branch:</b> {_branch} \n<b>• Release Date:</b> {_release} \n<b>• Version:</b> {_version} \n<b>• Authors:</b> <a href='https://github.com/{_author}'>{_author}</a>, <a href='https://github.com/{_coauthor}'>{_coauthor}</a>",
            link_preview=False,
            parse_mode="HTML",
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n**Error log:**\n`{error}`")
            return repo.__del__()
        build_status = app.builds(order_by="created_at", sort="desc")[0]
        if build_status.status == "failed":
           return await eod(event, "__Build Failed !!__")
        await event.edit(f"**Your Hêllẞø† Is UpToDate**\n\n**Version:**  __{hellbot_version}__\n**Oɯɳҽɾ:**  {hell_mention}")
    else:
        await parse_error(event, "`HEROKU_API_KEY` __is not configured.__")
    return


@hell_cmd(pattern="update build$")
async def upstream(event):
    hell = await eor(event, "`Hard-Update In Progress... \nPlease wait until docker build is finished...`")
    off_repo = UPSTREAM_REPO_URL
    os.chdir("/app")
    git_hell = f"rm -rf .git"
    try:
        await runcmd(git_hell)
    except BaseException:
        pass
    txt = "😕 `Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
    try:
        repo = Repo()
    except NoSuchPathError as error:
        await hell.edit(f"{txt}\n`directory {error}  not found`")
        return repo.__del__()
    except GitCommandError as error:
        await hell.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    _version, _release, _branch, _author, _coauthor = await hell_info(hellbot_info)
    await event.edit(
        f"<b><i>Hêllẞø† Docker Build In Progress !!</b></i> \n\n<b><i><u>Update Information:</b></i></u> \n<b>• Branch:</b> {_branch} \n<b>• Release Date:</b> {_release} \n<b>• Version:</b> {_version} \n<b>• Authors:</b> <a href='https://github.com/{_author}'>{_author}</a>, <a href='https://github.com/{_coauthor}'>{_coauthor}</a>",
        link_preview=False,
        parse_mode="HTML",
    )
    await deploy(event, repo, ups_rem, ac_br, txt)


CmdHelp("updater").add_command(
    "update", None, "Checks if any new update is available."
).add_command(
    "update now", None, "Soft-Update Your Hêllẞø†. Basically if you restart dyno it will go back to previous deploy."
).add_command(
    "update build", None, "Hard-Update Your Hêllẞø†. This won't take you back to your previous deploy. This will be triggered even if there is no changelog."
).add_info(
    "Hêllẞø† Updater."
).add_warning(
    "✅ Harmless Module."
).add()
