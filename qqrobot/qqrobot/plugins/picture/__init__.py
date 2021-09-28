"""
pic用于获得图片
"""
from nonebot import on_regex
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message

from .data_source import get_pic


# on_regex('来([1-9])张(.*)老师的图', rule=to_me(), priority=1)
picture = on_regex('来([1-9])张(.*)的图', rule=to_me(), priority=1)#进行图片操作


@picture.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    #获取数据
    num = state['_matched_groups'][0]
    tags = state['_matched_groups'][1].split(',')
    await bot.send(event, "正在图库中搜索！！！")
    pic_info = await get_pic(tags=tags,num=int(num))
    pic_info_fin = Message(pic_info)
    await picture.finish(pic_info_fin)

