"""
music用于获得网易云音乐推荐
"""
import random
import re

from nonebot import on_regex
from nonebot.adapters.cqhttp import MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


from .data_source import get_song, get_songlist, get_playlist_detail


# 来([1-9])首(.*)老师的歌
# 来([1-9])首和(.*)有关的歌
# 来([1-9])首(.*)  [歌名]
# 来1首ATRI推荐的歌

# 歌曲正则表达式


async def random_song(num):
    # 随机歌曲，也许需要缓存一个歌曲数组先暂时用歌单搜搜索
    return await abstract_song("atri")


async def man_song(name, num):  #需要从歌手入手
    pass

async def abstract_song(name):
    # 需要获取歌单id，然后再在歌单id内进行选取，注意空歌单
    song_lists =await get_songlist(name)
    # 获取id之后调用歌单详情函数，获取歌曲列表，默认第一个歌单？注意要选取num首歌
    num = random.randint(0, song_lists.__len__() - 1)
    list =await get_playlist_detail(song_lists[num])
    # 默认第一首歌曲返回？或者是在整个数组中选取一个随机数？也许需要缓存
    num=random.randint(0, list.__len__() - 1)
    return MessageSegment.music("163", list[num])


async def song(name):  # 依照歌名进行搜索，展示第一首，是否缓存？注意空数组
    songs =await get_song(name)
    if songs[0]:  # 如果搜索结果不为空就会走这个分支
        return MessageSegment.music("163", songs[0])
    return "你找的歌连网易云都没有呢···"


fun_song = {
    'ATRI推荐的歌': random_song,
    '(.*)老师的歌': man_song,
    '和(.*)有关的歌': abstract_song,
    '《(.*)》': song
}

# 来1个歌单(?)
music = on_regex('来(1|一)首(.*)', rule=to_me(), priority=1)


@music.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    # 获得后面的信息，用来判断之后的流程
    way = state['_matched_groups'][1]
    # 正则表达式进行查找
    # 循环匹配，一旦发现匹配需要退出循环
    for key, value in fun_song.items():
        song_tag = re.match(key, way)
        if song_tag:
            await bot.send(event, "正在网易云全球音乐库中搜索！！！")
            if song_tag.groups():
                # 获取关键tag，作为参数注入到函数中,注意为字符串
                await music.finish(await value(song_tag.group(1)))
            else:
                # 个人推荐歌曲,无需参数
                await music.finish(await value())
            break
    # print(state["_prefix"])
    # 来到这里说明歌曲命令不对


if __name__ == '__main__':
    print("")
