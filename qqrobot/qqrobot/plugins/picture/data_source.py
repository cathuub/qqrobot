import asyncio

import httpx
from nonebot.adapters.cqhttp import MessageSegment


async def get_pic(tags,num=1):
    if len(tags) > 3:
        return '你输入的tag过多啦！！[CQ:image,file=ques.jpg]'

    if (num >= 4):
        return '要的图片太多了！[CQ:image,file=sepi.jpg]'

    setu_be_url = f'https://api.lolicon.app/setu/v2?num={num}'

    for tag in tags:
        if tag == 'r-18':
            setu_be_url += '&r18=1'
            continue
        setu_be_url += '&tag=' + tag

    async with httpx.AsyncClient() as client:
        req = await client.get(
            setu_be_url
        )
    pic_json = req.json()

    image_cq = ""
    if pic_json['data'].__len__() == 0:
        return "暂时没有相关tag的图片，是库内没有哦，Atri建议上p站搜索。"


    if pic_json['data'].__len__() < num:
        num=pic_json['data'].__len__()
        image_cq += MessageSegment.text(f'库内暂时没有那么多相关tag的图片，目前只有{num}张·····')

    for i in range(0, num):
        setu_author = pic_json['data'][i]['author']
        setu_pid = pic_json['data'][i]['pid']
        setu_url = pic_json['data'][i]['urls']['original']
        filename = setu_url.rindex('/')
        name = setu_url[filename + 1:]
        image_cq += f'画师:{setu_author}\npid:{setu_pid}[CQ:image,file={name},url={setu_url}]'

    return image_cq



if __name__ == '__main__':#测试用
    loop = asyncio.get_event_loop()
    task = loop.create_task(get_pic(["白丝"]))
    loop.run_until_complete(task)
    loop.close()
    print(task.result())
