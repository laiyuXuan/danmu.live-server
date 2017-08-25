# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from server import bilibili, qq, app
from server.model.play import Play
from server.utils import strings



def match_danmu(play: Play):
    danmu = bilibili.match(play)
    if not danmu is None:
        print('a danmu if found with bilibili')
        return danmu
    danmu = qq.match(play)
    if not danmu is None:
        print('a danmu if found with qq')
        return danmu
    print("reach a todo block...")
    return None


def parse_movie_name(filename):
    parsed = parse_with_own_method(filename)
    if not parsed is None:
        return Play(name=parsed)
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
    return zh
