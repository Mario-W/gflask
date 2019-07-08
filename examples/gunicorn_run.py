# coding=utf8

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gflask
import flask


app = flask.Flask(__name__)

@app.route(r'/index/', methods=['GET'])
def index():
    return flask.jsonify({'res': 'ok', 'msg': 'index'})


@app.route(r'/login/', methods=['GET'])
def login():
    return flask.jsonify({'res': 'ok', 'msg': 'login'})


@app.route(r'/get_env_var/', methods=['GET'])
def get_env_var():
    return flask.jsonify({'res': 'ok', 'data': os.environ.items()})


def init_server():
    app.config.from_object('flask_app_config')


def gunicorn_app():
    init_server()
    return app


if __name__ == '__main__':
    init_server()
    gflask.runserver(app=app, reload=True, config=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_file.py'))
