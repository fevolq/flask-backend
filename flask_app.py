#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 11:44
# FileName:

import logging
import os
import random
import time
from functools import wraps

from flask import Flask, request, make_response
from flask.typing import ResponseReturnValue
from flask.views import View

from status_code import StatusCode
from config import conf
from query.bean import global_func
from utils import util, log_init


# 日志初始化
log_init.init_logging(os.path.join(os.path.dirname(__file__), conf.app_log_path), datefmt='%Y-%m-%d %H:%M:%S')


def create_app(secret_key='template'):
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        SECRET_KEY=secret_key,
    )

    @flask_app.route('/')
    def hello():
        return f'Hello World!!!'

    return flask_app


app: Flask = create_app()

logic = None


class TemplateView(View):

    def __init__(self, api_path, func):
        self.api_path = api_path
        self.func = func

    def dispatch_request(self) -> ResponseReturnValue:
        start = time.time()
        require_id = str(int(start*1000)) + ''.join([str(random.randint(1, 10)) for _ in range(6)])
        logging.info(f'{require_id}; {self.api_path}; StartTime：{util.time2str(start)}')
        g_call = global_func.g_args('call')
        g_call['require_id'] = require_id
        try:
            logic.before_call(self.api_path, request)
            if request.is_json:
                req_dic = request.get_json(force=True)
            else:
                # req_dic = request.get_data().decode()
                req_dic = dict(request.args)        # TODO: 参数处理待优化
            logging.info(f'{require_id}; args: {req_dic if req_dic else None}; method: {request.method}')
            respond = logic.call(self.api_path, self.func, request, req_dic)
            respond = logic.after_call(request, req_dic, self.api_path, respond)
        except Exception as e:
            logging.exception(e)
            respond = {'code': StatusCode.failure}
        finally:
            end = time.time()
            logging.info(f'{require_id}; {self.api_path}; EndTime：{util.time2str(end)}')
            respond = make_response(respond)
            respond.headers['X-TIME'] = f'{str(int(end - start)*1000)} ms'
            return respond


@app.before_request
def before_call():
    ...


@app.after_request
def after_call(response):
    ...
    return response


# 注册路由
def api_route(api_path, **api_kwargs):
    def reg_api(func):
        reg_api_path = f'/{api_path}'
        methods = api_kwargs.get('methods', None)
        if not methods:
            methods = ['GET']
        elif isinstance(methods, str):
            methods = [methods.upper()]
        elif not isinstance(methods, list):
            raise Exception(f'【{reg_api_path}】请求方式异常')
        else:
            pass
        app.add_url_rule(reg_api_path,
                         view_func=TemplateView.as_view(api_path,
                                                        api_path=api_path,
                                                        func=func),
                         methods=methods)
        logging.info(f'reg api: {reg_api_path}, methods: {methods}, func: {func.__name__}')
        @wraps(func)
        def reg_log(*args, **kwargs):
            logging.info(f'call api: {reg_api_path}, func: {func.__name__}')
            return func(*args, **kwargs)
        return reg_log
    return reg_api
