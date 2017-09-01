# -*- coding: utf-8 -*-

import hashlib
import unittest

import re

import requests
from bs4 import BeautifulSoup

from livedotdanmu import bilibili, matcher, douban
from livedotdanmu.model.play import Play


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # r = requests.get('https://api.acplay.net/api/v1/related/313990001', headers={'Accept':'application/json', 'User-Agent':'DanDanPlayForMac/2.2 (Mac OS X ban ben 10.12.6(ban hao 16G29))', 'Host':'api.acplay.net'})
        # r = requests.get(
        #     'http://cmts.iqiyi.com/bullet/84/00/733048400_300_1.z?rn=0.7411899881422457&business=danmu&is_iqiyi=true&is_video_page=true&tvid=733048400&albumid=733048400&categoryid=1&qypid=01010021010000000000',
        #     headers={'Accept-Encoding':'gzip, deflate',
        #              'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        #
        # )
        # print(r.content)
        # print(str(r.content, 'latin-1'))

        # print(str(r.content, 'latin-1'))
        # f = open('/Users/lyons/Downloads/733048400_300_1.z', mode='rb')


        # content = zlib.decompress(r.raw, -zlib.MAX_WBITS)
        # elif content_encode == 'deflate':
        # content = zlib.decompress(f.read()., -zlib.MAX_WBITS)

        # decompressed_data = zlib.decompress(f.read(), -zlib.MAX_WBITS)
        # f.close()

        # return inflated
        # return content
        # print(content)
        # print(qq.get_vid('https://v.qq.com/x/cover/71bctb897dwx46m.html'))
        # print(qq.get_danmu('1992564676', 3000))

        # file = open('/Users/lyons/doc/sample-danmu-qq.json', 'r')
        # print(qq.format_danmu(file.read()))
        # file.close()
        # print(bilibili.search_episode(Play(name='陨落星辰', season=1, episode=10)))
        # print("123123 {}".format(1))
        # result = re.compile('E0(\d+?)').match('S01')
        # print(result)
        # print(matcher.extract_season("权力的游戏第七季第五集"))
        # print(matcher.extract_episode("权力的游戏第七季第五集"))

        # print(matcher.extract_season("权力SSS的游EEE戏S3E06SSEE"))
        # print(matcher.extract_episode("权力SSS的游EEE戏S3E06SSEE"))
        #
        # print(matcher.extract_season("SSS06权力EE的游戏S01E2SESE"))
        # print(matcher.extract_episode("SSE权力的游戏S01E2EESSS"))
        #
        # print(matcher.extract_season("权力的游戏S10E20SSS"))
        # print(matcher.extract_episode("权力的游戏S10E20E"))

        # print(douban.get_type('权力的游戏'))
        # params = {
        #     'cid':3505577,
        #     'otype':'json',
        #     'type':'',
        #     'quality':0,
        #     'qn':0,
        # }
        #
        # print(GetSign(params, 'f3bb208b3d081dc8', AppSecret='1c15888dc316e05a15fdd0a02ed6584f'))

        bilibili.get_danmu_for_diff_sound_track_and_parted(BeautifulSoup(requests.get("https://www.bilibili.com/video/av2300622/").text, 'lxml'))

if __name__ == '__main__':
    unittest.main()


def GetSign(params, appkey, AppSecret=None):
    """
    获取新版API的签名，不然会返回-3错误
待添加：【重要！】
    需要做URL编码并保证字母都是大写，如 %2F

    cid = 3505577 & appkey = 84956560
    bc028eb7 & otype = json & type = & quality = 0 & qn = 0 & sign = c06528d8bae2a511054aab27faf1883a
"""
    # params['appkey']=appkey
    # data = ""
    # paras = params.keys()
    # sorted(paras)
    # for para in paras:
    #     if data != "":
    #         data += "&"
    #     data += para + "=" + str(params[para])
    # if AppSecret == None:
    #     return data
    # m = hashlib.md5()
    # m.update('cid=${cid}&from=miniplay&player=1&quality=2&type=mp4')
    #
    # m.update(data.encode('utf-8')+AppSecret.encode('utf-8'))
    return hashlib.md5("cid=3505577&from=miniplay&player=1&quality=2&type=mp41c15888dc316e05a15fdd0a02ed6584f".encode('utf-8')).hexdigest()
