#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/10/27 16:54
# FileName:

from typing import Any

from dao import poolDB, db
from config import conf


class Redis:

    def __init__(self, db_name, db_conf, use_pool) -> None:
        if use_pool:
            self.__conn = poolDB.get_coon(mode='redis', db_name=db_name, db_conf=db_conf)
        else:
            self.__conn = db.Db('redis', db_name, db_conf)

    @property
    def coon(self):
        return self.__conn

    def execute(self, action, *args, **kwargs) -> (Any, bool):
        with self.__conn as coon:
            try:
                ok = True
                res = getattr(coon, action)(*args, **kwargs)
            except Exception as e:
                ok = False
                res = e
        return res, ok


def redis_obj(
    db_name: int = None, db_conf: dict = None,
    use_pool: bool = True,
):
    if db_name is None:
        db_name = 0
    else:
        db_name = conf.REDIS_DB.get(db_name, db_name)
    if db_conf is None:
        db_conf = {
            'host': conf.REDIS_HOST,
            'port': conf.REDIS_PORT,
            'password': conf.REDIS_PWD,
        }
    return Redis(db_name, db_conf, use_pool)


def execute(
    action: str, *args,
    db_name: int = None, db_conf: dict = None,
    use_pool=True, **kwargs,
):
    redis = redis_obj(db_name=db_name, db_conf=db_conf, use_pool=use_pool)
    return redis.execute(action, *args, **kwargs)


if __name__ == '__main__':
    ...
    result = '...'

    # # string
    # result, ok = execute('set', 'key_string', 11, db_name=14, use_pool=False)
    # result, ok = execute('get', 'key_string', db_name=14, use_pool=False)         # 获取单个
    # result, ok = execute('mget', ['key_string', ], db_name=14, use_pool=False)    # 获取指定的多个key

    # # hash
    # result, ok = execute('hset', 'key_hash', 'a', 11, db_name=14, use_pool=False)      # 单个键值对
    # result, ok = execute('hmset', 'key_hash', {'b': 22, 'c': 'cc'}, db_name=14, use_pool=False)    # 多个键值对
    # result, ok = execute('hget', 'key_hash', 'a', db_name=14, use_pool=True)      # 获取指定键的值
    # result, ok = execute('hgetall', 'key_hash', db_name=14, use_pool=True)        # 获取所有键值对

    # # set
    # result, ok = execute('sadd', 'key_set', 'a', 11, 22, db_name=14, use_pool=True)
    # result, ok = execute('smembers', 'key_set', db_name=14, use_pool=True)

    print(type(result))
    print(result, type(result))
