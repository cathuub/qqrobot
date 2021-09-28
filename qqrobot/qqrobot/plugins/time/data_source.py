
import pytz
import datetime


country_timezone={
    "中国":'Asia/Shanghai',
    "加拿大": 'America/Vancouver',
}

def gettime(country):
    # 选择时区，生成一个时区对象

    zone=country_timezone.get(country)
    if (None==zone):
        return "你要查找的世界时间暂时没有收录在档案中·····"
    city=zone.rindex('/')
    city=zone[city + 1:]
    tz = pytz.timezone(zone)
    time = datetime.datetime.now(tz)
    if time.strftime("%p") == "AM":  # 上午
        time = datetime.datetime.now(tz).strftime("%Y年%m月%d号 上午%I点%M分%S")+f"——来自{city}"
    elif time.strftime("%p") == "PM":  # 下午
        time = datetime.datetime.now(tz).strftime("%Y年%m月%d号 下午%I点%M分%S")+f"——来自{city}"
    return time

if __name__ == '__main__':
    print(gettime("a"))


