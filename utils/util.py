#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/7 18:33
# FileName:

import datetime
import hashlib
import logging
import os
import platform
import random
import time
import typing
import uuid
from functools import wraps
from typing import List

import pytz


def asia_local_time(to_str: bool = True, fmt='%Y-%m-%d %H:%M:%S'):
    now = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
    result = now
    if to_str:
        result = datetime.datetime.strftime(now, fmt)
    return result


def time2str(t=None, fmt="%Y-%m-%d %H:%M:%S") -> str:
    """
    时间timestamp转字符串
    :param t: 时间戳
    :param fmt:
    :return:
    """
    t = time.time() if t is None else t
    return time.strftime(fmt, time.localtime(t))


def get_delay_date(date_str: str = '', delay: int = 0, date_type='str'):
    """
    获取指定日期的几日前或后的日期
    :param date_str: 日期，默认为当前日期。
    :type date_str: 2020-01-01
    :param delay: 间隔天数。正数为往后，负数为往前。
    :type delay: int
    :param date_type: 返回类型
    :type date_type: str、datetime
    :return:
    :rtype:
    """
    if not date_str:
        date_str = str(datetime.datetime.now().date())
    delay_date = datetime.datetime.strptime(date_str, "%Y-%m-%d") + datetime.timedelta(days=delay)
    if date_type == 'str':
        return datetime.datetime.strftime(delay_date, "%Y-%m-%d")
    elif date_type == 'datetime':
        return delay_date
    return None


def hash_list(dict_list: List[dict], hash_field):
    arr = []
    for item in dict_list:
        v = item.get(hash_field, None)
        if not v:
            continue
        m = hashlib.md5()
        m.update(v.lower().encode(encoding='UTF-8'))
        arr.append(m.hexdigest())
    return arr


def random_string(length: int, choices: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> str:
    """随机字符串"""
    return ''.join(random.choice(choices) for _ in range(length))


def md5(s: typing.Union[str, bytes]) -> str:
    """md5"""
    if isinstance(s, str):
        s = s.encode(encoding='UTF-8')
    return hashlib.md5(s).hexdigest()


def gen_unique_str(key: str = None):
    key = random_string(3) if key is None else key
    key = f'{time.time()}{uuid.uuid4()}{key}'
    return md5(key)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def remove_dir(path):
    if os.path.exists(path):
        os.remove(path)


def is_linux():
    return platform.system().lower() == 'linux'


def error_alarm(ignore_except_list: List = [], raise_error: bool = True, alarm_func: dict = None):
    """
    异常告警装饰器
    :param ignore_except_list: 忽略的异常类型
    :param raise_error: 是否推出异常
    :param alarm_func: 异常发生时的告警处理
    :return:
    """
    def do(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            res = None
            try:
                res = func(*args, **kwargs)
            except (*ignore_except_list, ):
                pass
            except Exception as e:
                if alarm_func is not None:
                    # 报警
                    logging.error(e)
                    alarm_func['func'](*alarm_func.get('args', []), **alarm_func.get('kwargs', {}))
                if raise_error:
                    print('raise')
                    raise Exception
            return res
        return decorated_func
    return do
