from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

redis = FlaskRedis(app)
