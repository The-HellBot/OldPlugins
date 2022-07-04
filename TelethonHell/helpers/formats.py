import datetime
import string

from telethon.tl.tlobject import TLObject
from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate

PRINTABLE_SET = set(bytes(string.printable, "ascii"))
STR_LEN_MAX = 256
BYTE_LEN_MAX = 64


def parse_pre(text):
    text = text.strip()
    return (
        text,
        [
            MessageEntityPre(
                offset=0, length=len(add_surrogate(text)), language="potato"
            )
        ],
    )


def yaml_format(obj, indent=0):
    result = []
    if isinstance(obj, TLObject):
        obj = obj.to_dict()

    if isinstance(obj, dict):
        result.append(obj.get("_", "dict") + ":")
        if obj:
            items = obj.items()
            has_multiple_items = len(items) > 2
            if has_multiple_items:
                result.append("\n")
            indent += 2
            for k, v in items:
                if k == "_" or v is None:
                    continue
                formatted = yaml_format(v, indent)
                if not formatted.strip():
                    continue
                result.append(" " * (indent if has_multiple_items else 1))
                result.append(f"{k}: {formatted}")
                result.append("\n")
            result.pop()
            indent -= 2
            result.append(" " * indent)
    elif isinstance(obj, str):
        # truncate long strings and display elipsis
        result.append(repr(obj[:STR_LEN_MAX]))
        if len(obj) > STR_LEN_MAX:
            result.append("…")
    elif isinstance(obj, bytes):
        # repr() bytes if it's printable, hex like "FF EE BB" otherwise
        if all(c in PRINTABLE_SET for c in obj):
            result.append(repr(obj))
        else:
            if len(obj) > BYTE_LEN_MAX:
                result.append("<…>")
            else:
                result.append(" ".join(f"{b:02X}" for b in obj))
    elif isinstance(obj, datetime.datetime):
        # ISO-8601 without timezone offset (telethon dates are always UTC)
        result.append(obj.strftime("%Y-%m-%d %H:%M:%S"))
    elif hasattr(obj, "__iter__"):
        # display iterables one after another at the base indentation level
        result.append("\n")
        indent += 2
        for x in obj:
            result.append(" " * indent)
            result.append(yaml_format(x, indent))
            result.append("\n")
        result.pop()
        indent -= 2
        result.append(" " * indent)
    else:
        result.append(repr(obj))

    return "".join(result)
