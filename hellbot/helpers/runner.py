import asyncio
import functools
import os
import shlex
import sys
from typing import Tuple
from uuid import uuid4


def rand_key():
    return str(uuid4())[:8]


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


def run_sync(func, *args, **kwargs):
    return asyncio.get_event_loop().run_in_executor(
        None, functools.partial(func, *args, **kwargs)
    )


def run_async(loop, coro):
    return asyncio.run_coroutine_threadsafe(coro, loop).result()

async def reload_hellbot():
    executable = sys.executable.replace(" ", "\\ ")
    args = [executable, "-m", "hellbot"]
    os.execle(executable, *args, os.environ)
    os._exit(143)


# hellbot
