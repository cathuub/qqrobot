"""
网易云搜索主要脚本
暂时支持 歌搜索，歌手单曲推荐(基于搜索)，随机推荐
"""
import asyncio
import random

import httpx
from nonebot.adapters.cqhttp import MessageSegment

from rsacode import createSecretKey
from rsacode import aesEncrypt
from rsacode import rsaEncrypt
import json


headers = {#使用Referer假装从网易云网站本身发送的请求
    'Referer': 'http://music.163.com',
}

#这个不知道是什么东西 跟着抄过来
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'

#将json进行第一次aes加密的时候用这个作为密钥
nonce = '0CoJUm6Qyw8W8jud'

# rsa加密的公钥
pubKey = '010001'

#加密函数
def code(datajson) :#加密函数
    #获得一个16位的随机字符串
    secKey = createSecretKey(16)

    #两次AES加密
    encText = aesEncrypt(datajson, nonce) #把传入的的json数据使用nonce进行第一次aes加密
    encText = aesEncrypt(encText, secKey)#使用随机的十六位字符串作为密钥把上面的到的结果进行第二次加密

    #RSA加密
    encSecKey = rsaEncrypt(secKey, pubKey, modulus) #把我们用作ARS加密的密钥进行ras加密
    #由于我们这里使用的一直是使用十六个F作为密钥所以这个对于我们来说是不变的，所以只要加密一遍以后直接复制出来搞成一个常量就行，每次提交给服务器都一样

    data = {#载入数据
        'params': str(encText),
        'encSecKey': encSecKey
    }
    return data#将加密好的data返回


#歌曲搜索,这个是搜索接口，不按id,返回歌曲搜索的函数
async def get_song(mes):
    #注意，目前由于网易云搜索中将会存在下架歌曲，因此可能会无法播放
    #注意，冷门歌曲可能会没有20个搜索项，可以先20之后获取到playlist中的长度单位再随机
    data = {
        's': mes,
        'offset': 0,  # 第几页
        'limit': 20,  # 一页有多少首歌
        'type': "1",  # 类型为歌曲
    }
    # 将字典dump成一个json字符串
    datajson = json.dumps(data)
    # 加密
    data = code(datajson)
    # 发送post请求，req就是结果
    async with httpx.AsyncClient() as client:
        req = await client.post(
            f"http://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
            data=data,
            headers=headers,
        )
    req_json = req.json()
    songs_id=[]
    for song in req_json['result']['songs']:
        songs_id.append(song['id'])
    return songs_id
    # if (req_json['result']['songCount'] == 0):  # 如果搜索结果为空就会走这个分支
    #     return "你找的歌连网易云都没有呢···"

#歌手搜索
async def get_songer(mes):
    data = {
        's': mes,
        'offset': 1,  # 第几页
        'limit': "3",  # 一页有多少种类，取三，不然在冷门情况下可能会有杂牌歌单混入
        'type': "100",  # 类型为歌手
    }

    # 将字典dump成一个json字符串
    datajson = json.dumps(data)
    # 加密
    data = code(datajson)
    # 发送post请求，req就是结果
    async with httpx.AsyncClient() as client:
        req = await client.post(
            f"http://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
            data=data,
            headers=headers,
        )
    req_json=req.json()
    singer_lists = []
    for list in req_json['result']['singer']:
        singer_lists.append(list['id'])
    return singer_lists


#歌单搜索
async def get_songlist(mes):
    data = {
        's': mes,
        'offset': 1,  # 第几页
        'limit': "3",  # 一页有多少种类，取三，不然在冷门情况下可能会有杂牌歌单混入
        'type': "1000",  # 类型为歌单
    }

    # 将字典dump成一个json字符串
    datajson = json.dumps(data)
    # 加密
    data = code(datajson)
    # 发送post请求，req就是结果
    async with httpx.AsyncClient() as client:
        req = await client.post(
            f"http://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
            data=data,
            headers=headers,
        )
    req_json=req.json()
    songs_lists = []
    for list in req_json['result']['playlists']:
        songs_lists.append(list['id'])
    return songs_lists

#歌单中歌曲获取其
async def get_playlist_detail(playlist_id):
    data = {
        'id': playlist_id
    }
    # 将字典dump成一个json字符串
    datajson = json.dumps(data)
    # 加密
    data = code(datajson)
    # 发送post请求，req就是结果
    async with httpx.AsyncClient() as client:
        req = await client.post(
            f"https://music.163.com/weapi/v6/playlist/detail",
            data=data,
            headers=headers,
        )
    req_json = req.json()
    list_songs = []
    for song in req_json['playlist']['trackIds']:
        list_songs.append(song['id'])
    return list_songs

if __name__ == '__main__':#测试用

    loop = asyncio.get_event_loop()
    task = loop.create_task(get_playlist_detail("1444208"))
    loop.run_until_complete(task)
    loop.close()
    print(task.result())

