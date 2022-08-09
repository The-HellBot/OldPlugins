import io
import sys
import traceback

from . import *


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


CmdHelp("calculator").add_command(
    "calc", "Your expression", "Solves the given maths equation by BODMAS rule"
).add_info(
    "Calculator"
).add_warning(
    "✅ Harmless Module."
).add()
