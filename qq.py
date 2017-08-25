import requests
import json
from bs4 import BeautifulSoup

GET_DANMU_ID = 'https://bullet.video.qq.com/fcgi-bin/target/regist?otype=json&cid={0}&lid=&g_tk=&vid={1}'
GET_DANMU = 'https://mfm.video.qq.com/danmu?otype=json&target_id={0}&count={1}'

def get_true_play_url(url):
    r = requests.get(url)
    print(r.text)
    soup = BeautifulSoup(r.text, 'html')
    tags = soup.findAll('link')

    if tags is None or tags.__len__() == 0:
        return None
    for tag in tags:
        if tag['rel'] and tag['rel'][0] == 'canonical':
            return tag['href']

def get_danmu_id(url:str):
    splits = url.split('/')
    vid = splits[splits.__len__() - 1].split('.')[0]
    cid = splits[splits.__len__() - 2]
    print('vid: %s, cid: %s' %(vid, cid))
    r = requests.get(str.format(GET_DANMU_ID, cid, vid))
    if r.status_code != 200:
        return None
    content = r.text.replace(';', '')
    splits = content.split('{')[1]
    return json.loads('{' + splits)['targetid']

def get_danmu(danmuid, count):
    r = requests.get(str.format(GET_DANMU, danmuid, count))
    return r.text