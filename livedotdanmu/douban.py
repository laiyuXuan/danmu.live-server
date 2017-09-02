import json

import os
import random

import requests
import time

from livedotdanmu import app, const, matcher, redis
from livedotdanmu.model.play import Play
from livedotdanmu.utils import https

RANK_TOP_URL = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start=0&limit=100'


def get_type(name):
    result = do_search(name)
    if result is None:
        return
    type = result['subjects'][0]['subtype']
    if type == 'movie':
        return const.MOVIE
    elif type == 'tv':
        return const.EPISODE


def do_search(name):
    url: str = app.config['DOUBAN_SEARCH_MOVICE_URL']
    r = requests.get(url.format(name), headers=https.fake_headers('api.douban.com'))
    if r.status_code != 200:
        print('failed to search with douban api {}'.format(url))
        return None
    result = json.loads(r.text)
    if int(result['total']) == 0:
        print('no matched on douban for {}'.format(name))
        return None
    return result


def crawl_rank_top(type, start):
    r = requests.get(RANK_TOP_URL.format(type))
    if r.status_code != 200:
        print('request failed, {}'.format(r.text))
        return None
    results: [dict] = json.loads(r.text)
    for idx, result in enumerate(results[start:]):
        title = result['title']
        year = str.split(result['release_date'], '-')[0]
        danmuId = redis.get(const.PREFIX_MOVIVE_NAME_2_DANMU.format(title))
        if danmuId is None:
            danmuId = redis.get(const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU.format(title, year))
        if not danmuId is None:
            print('danmu {} existed for {} ({})'.format(danmuId, title, year))
            continue
        danmuId = matcher.match(Play(name=title, year=year, type=const.MOVIE))
        print('danmu for {} ({}) obtained, {}'.format(title, year, danmuId))
        print('current idx {}'.format(start + idx))
        time.sleep(random.randint(2, 4) * 2)
    print('ALL DONE.')