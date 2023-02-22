#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/12/28 11:22
# FileName:

import json
from typing import List

from dao import sql_builder, mysqlDB
from query.bean import setting
from utils import log_sls, pools


class Config:

    """过滤器配置"""

    def __init__(self, filter_name):
        self.filter_name = filter_name

        self.label_col = 'label'
        self.value_col = 'value'
        self.options = None         # 可选值
        self.sql = None
        self.args = None
        self.is_json = False        # 可选值为一个json格式的字符串

    def get_options(self):
        try:
            getattr(self, self.filter_name)()
        except Exception:
            raise Exception(f'暂无{self.filter_name}配置')

        if self.options is None:
            res, ok = mysqlDB.execute(self.sql, self.args)
            if not ok:
                log_sls.error('filterConfig', '数据请求异常', res=res)
                return self.options, False
            self.options = res

        if self.is_json:
            self.options = json.loads(self.options[0]['config']) if self.options else []

        result = []
        for row in self.options:
            # 过滤掉空值
            if (row[self.label_col] is None or row[self.label_col] == '')\
                    and (row[self.value_col] is None or row[self.value_col] == ''):
                continue
            result.append({
                'label': row[self.label_col],
                'value': row[self.value_col],
            })
        return result, True

    # 方法名为过滤器的名称，严格匹配
    # 模板：查sql
    def template_sql(self):
        self.is_json = True
        table = ''
        self.sql, self.args = sql_builder.gen_select_sql(table, ['config'], condition={})

    # 模板：setting
    def template_setting(self):
        self.options = setting.Template.get_options()


def get_filter_options(filter_name) -> List:
    """
    查询单个过滤器的可选值
    :param filter_name:
    :return: [{'label': 显示名, 'value': '真实值'}]
    """
    options, ok = Config(filter_name).get_options()
    if not ok:
        options = []
    return options


def get_filters_options(filter_arr) -> dict:
    """
    批量查询过滤器的可选值
    :param filter_arr: [过滤器名称]
    :return: {过滤器名称: 过滤器的可选值}
    """
    result = {}
    args_list = [[(filter_name,)] for filter_name in filter_arr]
    result_list = pools.execute_thread(get_filter_options, args_list)
    for index, filter_name in enumerate(filter_arr):
        result[filter_name] = result_list[index]
    return result
