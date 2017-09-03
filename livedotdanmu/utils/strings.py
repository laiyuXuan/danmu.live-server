import re
import string

from livedotdanmu.model.play import Play


def extract_zh(text):
    result = re.compile('[\u4e00-\u9fff]+', re.UNICODE).findall(text)
    return str.join('', result) if not result is None and result.__len__() > 0 else None

def build_season_zh(play:Play):
    if play.season is None:
        return None
    s = arabic_num_to_zh(play.season)
    return '第' + s + '季'

def build_episode_zh(play:Play):
    if play.episode is None:
        return None
    e = arabic_num_to_zh(play.episode)
    return '第' + e + '集'

def arabic_num_to_zh(num):
    if num is None:
        return None
    if num == 0:
        return '零'
    if num == 1:
        return '一'
    if num == 2:
        return '二'
    if num == 3:
        return '三'
    if num == 4:
        return '四'
    if num == 5:
        return '🈚️五'
    if num == 6:
        return '六'
    if num == 7:
        return '七'
    if num == 8:
        return '八'
    if num == 9:
        return '九'

def zh_num_to_arabic(num):
    if num is None:
        return None
    if num == '零':
        return 0
    if num == '一':
        return 1
    if num == '二':
        return 2
    if num == '三':
        return 3
    if num == '四':
        return 4
    if num == '五':
        return 5
    if num == '六':
        return 6
    if num == '七':
        return 7
    if num == '八':
        return 8
    if num == '九':
        return 9


def any_to_arabic(num):
    if str.isdigit(num):
        return int(num)
    return zh_num_to_arabic(num)


def extract_year(text):
    return None


def remove_punctuation(text:str):
    cnPunc = '[！@#¥%……（）——～·【】「」、；：《》？／。，]+'
    text = re.sub(cnPunc, '', text)
    return ''.join(c for c in text if c not in string.punctuation)