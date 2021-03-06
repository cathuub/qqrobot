"""
Autogenerate response to commands /help !help help.

For more info on usage:
/help -h
"""
# pylint: disable=invalid-name
# import asyncio
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import re
from time import time
import logzero
from logzero import logger

import nonebot
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.rule import to_me

from .parse_cmd import parse_cmd
from .fetch_plugin_info import fetch_plugin_info

# for ratelimit, will not respond twice within 10 seconds
_vars = dict(last_sent=0.0, interval=10)

logzero.loglevel(10)
nonebot_plugin_autohelp = nonebot.on_regex("^[/!#]?\s*(?:help|menu|帮助|菜单|caidan|info)|[/#]i",rule=to_me(),priority=1)

config = nonebot.Config()

logger.info("Loaded plugins: %s", [elm.name for elm in nonebot.get_loaded_plugins()])


@nonebot_plugin_autohelp.handle()
async def handle(bot: Bot, event: Event, state: dict):

    logger.debug(" nonebot_plugin_autohelp entry ")
    logger.debug("state: %s", state)

    #命令限制板块，暂时注释
    # _ = time() - _vars.get("last_sent")
    # logger.debug("check time interval: %.1f", _)
    # if _ < _vars["interval"]:
    #     logger.debug("Too soon... return ...")
    #     return

    # messages not startswith [/!#]?\s*help (case-insensitive
    #msg = event.get_plaintext()
    #logger.debug("msg: %s", msg)
    # if not re.findall(, msg, re.I)：查看命令是否匹配
    # if not patt.findall(msg):
    #     logger.debug("patt.findall(msg) False, return...")
    #     return

    parser = ArgumentParser(prog="help", formatter_class=ArgumentDefaultsHelpFormatter,)
    parser.add_argument(
        "-d", "--details", action="store_true", help="show __doc__ for each plugin"
    )
    parser.add_argument("params", nargs="*", help="list of parameters of type str")

    command = str(event.message).strip()
    logger.debug("command (str(event.message).strip()): %s", command)

    args, stdout, stderr = parse_cmd(command, parser)
    logger.debug("args: %s", args)

    if stdout or stderr:
        await bot.send(message="\n---\n".join([stdout, stderr]), event=event)
        return
    # keys = [
    #     "nickname",
    #     "command_start",
    #     "command_sep",
    # ]
    # info = "\n".join(
    #     f"{key}: {', '.join(val)}" for key, val in nonebot.Config() if key in keys
    # )

    # info=""
    # logger.debug("Respond... \n%s", info)
    #
    # logger.debug("args: %s", args)

    # args.params contains "details" or "detail" or "详细"
    #det = any(map(lambda x: x in args.params, ["details", "detail", "详细"]))

    # if args.details or det:
    #     try:
    #         plugin_info = fetch_plugin_info(details=True)
    #     except Exception as e:
    #         logger.error("fetch_plugin_info() exc: %s", e)
    #         plugin_info = str(e)
    #     try:
    #         await bot.send(message=f"info:{info}plugin:{plugin_info}end", event=event)
    #
    #         # reset timer if sent successfully
    #         _vars["last_sent"] = time()
    #     except Exception as e:
    #         logger.error(e)
    # else:
    try:
        plugin_info = fetch_plugin_info()
    except Exception as e:
        logger.error("fetch_plugin_info() exc: %s", e)
        plugin_info = str(e)
    try:
        if plugin_info:
            await nonebot_plugin_autohelp.finish(message=f"{plugin_info}")
        else:
            print("none")
            # reset timer if sent successfully
        #_vars["last_sent"] = time()
    except Exception as e:
        logger.error(e)
