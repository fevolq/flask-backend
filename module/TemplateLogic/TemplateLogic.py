#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 11:46
# FileName:

import flask

from flask_app import api_route
from config import conf
from status_code import StatusCode


class TemplateLogic:

    def __init__(self):
        pass

    @api_route('template/info', methods=['GET', 'POST'])
    def info(self, request: flask.request, req_dic):
        resp = {
            'code': StatusCode.success,
            'msg': '测试',
            'method': request.method,
            'args': req_dic,
            'db': conf.MYSQL_DB,
        }
        return resp
