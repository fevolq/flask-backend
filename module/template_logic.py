#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/7 16:47
# FileName:

from typing import List


import status_code
from query.bean import (
    filter_config
)


class Template:

    def __init__(self): ...

    @staticmethod
    def info(request):
        data = {
            'code': status_code.StatusCode.success,
            'method': request.method,
        }
        return data

    @staticmethod
    def filters(query: List):
        result = filter_config.get_filters_options(query)
        return {
            'code': status_code.StatusCode.success,
            'data': result,
        }
