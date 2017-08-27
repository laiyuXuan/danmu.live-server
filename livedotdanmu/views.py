# -*- coding: utf-8 -*-
import uuid

from flask_cors import CORS
from flask_restful import Resource, Api

from livedotdanmu import matcher, bilibili, const, redis, app
from livedotdanmu.utils import files

api = Api(app)
CORS(app, supports_credentials=True)


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
        id = bilibili.search_movie(keyword)
        return {'id': id}


class DanmuMatch(Resource):
    def get(self, name):
        play = matcher.parse_play_by_name(name)
        if play is None:
            return {'no': 'match'}, 400
        danmuId = redis.get(
            str.format(const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU, play.name, play.year if not play.year is None else ''))
        if not danmuId is None:
            print('danmu for %s is found in local' % (play.name))
            return {'danmuId': danmuId}
        danmu = matcher.match_danmu(play)
        if danmu is None or danmu == '':
            return {'no': 'match'}, 400
        danmuId = uuid.uuid4().hex
        files.write_json_file(app.config['DANMU_FILE_PATH'] + danmuId, danmu)
        redis.set(str.format(
            const.PREFIX_MOVIVE_NAME_YEAR_2_DANMU, play.name, play.year if not play.year is None else ''), danmuId)
        return {'danmuId': danmuId}


class DanmuByID(Resource):
    def get(self, id):
        return files.open_json_file(app.config['DANMU_FILE_PATH'] + id)


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


api.add_resource(HelloWorld, '/')
api.add_resource(DanmuMatch, '/danmu/match/<name>')
api.add_resource(DanmuByID, '/danmu/id/<id>')
api.add_resource(BasicDanmu, '/danmu/basic/<filename>')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
