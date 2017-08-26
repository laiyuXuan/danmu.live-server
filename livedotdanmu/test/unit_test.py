import unittest

from livedotdanmu import bilibili
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
        print(bilibili.search_episode(Play(name='陨落星辰', season=3, episode=1)))
        # print("123123 {}".format(1))

if __name__ == '__main__':
    unittest.main()
