from tkinter import Message

from nonebot import on_command
from nonebot.rule import to_me, regex
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message

from .data_source import gettime

time = on_command("世界时间", rule=to_me(), priority=1)#进行歌名操作


@time.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    country = str(event.get_message()).strip()  # 来一首之后的字符串处理
    if country:
        state["country"] = country  # 如果用户发送了参数则直接赋值


@time.got("country", prompt="你想查看什么国家的时间呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):

    country = state["country"]
    #需要将country处理为能识别的城市进行测试
    time_info = gettime(country)
    await time.finish(time_info)



