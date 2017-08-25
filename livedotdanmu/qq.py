import json

import requests
from bs4 import BeautifulSoup

from livedotdanmu import const
from livedotdanmu.model.play import Play

URLS = {
    'GET_DANMU_ID': 'https://bullet.video.qq.com/fcgi-bin/target/regist?otype=json&cid={0}&lid=&g_tk=&vid={1}',
    'GET_DANMU': 'https://mfm.video.qq.com/danmu?otype=json&target_id={0}&count={1}',
    'SEARCH': 'https://v.qq.com/x/search/?q={0}&stag=7&smartbox_ab='
}
COUNT = 3000


def match(play: Play):
    if play.type == const.MOVIE:
        url = search_by_name(play)
        if url is None or url == '':
            print('failed to find url of %s with v.qq.com' % (play.name))
            return None
        danmuId = get_danmu_id(url)
        if danmuId is None or danmuId == '':
            print('failed to find danmuId of %s with v.qq.com url %s' % (play.name, url))
            return None
        danmu = get_danmu(danmuId, COUNT)
        return danmu

    elif play.type == const.EPISODE:
        print('reach a todo block')
        pass
    else:
        print('reach a todo block')
        pass


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


def get_danmu_id(url: str):
    splits = url.split('/')
    vid = splits[splits.__len__() - 1].split('.')[0]
    cid = splits[splits.__len__() - 2]
    print('vid: %s, cid: %s' % (vid, cid))
    r = requests.get(str.format(URLS['GET_DANMU_ID'], cid, vid))
    if r.status_code != 200:
        return None
    content = r.text.replace(';', '')
    splits = content.split('{')[1]
    return json.loads('{' + splits)['targetid']


def format_danmu(raw):
    danmus = []
    loaded = json.loads(raw)
    for comment in loaded['comments']:
        style = json.loads(comment['content_style']) if comment['content_style'] != '' else None
        danmu = {
            'author': comment['opername'],
            'time': comment['timepoint'],
            'text': comment['content'],
            'color': '#' + style['color'] if not style is None and 'color' in style else 'ffffff',
            'type': 'right'
        }
        danmus.append(danmu)
    result = {
        'code': 1,
        'danmaku': danmus
    }
    return result


def get_danmu(danmuid, count):
    r = requests.get(str.format(URLS['GET_DANMU'], danmuid, count))
    if r.status_code != 200:
        return None
    return format_danmu(r.text)


def search_by_name(play: Play):
    if play.type == const.MOVIE:
        r = requests.get(str.format(URLS['SEARCH'], play.name))
        soup = BeautifulSoup(r.text, 'lxml')
        matched = soup.find_all(class_='result_item_v')

        if matched is None or matched.__len__() == 0:
            return None
        matched = filter(lambda m: m.find_all(class_='icon_source icon_source_tencentvideo').__len__() > 0,
                         matched).__next__()
        if matched is None or matched.__len__() == 0:
            print('not found with tencent source for :%s' % (play.name))
            return None
        return matched.find_all(class_='btn_primary')[0]['href']
    elif play.type == const.EPISODE:
        pass
    else:
        pass
