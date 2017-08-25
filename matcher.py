# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from guessit import guessit
from bili import Bilibili
from model.play import Play
from utils import strings

ACPLAY_API_URL = "http://acplay.net/api/v1/match?hash=0&length=5&duration=0&fileName="
BILIBILI_DANMU_URL = "http://comment.bilibili.com/{0}.xml"


class Matcher():
    def match_danmu(self, play:Play):
        if play.type == 1:
            print("reach a todo block...")
            pass
        else:
            cid = Bilibili().search_movie(play.name)
            if not cid is None:
                print('one cid found: %s' % (cid))
                return BILIBILI_DANMU_URL.format(cid)
            else:
                print("reach a todo block...")
                return None


    def parse_movie_name(self, filename):
        parsed = self.parse_with_own_method(filename)
        if not parsed is None:
            return Play(name=parsed)
        # guessed = guessit(filename)
        # if not guessed is None:
        #     return Play(name=guessed['title'])
        matched = self.query_acplay(filename)
        if not matched is None:
            splits = str.split(matched['animetitle'], "(")
            year = splits[1].split(",")[1].remove(")") if  splits.__len__() == 2 and splits[1].split(",").__len__() == 2 else None
            return Play(name=splits[0], type=1 if matched['type'] == 1 else 0, year=year)
        return None



    def query_acplay(self, filename):
        headers = {'ACCEPT': 'text/xml'}
        r = requests.get(ACPLAY_API_URL + filename, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        matches = soup.findAll('match')
        if matches.__len__() == 0:
            return None
        return matches[0]

    def parse_with_own_method(self, filename):
        zh = strings.extract_zh(filename)
        if zh is None:
            return None
        file = open('movie_stop_words')
        stopWords = file.read()
        stopWordList = stopWords.split("\n")
        for stopWord in stopWordList:
            zh = zh.replace(stopWord, '')
        return zh

