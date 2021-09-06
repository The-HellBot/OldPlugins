import datetime
import inspect
import os
import re
import sys

from pathlib import Path

from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError, MessageNotModifiedError

from hellbot import LOGS, bot, tbot
from hellbot.clients import H2, H3, H4, H5
from hellbot.config import Config
from hellbot.helpers import *

sudo_users = list(Config.SUDO_USERS)

class REGEX:
    def __init__(self):
        self.regex = ""
        self.regex1 = ""
        self.regex2 = ""
REGEX_ = REGEX()


def hell_cmd(
    TelegramClient,
    pattern: str or tuple = None,
    allow_sudo: bool = True,
    edited: bool = True,
    forward_=False,
    **kwargs,
) -> callable:
    kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)
    kwargs.setdefault("forwards", forward_)
    if Config.BL_CHAT is not None:
        kwargs["blacklist_chats"] = True
        kwargs["chats"] = list(Config.BL_CHAT)
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    if pattern is not None:
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            REGEX_.regex1 = REGEX_.regex2 = re.compile(pattern)
        else:
            reg1 = "\\" + Config.HANDLER
            reg2 = "\\" + Config.SUDO_HANDLER
            REGEX_.regex1 = re.compile(reg1 + pattern)
            REGEX_.regex2 = re.compile(reg2 + pattern)

        def decorator(func):
            from hellbot import bot

            if not func.__doc__ is None:
                CMD_HELP[command[0]].append((func.__doc__).strip())
            if pattern is not None:
                if edited:
                    bot.add_event_handler(
                        wrapper,
                        MessageEdited(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                    )
                bot.add_event_handler(
                    wrapper,
                    NewMessage(pattern=REGEX_.regex1, outgoing=True, **kwargs),
                )
                if allow_sudo:
                    if edited:
                        bot.add_event_handler(
                            wrapper,
                            MessageEdited(
                                pattern=REGEX_.regex2,
                                from_users=list(Config.SUDO_USERS),
                                **kwargs,
                            ),
                        )
                    bot.add_event_handler(
                        wrapper,
                        NewMessage(
                            pattern=REGEX_.regex2,
                            from_users=list(Config.SUDO_USERS),
                            **kwargs,
                        ),
                    )
            else:
                if file_test in CMD_LIST and func in CMD_LIST[file_test]:
                    return None
                try:
                    CMD_LIST[file_test].append(func)
                except BaseException:
                    CMD_LIST.update({file_test: [func]})
                if edited:
                    bot.add_event_handler(func, events.MessageEdited(**kwargs))
                bot.add_event_handler(func, events.NewMessage(**kwargs))
                if H2:
                    if edited:
                        H2.add_event_handler(func, events.NewMessage(**kwargs))
                    H2.add_event_handler(func, events.NewMessage(**kwargs))
                if H3:
                    if edited:
                        H3.add_event_handler(func, events.NewMessage(**kwargs))
                    H3.add_event_handler(func, events.NewMessage(**kwargs))
                if H4:
                    if edited:
                        H4.add_event_handler(func, events.NewMessage(**kwargs))
                    H4.add_event_handler(func, events.NewMessage(**kwargs))
                if H5:
                    if edited:
                        H5.add_event_handler(func, events.NewMessage(**kwargs))
                    H5.add_event_handler(func, events.NewMessage(**kwargs))

        return decorator


def hellbot_cmd(
    TelegramClient,
    edited: bool = False,
    **kwargs,
) -> callable:
    kwargs["func"] = kwargs.get("func", lambda e: e.via_bot_id is None)

    def decorator(func):
        async def wrapper(check):
            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except MessageNotModifiedError:
                LOGS.error("Message was same as previous message")
            except MessageIdInvalidError:
                LOGS.error("Message was deleted or cant be found")
            except BaseException as e:
                LOGS.exception(e)

        from hellbot import tbot

            if edited is True:
                tbot.add_event_handler(func, events.MessageEdited(**kwargs))
            else:
                tbot.add_event_handler(func, events.NewMessage(**kwargs))

            return wrapper

        return decorator


# admin cmd or normal user cmd
def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        else:
            if len(Config.HANDLER) == 2:
                hellreg = "^" + Config.HANDLER
                reg = Config.HANDLER[1]
            elif len(Config.HANDLER) == 1:
                hellreg = "^\\" + Config.HANDLER
                reg = Config.HANDLER
            args["pattern"] = re.compile(hellreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})

    args["outgoing"] = True
    # decides that other users can use it or not
    # hellbot outgoing
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # blacklisted chats. 
    # hellbot will not respond in these chats.
    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats

    # blacklisted chats.
    # hellbot will not respond in these chats.
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]

    # plugin check for outgoing commands

    return events.NewMessage(**args)


def sudo_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
        else:
            if len(Config.SUDO_HANDLER) == 2:
                hellreg = "^" + Config.SUDO_HANDLER
                reg = Config.SUDO_HANDLER[1]
            elif len(Config.SUDO_HANDLER) == 1:
                hellreg = "^\\" + Config.SUDO_HANDLER
                reg = Config.HANDLER
            args["pattern"] = re.compile(hellreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )
            try:
                SUDO_LIST[file_test].append(cmd)
            except BaseException:
                SUDO_LIST.update({file_test: [cmd]})
    args["outgoing"] = True
    # outgoing check
    # hellbot
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]
    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True
    # blacklisted chats
    # hellbot won't respond here
    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if black_list_chats:
        args["chats"] = black_list_chats
    # blacklisted chats
    # hellbot won't respond here
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]
    # outgoing check
    # hellbot
    return events.NewMessage(**args)


on = bot.on


def on(**args):
    def decorator(func):
        async def wrapper(event):
            # check if sudo
            await func(event)

        client.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorater


# register decorate
def register(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", True)
    allow_sudo = args.get("allow_sudo", False)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    reg = re.compile("(.*)")
    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass

            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    def decorator(func):
        if not disable_edited:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


# command decorations
def command(**args):
    args["func"] = lambda e: e.via_bot_id is None

    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    pattern = args.get("pattern", None)
    allow_sudo = args.get("allow_sudo", None)
    allow_edited_updates = args.get("allow_edited_updates", False)
    args["incoming"] = args.get("incoming", False)
    args["outgoing"] = True
    if bool(args["incoming"]):
        args["outgoing"] = False

    try:
        if pattern is not None and not pattern.startswith("(?i)"):
            args["pattern"] = "(?i)" + pattern
    except BaseException:
        pass

    reg = re.compile("(.*)")
    if pattern is not None:
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = cmd.group(1).replace("$", "").replace("\\", "").replace("^", "")
            except BaseException:
                pass
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    if allow_sudo:
        args["from_users"] = list(Config.SUDO_USERS)
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
    del allow_sudo
    try:
        del args["allow_sudo"]
    except BaseException:
        pass

    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    if "allow_edited_updates" in args:
        del args["allow_edited_updates"]

    def decorator(func):
        if allow_edited_updates:
            bot.add_event_handler(func, events.MessageEdited(**args))
        bot.add_event_handler(func, events.NewMessage(**args))
        try:
            LOAD_PLUG[file_test].append(func)
        except BaseException:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator

# hellbot
