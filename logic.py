#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 11:45
# FileName:

from status_code import StatusCode
from module.TemplateLogic.TemplateLogic import TemplateLogic


class Logic:

    def __init__(self):
        self._template = TemplateLogic()

    def call(self, api_path: str, func, request, req_dic):
        if api_path.startswith('template/'):
            target_obj = self._template
        else:
            return {'code': StatusCode.is_conflict, 'msg': '请重新登录'}

        return func(target_obj, request, req_dic)

    def before_call(self, api_path, request):
        pass

    def after_call(self, request, req_obj, api_path, respond):
        return respond
