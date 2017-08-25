# -*- coding: utf-8 -*-
import json
import uuid

import redis
import requests
from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api

import const
from bili import Bilibili
from matcher import Matcher
from name_finder import NameFinder
from utils import files

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)

origin = 'http://127.0.0.1:8887'
client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True, charset='utf-8')

DANMU_FILE_PATH = '/danmu/'


# @api.representation('application/json')
# def output_json(data, code, headers=None):
#     resp = api.make_response(json.dumps(data), code)
#     resp.headers.extend(headers or {'Access-Control-Allow-Origin':origin})
#     return resp


class HelloWorld(Resource):
    def get(self):
        return {'danmu': 'live'}


class Search(Resource):
    def get(self, keyword):
        b = Bilibili()
        id = b.search_movie(keyword)
        return {'id': id}


class Parse(Resource):
    def get(self, filename):
        n = NameFinder()
        match = n.query_acplay(filename)
        return {'name': match}


class DanmuMatch(Resource):
    def get(self, name):
        m = Matcher()
        play = m.parse_movie_name(name)
        if play is None:
            return {'no': 'match'}, 400
        danmuId = client.get(
            str.format(const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU, play.name, play.year if not play.year is None else ''))
        if not danmuId is None:
            print('danmu for %s is found in local' % (play.name))
            return {'danmuId': danmuId}
        url = Matcher().match_danmu(play)
        if url is None or url == '':
            return {'no': 'match'}, 400
        print('danmu url: %s' % (url))
        r = requests.get(url)
        danmu = Bilibili().convert_danmu_2_json(r.text)
        if not danmu is None:
            danmuId = uuid.uuid4().hex
            files.write_json_file(DANMU_FILE_PATH + danmuId, danmu)
            client.set(str.format(const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU, play.name,
                                  play.year if not play.year is None else ''), danmuId)
            return {'danmuId': danmuId}
        else:
            return {'no': 'match'}, 400


class DanmuByID(Resource):
    def get(self, id):
        return files.open_json_file(DANMU_FILE_PATH + id)


class Test(Resource):
    def get(self):
        return {'cn': '中文'}


class BasicDanmu(Resource):
    def get(self, filename):
        return {"code": 1,
                "danmaku": [
                    {
                        "author": "danmu.live",
                        "time": "0.0000001",
                        "text": filename + "弹幕加载中",
                        "color": "#ffffff",
                        "type": "top"
                    }]}

api.add_resource(Test, '/test')
api.add_resource(HelloWorld, '/')
api.add_resource(DanmuMatch, '/danmu/match/<name>')
api.add_resource(DanmuByID, '/danmu/id/<id>')
api.add_resource(BasicDanmu, '/danmu/basic/<filename>')

if __name__ == '__main__':
    app.run(debug=True)
