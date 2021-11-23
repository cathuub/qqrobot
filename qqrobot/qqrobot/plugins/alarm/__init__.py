import random
import datetime

import nonebot
import pytz
from nonebot import require
from nonebot.adapters.cqhttp.message import Message

scheduler = require("nonebot_plugin_apscheduler").scheduler

# 人性化词语
mid_word = [
    "是时候",
    "早该",
    "应该和高性能机器人一样",
]
country_point = {
    'Asia/Shanghai': "中国",
    'America/Vancouver': "加拿大"
}


# 睡觉函数
async def goto_sleep(country):
    tz = pytz.timezone(country)
    time_now = datetime.datetime.now(tz)
    sleep_cq = '[CQ:image,file=sleep.JPG]'
    str = country_point.get(country) + "已经" + time_now.strftime("%H点%M分") + "了哦," + mid_word[
        random.randint(0, mid_word.__len__() - 1)] + "睡觉了" + sleep_cq

    sleep_message = Message(str)

    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id='这里输入需要提醒的群号', message=sleep_message)


# 吃饭函数
async def goto_eat(country):
    tz = pytz.timezone(country)
    time_now = datetime.datetime.now(tz)
    eat_cq = '[CQ:image,file=eat.JPG]'

    str = country_point.get(country) + "已经" + time_now.strftime("%H点%M分") + "了哦," + mid_word[
        random.randint(0, mid_word.__len__() - 1)] + "吃饭了" + eat_cq

    eat_message = Message(str)

    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=869386880, message=eat_message)


# 起床函数
async def goto_stduy(country):
    tz = pytz.timezone(country)
    time_now = datetime.datetime.now(tz)
    stduy_cq = '[CQ:image,file=eat.JPG]'

    str = country_point.get(country) + "已经" + time_now.strftime("%H点%M分") + "了哦,是时候起床了了" + stduy_cq

    weakup_message = Message(str)
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=869386880, message=weakup_message)



scheduler.add_job(goto_sleep, 'cron', day_of_week='0-6', hour='23',timezone='America/Vancouver', args=['America/Vancouver'])
scheduler.add_job(goto_eat, 'cron', day_of_week='0-6', hour='8,12,18', timezone='America/Vancouver', args=['America/Vancouver'])
scheduler.add_job(goto_stduy, 'cron', day_of_week='0-6', hour='7', timezone='America/Vancouver', args=['America/Vancouver'])


scheduler.add_job(goto_sleep, 'cron', day_of_week='0-6', hour='23', timezone= 'Asia/Shanghai', args=['Asia/Shanghai'])
scheduler.add_job(goto_eat, 'cron', day_of_week='0-6', hour='8,12,18', timezone= 'Asia/Shanghai', args=['Asia/Shanghai'])
scheduler.add_job(goto_stduy, 'cron', day_of_week='0-6', hour='7', timezone= 'Asia/Shanghai', args=['Asia/Shanghai'])
