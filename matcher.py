# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

import bilibili
import qq
from model.play import Play
from utils import strings

ACPLAY_API_URL = "http://acplay.net/api/v1/match?hash=0&length=5&duration=0&fileName="
BILIBILI_DANMU_URL = "http://comment.bilibili.com/{0}.xml"


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
    matched =query_acplay(filename)
    if not matched is None:
        splits = str.split(matched['animetitle'], "(")
        year = splits[1].split(",")[1].remove(")") if splits.__len__() == 2 and splits[1].split(
            ",").__len__() == 2 else None
        return Play(name=splits[0], type=1 if matched['type'] == 1 else 0, year=year)
    return None


def query_acplay(filename):
    headers = {'ACCEPT': 'text/xml'}
    r = requests.get(ACPLAY_API_URL + filename, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    matches = soup.findAll('match')
    if matches.__len__() == 0:
        return None
    return matches[0]


def parse_with_own_method(filename):
    zh = strings.extract_zh(filename)
    if zh is None:
        return None
    file = open('movie_stop_words')
    stopWords = file.read()
    stopWordList = stopWords.split("\n")
    for stopWord in stopWordList:
        zh = zh.replace(stopWord, '')
    return zh
