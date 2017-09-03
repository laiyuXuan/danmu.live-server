import re
from random import randint

import requests
import zlib
from bs4 import BeautifulSoup

from livedotdanmu import const, app
from livedotdanmu.model.play import Play
from livedotdanmu.utils import strings


def try_get_first_of_series(soup:BeautifulSoup, play:Play):
    results = soup.find_all(class_='result_info result_info-180236 result-info-movie ')
    if results.__len__() == 0:
        return soup
    name = play.name +  '1'
    r = requests.get(app.config['IQIYI_SEARCH_MOVIE_URL'].format(name + ' ' + str(play.year) if not play.year is None else name))
    if r.status_code != 200:
        return soup
    newSoup = BeautifulSoup(r.text, 'lxml')
    if newSoup.find_all(class_='result_info result_info-180236 ').__len__() == 0:
        return soup
    return newSoup


def search_movie(play: Play):
    searchUrl = app.config['IQIYI_SEARCH_MOVIE_URL'].format(play.name + ' ' + str(play.year) if not play.year is None else play.name)
    print('search {} on iqiyi {}'.format(play.name, searchUrl))
    r = requests.get(searchUrl)
    if r.status_code != 200:
        print('failed to search {} on iqiyi, {}'.format(play.name, r.status_code))
        return None
    soup = BeautifulSoup(r.text, 'lxml')
    soup = try_get_first_of_series(soup, play)
    results = soup.find_all(class_='result_info result_info-180236 ')
    if results.__len__() == 0:
        print('no {} found on iqiyi'.format(play.name))
        return None
    matched = list(filter(lambda r: r.find_all(class_='icon_placeSource icon_iqiyi').__len__() > 0
                                    and r.find_all(class_='info_play_btn').__len__() > 0
                                    and strings.remove_punctuation(
        r.find_all(class_='result_title')[0].find_all('a')[0]['title']).__contains__(play.name),
                          results))
    if matched.__len__() == 0:
        print('no playable source for {} found on iqiyi'.format(play.name))
        return None
    playUrl = matched[0].find_all(class_='info_play_btn')[0]['href']
    r = requests.get(playUrl)
    if r.status_code != 200:
        print('failed to open play url {} for {}'.format(playUrl, play.name))
        return None
    tvId = re.compile('tvId:(.+?),').findall(r.text)[0]
    albumId = re.compile('albumId:(.+?),').findall(r.text)[0]
    categoryId = re.compile('cid:(.+?),').findall(r.text)[0]
    return tvId, 1, albumId, categoryId


def search_episode(play):
    # return tvId, paragraph, albumId, categoryId
    return None


def get_danmu(tvId, paragraph, albumId, categoryId):
    t = '0000' + tvId
    first = t[t.__len__() - 4: t.__len__() - 2]
    second = t[t.__len__() - 2:]
    rn = '0.' + str(random_with_N_digits(16))
    url = app.config['IQIYI_GET_DANMU_URL'].format(first, second, tvId, paragraph, rn, tvId, albumId, categoryId)
    print('danmu url {}'.format(url))
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print('failed to get danmu from iqiyi {}'.format(url))
    return zlib.decompressobj().decompress(bytearray(r.raw.data))


def format_danmu(raw_danmu, play: Play):
    soup = BeautifulSoup(raw_danmu, 'lxml')
    danmus = []
    danmuTags = soup.find_all('bulletinfo')
    for tag in danmuTags:
        time = tag.find_all('showtime')[0].text
        text = tag.find_all('content')[0].text
        color = '#' + tag.find_all('color')[0].text.lower()
        type = 'right' if tag.find_all('position')[0].text == '0' else 'top'
        one_danmu = {
            'author': 'iota',
            'time': time,
            'text': text,
            'color': color,
            'type': type
        }
        danmus.append(one_danmu)

    result = {
        'code': 1,
        'danmaku': danmus
    }
    print('found a danmu for {} ({}) on iqiyi'.format(play.name, play.year))
    return result


def match(play: Play):
    if play.type == const.MOVIE:
        tvId, paragraph, albumId, categoryId = search_movie(play)
    elif play.type == const.EPISODE:
        tvId, paragraph, albumId, categoryId = search_episode(play)
    else:
        print('reach a todo block')
        return None
    if tvId is None or albumId is None or categoryId is None:
        return None
    raw_danmu = get_danmu(tvId, paragraph, albumId, categoryId)
    if raw_danmu is None:
        return None
    return format_danmu(raw_danmu, play)


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)
