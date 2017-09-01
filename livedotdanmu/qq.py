import json

import requests
from bs4 import BeautifulSoup, Tag

from livedotdanmu import const, app
from livedotdanmu.model.play import Play
from livedotdanmu.utils import strings

COUNT = 9999


def match(play: Play):
    if play.type == const.MOVIE:
        url = search_movie_by_name(play)
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
        url = search_episode_by_name(play)
        if url is None or url == '':
            print('failed to find url of %s with v.qq.com' % (play.name + '第' + play.season + '季'))
            return None
        danmuId = get_danmu_id(url)
        if danmuId is None or danmuId == '':
            print('failed to find danmuId of %s with v.qq.com url %s' % (play.name + '第' + play.season + '季', url))
            return None
        danmu = get_danmu(danmuId, COUNT)
        return danmu
    else:
        print('an unexpected branch is reached at qq.match()...')
        return None


def search_episode_by_name(play: Play):
    name = play.name
    if not play.season is None:
        name = play.name + '第' + strings.arabic_num_to_zh(play.season) + '季'
    matched: Tag = get_matched_video_div(name)
    if matched is None:
        return None
    episodeDiv = matched.find_all(class_='result_episode_list cf')
    if episodeDiv is None:
        return None
    episodes = episodeDiv[0].find_all(class_='item')
    if episodes is None:
        return None
    # TODO: save other episodes' danmu to db
    return episodes[play.episode - 1].find_all('a')[0]['href']


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
    r = requests.get(app.config['QQ_GET_DANMU_ID_URL'].format(cid, vid))
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
    r = requests.get(app.config['QQ_GET_DANMU_URL'].format(danmuid, count))
    if r.status_code != 200:
        return None
    return format_danmu(r.text)


def search_movie_by_name(play: Play):
    matched = get_matched_video_div(play.name)
    if matched is None:
        return None
    return matched.find_all(class_='btn_primary')[0]['href']


def get_matched_video_div(name):
    r = requests.get(app.config['QQ_SEARCH_URL'].format(name))
    soup = BeautifulSoup(r.text, 'lxml')
    matched = soup.find_all(class_='result_item_v')

    if matched.__len__() == 0:
        return None
    matched = filter(lambda m: m.find_all(class_='icon_source icon_source_tencentvideo').__len__() > 0,
                     matched).__next__()
    if matched is None or matched.__len__() == 0:
        print('not found with tencent source for :%s' % (name))
        return None
    return matched
