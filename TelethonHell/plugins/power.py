import asyncio
import sys

from asyncio.exceptions import CancelledError

from TelethonHell.DB.gvar_sql import addgvar, delgvar, gvarstat
from . import *


@hell_cmd(pattern="restart$")
async def re(hell):
    event = await eor(hell, "Restarting Hêllẞø† ...")
    try:
        await restart(event)
    except CancelledError:
        pass
    except Exception as e:
        LOGS.info(e)


@hell_cmd(pattern="reload$")
async def rel(event):
    await eor(event, "Reloading Hêllẞø†... Wait for few seconds...")
    await reload_hellbot()


@hell_cmd(pattern="shutdown$")
async def down(hell):
    event = await eor(hell, "`Turing Off Hêllẞø†...`")
    await asyncio.sleep(2)
    await event.edit("**[ ⚠️ ]** \n**Hêllẞø† is now turned off. Manually turn it on to start again.**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)


@hell_cmd(pattern="svar(?:\s|$)([\s\S]*)")
async def sett(event):
    hel_ = event.pattern_match.group(1)
    var_ = hel_.split(" ")[0].upper()
    val_ = hel_.split(" ")[1:]
    valu = " ".join(val_)
    hell = await eor(event, f"**Setting variable** `{var_}` **as** `{valu}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    elif valu == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}svar VARIABLE_NAME variable_value`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any DB variable named__ `{var_}`. __Check spelling or get full list by__ `{hl}vars`")
    try:
        addgvar(var_, valu)
    except Exception as e:
        return await eod(hell, f"**ERROR !!** \n\n`{e}`")
    await eod(hell, f"**Variable Added Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{valu}`")


@hell_cmd(pattern="gvar(?:\s|$)([\s\S]*)")
async def gett(event):
    var_ = event.pattern_match.group(1).upper()
    hell = await eor(event, f"**Getting variable** `{var_}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}gvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any variable named__ `{var_}`. __Check spelling or get full list by `{hl}vars`")
    try:
        sql_v = gvarstat(var_)
        os_v = os.environ.get(var_) or "None"
    except Exception as e:
        return await eod(hell, f"**ERROR !!** \n\n`{e}`")
    await hell.edit(f"**• OS VARIABLE:** `{var_}`\n**» OS VALUE :** `{os_v}`\n------------------\n**• DB VARIABLE:** `{var_}`\n**» DB VALUE :** `{sql_v}`\n")


@hell_cmd(pattern="dvar(?:\s|$)([\s\S]*)")
async def dell(event):
    var_ = event.pattern_match.group(1).upper()
    hell = await eor(event, f"**Deleting Variable** `{var_}`")
    if var_ == "":
        return await eod(hell, f"**Invalid Syntax !!** \n\nTry: `{hl}dvar VARIABLE_NAME`")
    if var_ not in db_config:
        return await eod(hell, f"__There isn't any variable named__ `{var_}`. Check spelling or get full list by `{hl}vars`")
    if gvarstat(var_):
        try:
            x = gvarstat(var_)
            delgvar(var_)
            await eod(hell, f"**Deleted Variable Successfully!!** \n\n**• Variable:** `{var_}` \n**» Value:** `{x}`")
        except Exception as e:
            await eod(hell, f"**ERROR !!** \n\n`{e}`")
    else:
        await eod(hell, f"**No variable named** `{var_}`")


CmdHelp("power").add_command(
    "restart", None, "Restarts your userbot. Redtarting Bot may result in better functioning of bot when its laggy"
).add_command(
    "reload", None, "Reloads the bot DB and SQL variables without deleting any external plugins if installed."
).add_command(
    "shutdown", None, "Turns off Hêllẞø†. Userbot will stop working unless you manually turn it on."
).add_command(
    "svar", "<variable name> <variable value>", "Sets the variable to SQL variables without restarting the bot.", "svar ALIVE_PIC https://telegra.ph/file/57bfe195c88c5c127a653.jpg"
).add_command(
    "gvar", "<variable name>", "Gets the info of mentioned variable from both SQL & OS.", "gvar ALIVE_PIC"
).add_command(
    "dvar", "<variable name>", "Deletes the mentioned variable from SQL variables without restarting the bot.", "dvar ALIVE_PIC"
).add_info(
    "Power Switch For Bot"
).add_warning(
    "✅ Harmless Module"
).add()
