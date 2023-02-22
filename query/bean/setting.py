#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/12/16 11:17
# FileName:

from query.bean import num_obj


class BaseSetting:
    options = None
    unique_row = None
    memo = None

    def __repr__(self):
        return self.memo

    @classmethod
    def get_options(cls):
        return [
            {'label': None, 'value': None, },
        ]


class Template(BaseSetting):
    options = num_obj.Template
    unique_row = 'template.col'
    memo = '配置模板'

    def __repr__(self):
        return self.memo

    @classmethod
    def get_options(cls):
        return [
            {'label': '等待中', 'value': cls.options.yet.value, },
            {'label': '进行中', 'value': cls.options.ready.value, },
            {'label': '已结束', 'value': cls.options.end.value, },
        ]
