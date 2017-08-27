import json

import requests

from livedotdanmu import app, const
from livedotdanmu.utils import https


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