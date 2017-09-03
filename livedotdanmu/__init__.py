from flask import Flask
from flask_redis import FlaskRedis
from redis import Redis

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.dev')
app.config.from_pyfile('config.py')

redis:Redis = FlaskRedis(app)
