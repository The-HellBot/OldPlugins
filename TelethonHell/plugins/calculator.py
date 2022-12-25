import io
import math
import sys
import traceback

from TelethonHell.plugins import *


@hell_cmd(pattern="calc(?:\s|$)([\s\S]*)")
async def _(event):
    cmd = event.text.split(" ", 1)[1]
    hell = await eor(event, "Calculating ...")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    san = f"print({cmd})"
    try:
        await aexec(san, hell)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sorry I can't find result for the given equation"
    final_output = f"**EQUATION**: `{cmd}` \n\n **SOLUTION**: \n`{evaluation}` \n"
    await hell.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


@hell_cmd(pattern="math(?:\s|$)([\s\S]*)")
async def maths(event):
    lists = event.text.split(" ")
    if len(lists) <= 2:
        return await parse_error(event, f"__Give valid arguments.__\n\n**Example:** `{hl}math sin 60`", False)
    if lists[1] == "sin":
        output = math.sin(float(lists[2]))
    elif lists[1] == "cos":
        output = math.cos(float(lists[2]))
    elif lists[1] == "tan":
        output = math.tan(float(lists[2]))
    elif lists[1] == "square":
        output = (float(lists[2]) * float(lists[2]))
    elif lists[1] == "cube":
        output = (float(lists[2]) * float(lists[2]) * float(lists[2]))
    elif lists[1] == "sqroot":
        output = math.sqrt(float(lists[2]))
    elif lists[1] == "factorial":
        output = math.factorial(float(lists[2]))
    elif lists[1] == "power":
        output = math.pow(float(lists[2]), float(lists[3]))
    else:
        return await parse_error(event, f"__Unknown operator__ `{lists[1]}`\n__Get a list of supported operators by__ `{hl}mathflag`\n__If you want this to be added in bot report it to developers.__", False)

    await eor(event, f"**Math:** __{lists[1]} {lists[2]}__ \n==> `{output}`")


@hell_cmd(pattern="mathflag$")
async def mathflag(event):
    flags = [
        "sin", "cos", "tan", "square", "cube", "sqroot", "factorial", "power"
    ]
    output = "**Supported operations of math are:**\n"
    for i in flags:
        output += f"\n> `{i}`"
    await eor(event, output)


CmdHelp("calculator").add_command(
    "calc", "Your expression", "Solves the given maths equation by BODMAS rule"
).add_command(
    "math", "<flag> <argument>", "Does a math problem for you.", "math sin 90"
).add_command(
    "mathflag", None, "Gets all the operations supported for math command."
).add_info(
    "Calculator"
).add_warning(
    "✅ Harmless Module."
).add()
