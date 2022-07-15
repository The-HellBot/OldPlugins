from TelethonHell.utils.extras import delete_hell as eod
from TelethonHell.utils.extras import edit_or_reply as eor


class CancelProcess(Exception):
    """
    Cancel Process
    """


async def parse_error(event, error, delete=False, time=10):
    if delete:
        await eod(event, f"**ERROR !!** \n\n`{error}`", time)
    else:
        await eor(event, f"**ERROR !!** \n\n`{error}`")


# hellbot
