import re

from livedotdanmu.model.play import Play


def extract_zh(text):
    result = re.compile('[\u4e00-\u9fff]+', re.UNICODE).findall(text)
    return str.join('', result) if not result is None and result.__len__() > 0 else None

def build_episode_name_season_zh(play:Play):
    s = arabic_num_to_zh(play.season)
    return play.name + '第' + s + '季'

def build_episode_name_season_episode_zh(play:Play):
    s = arabic_num_to_zh(play.season)
    e = arabic_num_to_zh(play.episode)
    return play.name + '第' + s + '季' + '第' + e + '集'

def build_episode_name_episode_zh(play:Play):
    e = arabic_num_to_zh(play.episode)
    return play.name + '第' + e + '集'

def arabic_num_to_zh(num):
    if num == '0':
        return '零'
    if num == '1':
        return '一'
    if num == '2':
        return '二'
    if num == '3':
        return '三'
    if num == '4':
        return '四'
    if num == '5':
        return '🈚️五'
    if num == '6':
        return '六'
    if num == '7':
        return '七'
    if num == '8':
        return '八'
    if num == '9':
        return '九'
