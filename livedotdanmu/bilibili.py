import re

import requests
from bs4 import BeautifulSoup

from livedotdanmu import const, app
from livedotdanmu.model.play import Play
from livedotdanmu.utils import strings


def match(play: Play):
    if play.type == const.MOVIE:
        cid = search_movie(play.name)
    elif play.type == const.EPISODE:
        cid = search_episode(play)
    else:
        print('reach a todo block')
        cid = None
    if cid is None:
        return None
    r = requests.get(str.format(app.config['BILIBILI_DANMU_URL'], cid))
    return format_danmu(r.text)


def search_movie(keyword):
    link = try_pgc_search(keyword)
    if not link is None:
        print('found a url for movie %s : %s' % (keyword, link))
        return get_cid(link)
    link = try_movie_search(keyword)
    if not link is None:
        print('found a url for movie %s : %s' % (keyword, link))
        return get_cid(link)
    return None


def search_episode(play: Play):
    result = search_ended_episode(play, app.config['BILIBILI_SEARCH_URL_EPISODE_ENDED'])
    if not result is None:
        return get_episode_cid(result, play)
    result = search_ended_episode(play, app.config['BILIBILI_SEARCH_URL_EPISODE_SHOWING'])
    if not result is None:
        return get_episode_cid(result, play)
    return None


def search_ended_episode(play: Play, searchUrl):
    seasonZH = strings.build_season_zh(play)
    r = requests.get(str.format(searchUrl, play.name + seasonZH))
    if r.status_code != 200:
        print('bad request when searching episode on bilibili :%s' % (r.text))
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    video_matrix = soup.select(".video.matrix")
    if video_matrix is None or video_matrix.__len__() == 0:
        print('no matched when searching episode on bilibili for play %s' % (play.name + seasonZH))
        return None
    for video in video_matrix:
        title: str = video.find_all('a')[0]['title']
        if title.__contains__(play.name) and title.__contains__(seasonZH):
            return 'http:' + video.find_all('a')[0]['href']
    print('no matched when searching episode on bilibili for play %s' % (play.name + seasonZH))
    return None


def get_episode_cid(url, play:Play):
    r = requests.get(url)
    if r.status_code != 200:
        print('bad request when getting episode cid on bilibili %s' %(url))
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    options = soup.select('div.player-wrapper')[0].find_all('option')
    # TODO save other episodes' danmu to db
    print('found a cid on bilibili for {} {} {}'.format(play.name, play.season, play.episode))
    return options[play.episode - 1]['cid']


def try_pgc_search(keyword):
    r = requests.get(app.config['BILIBILI_SEARCH_URL_PGC'] + keyword)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text, "lxml")
    movie_item = soup.select(".movie-item")
    if movie_item.__len__() == 0:
        return
    return soup.select(".movie-item .left-img")[0]["href"]


def get_cid(link):
    try:
        url = "https:" + link
        print(url)
        r = requests.get(
            url,
            headers=fake_headers())
        if r.status_code != 200:
            return
        pattern = "cid\=\"(.+?)\""
        pattern1 = "cid\=(.+?)&"
        cid = re.findall(pattern, r.text, False)
        if cid.__len__() != 0:
            return cid[0]
        return re.findall(pattern1, r.text, False)[0]
    except requests.exceptions.ConnectionError:
        print("something went wrong...")
        return None


def try_movie_search(keyword):
    r = requests.get(app.config['BILIBILI_SEARCH_URL_MOVIE'] + keyword)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text, "lxml")
    video_matrix = soup.select(".video.matrix")
    if video_matrix.__len__() == 0:
        return
    return video_matrix[0].select(".title")[0]["href"]


def format_danmu(response):
    danmus = []
    soup = BeautifulSoup(response, 'lxml')
    danmuTags = soup.findAll('d')
    if danmuTags.__len__() == 0:
        return
    for danmu in danmuTags:
        text = danmu.contents[0] if danmu.contents.__len__() > 0 else ''
        infos = str.split(danmu['p'], ',')
        if infos[1] == '4':
            type = 'bottom'
        elif infos[1] == '5':
            type = 'top'
        else:
            type = 'right'
        one_danmu = {
            'author': 'Bilibili',
            'time': infos[0],
            'text': text,
            'color': '#' + hex(int(infos[3])).replace('0x', ''),
            'type': type
        }
        danmus.append(one_danmu)

    result = {
        'code': 1,
        'danmaku': danmus
    }
    # print('parsed result :' + result)
    return result


def get_danmu_by_cid(id):
    r = requests.get(str.format(app.config['BILIBILI_DANMU_URL'], id))
    return format_danmu(r.text)


def fake_headers():
    return {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'bangumi.bilibili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
