#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 11:43
# FileName:

import flask_app

from logic import Logic
from config import conf


def app_init():
    flask_app.logic = Logic()


app = flask_app.app
app_init()


if __name__ == '__main__':
    app.run(
        host=conf.app_host,
        port=conf.app_port,
        threaded=conf.use_thread
    )
