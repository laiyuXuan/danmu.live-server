# -*- coding: utf-8 -*-
import re
import uuid

import requests
from bs4 import BeautifulSoup

from livedotdanmu import bilibili, qq, app, douban, redis, const
from livedotdanmu.model.play import Play
from livedotdanmu.utils import strings, files


def match(play:Play):
    danmu = search_danmu(play)
    if danmu is None:
        return None
    danmuId = uuid.uuid4().hex
    print('danmuId {} for {}({})'.format(danmuId, play.name, play.year))
    files.write_json_file(app.config['DANMU_FILE_PATH'] + danmuId, danmu)
    redis.set(const.PREFIX_MOVIVE_NAME_2_DANMU.format(play.name), danmuId)
    if not play.year is None:
        redis.set(const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU.format(play.name, play.year), danmuId)
    return danmuId


def search_danmu(play: Play):
    danmu = bilibili.match(play)
    if not danmu is None:
        print('a danmu is found with bilibili')
        return danmu
    danmu = qq.match(play)
    if not danmu is None:
        print('a danmu is found with qq')
        return danmu
    print("reach a todo block...")
    return None


def parse_play_by_name(filename):
    play = parse_with_own_method(filename)
    if not play is None:
        return play
    # guessed = guessit(filename)
    # if not guessed is None:
    #     return Play(name=guessed['title'])
    matched = query_acplay(filename)
    if not matched is None:
        splits = str.split(matched['animetitle'], "(")
        year = splits[1].split(",")[1].remove(")") if splits.__len__() == 2 and splits[1].split(
            ",").__len__() == 2 else None
        return Play(name=splits[0], type=1 if matched['type'] == 1 else 0, year=year)
    return None


def query_acplay(filename):
    headers = {'ACCEPT': 'text/xml'}
    r = requests.get(app.config['ACPLAY_API_URL'] + filename, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    matches = soup.findAll('match')
    if matches.__len__() == 0:
        return None
    return matches[0]


def parse_with_own_method(filename):
    zh = strings.extract_zh(filename)
    if zh is None:
        return None
    file = open('static/movie_stop_words')
    stopWords = file.read()
    stopWordList = stopWords.split("\n")
    for stopWord in stopWordList:
        zh = zh.replace(stopWord, '')
    season = extract_season(filename)
    episode = extract_episode(filename)
    type = douban.get_type(zh)
    return Play(name=zh, season=season, episode=episode, type=type)


def extract_season(filename):
    result = re.compile('.*第(.+?)季').findall(filename)
    if result.__len__() > 0:
        return strings.any_to_arabic(result[0])

    result = re.compile('.*S0(\d+?)').findall(filename)
    if result.__len__() > 0:
        return int(result[0])

    result = re.compile('.*S1(\d+?)').findall(filename)
    if result.__len__() > 0:
        return int('1' + result[0])

    result = re.compile('.*S(\d+?)').findall(filename)
    if result.__len__() > 0:
        return int(result[0])
    print('failed to extract season from {}'.format(filename))


def extract_episode(filename):
    result = re.compile('.*第(.+?)集').findall(filename)
    if result.__len__() > 0:
        return strings.any_to_arabic(result[0])
    result = re.compile('.*E(\d+?)(\d+?)').findall(filename)
    if result.__len__() > 0 and result[0].__len__() == 2:
        return int(result[0][0] + result[0][1])
    result = re.compile('.*E(\d+?)').findall(filename)
    if result.__len__() > 0:
        return int(result[0])

    print('failed to extract episode from {}'.format(filename))