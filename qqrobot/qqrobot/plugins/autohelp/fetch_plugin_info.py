"""Fetch plugin info such as aliases and __doc__."""
# pylint: disable=invalid-name
from typing import List, Union
from types import ModuleType

from pathlib import Path
import re
import ast
import logzero
from logzero import logger

import nonebot

logzero.loglevel(10)

#直接通过文件获取提醒内容，编写者需要自行填写
def extrac_info(file: Union[str, Path]) -> str:
    if not Path(file).is_file():
        logger.warning(" file [%s] does not exist or is not a file.", file)
        raise Exception(" file [%s] does not exist or is not a file." % file)
    try:
        text = Path(file).read_text(encoding="utf8")#读取文件下内容
    except Exception as e:
        logger.error(e)
        raise
    return text

def fetch_aliases(mod: ModuleType, attach_doc: bool = False) -> str:

    if Path(mod.__file__).name in ["__init__.py"]:#判断对应文件是否是init.py
        # is a package, search the folder for command/aliases info
        p_dir = Path(mod.__file__).parent
        info = ""
        for file in p_dir.glob("*.txt"):#获取包下的注释文件，注意后缀名必须是txt
            try:
                info = extrac_info(file)
            except Exception as e:
                logger.error("file: %s, extrac_info(file) exc: %s", file, e)
                info = ""
            if info.strip():
                break
    else:#没有？
        try:
            info = extrac_info(mod.__file__)
        except Exception as e:
            logger.error(
                "mod.__file__: %s, extrac_info(mod.__file__) exc: %s", mod.__file__, e
            )
            info = ""

    # #info = info.strip()
    # if attach_doc:
    #     if mod.__doc__ is None or not mod.__doc__.strip():
    #         info += f'\n(无文档。可在{mod.__file__}开始处以"""..."""形式添加文档'
    #     else:
    #         info += f"\n__doc__:{mod.__doc__}"

    return info


def fetch_plugin_info(
    # mod_list: Optional[Union[ModuleType, List[ModuleType]]] = None,
    mod_list: List[ModuleType] = None,
    details: bool = False,
) -> str:
    """Fetch plugin info such as aliases and __doc__.

    Args:
        mod_list: target modules
        details: whether to attach moduel.__doc__

    Returns:
        command and it's aliases, and module.__doc__ if details is True
    """
    if mod_list is None:
        mod_list = [elm.module for elm in nonebot.get_loaded_plugins()]

    # if isinstance(mod_list, ModuleType): mod_list = list(mod_list)

    res = ""
    for module in mod_list:
        res += fetch_aliases(module, attach_doc=details)

    return res
