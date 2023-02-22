#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/8 11:26
# FileName:


import json

import requests

from config import conf


def base_request(api_path, method, params=None, data=None):
    resp = requests.request(method, url=f'http://localhost:{conf.app_port}/{api_path}', params=params, json=data)
    if resp.status_code == 200:
        data = resp.json()
        try:
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except UnicodeEncodeError:
            print(json.dumps(data, indent=4))
    else:
        print(f'{api_path} 请求失败')


def info():
    api_path = 'template/info'
    method = 'get'
    params = {
        'params': [1, 2, 3],
    }
    data = {
        'data': ['a', 'b', 'c']
    }
    return base_request(api_path, method, params=params, data=data)


def config():
    api_path = 'template/config'
    method = 'get'
    data = {'query': ['template_setting']}
    return base_request(api_path, method, params=data)


if __name__ == '__main__':
    # info()
    # config()

    ...
