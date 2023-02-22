#!-*-coding:utf-8 -*-
# python3.7
# Create time: 2022/10/11 14:10
# Filename: 连接池

import hashlib
import threading

from dbutils.pooled_db import PooledDB
import redis
import pymysql
from elasticsearch import Elasticsearch


class PoolDB:

    # instance = None
    _lock = threading.RLock()
    __pools = {}  # key: PooledDB()

    # 不使用单例，否则属性会冲突覆盖
    # def __new__(cls, *args, **kwargs):
    #     # 构造单例
    #     if hasattr(cls, 'instance'):
    #         return cls.instance
    #
    #     # 线程锁
    #     with cls._lock:
    #         if not hasattr(cls, 'instance'):
    #             cls.instance = super(PoolDB, cls).__new__(cls)
    #         return cls.instance

    def __init__(self, mode: str, db_name, db_conf):
        self._mode = mode
        self._db_name = db_name
        self._db_conf = db_conf

        self.__key = hashlib.md5(f'{self._mode}/{self._db_name}/{self._db_conf}'.encode(encoding='UTF-8')).hexdigest()
        if self.__key not in PoolDB.__pools:
            self._prepare()

    def _prepare(self):
        if self._mode.lower() == 'mysql':
            creator = pymysql
            host = self._db_conf['host']
            port = self._db_conf['port']
            user = self._db_conf['user']
            password = self._db_conf['password']
            database = self._db_name

            pool = PooledDB(
                creator=creator,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                autocommit=True,
                charset='utf8mb4',
                read_timeout=20,
                write_timeout=60,
                maxconnections=100,
                mincached=3,
                maxusage=30,
                blocking=True,
                cursorclass=pymysql.cursors.DictCursor,
                ping=7
            )
        elif self._mode.lower() == 'redis':
            host = self._db_conf['host']
            port = self._db_conf['port']
            password = self._db_conf['password']
            database = self._db_name

            pool = redis.ConnectionPool(
                host=host,
                port=port,
                password=password,
                db=database,
                max_connections=100,
                decode_responses=True,
            )
        elif self._mode.lower() == 'elasticsearch':
            host = self._db_conf['host']
            port = self._db_conf['port']
            user = self._db_conf['user']
            password = self._db_conf['password']

            pool = Elasticsearch(
                hosts=f'http://{host}:{port}',
                http_auth=(user, password),
                sniff_on_node_failure=True,
                sniff_timeout=60,
            )
        else:
            raise Exception(f'mode错误，当前未实现{self._mode}模式')
        PoolDB.__pools[self.__key] = pool

    def get_connection(self):
        coon = None
        if self._mode == 'mysql':
            coon = PoolDB.__pools[self.__key].connection()
        elif self._mode == 'redis':
            coon = redis.Redis(connection_pool=PoolDB.__pools[self.__key])
        elif self._mode == 'mongo':
            pass
        elif self._mode == 'elasticsearch':
            coon = PoolDB.__pools[self.__key]
            if not coon.ping():
                self._prepare()
                return self.get_connection()
        return coon


def get_coon(mode: str = 'mysql', **kwargs):
    """

    :param mode: 使用的模式
    :param kwargs:
    :return:
    """
    db_name = kwargs.get('db_name', None)
    db_conf = kwargs.get('db_conf', None)

    dbpool = PoolDB(mode, db_name, db_conf)
    return dbpool.get_connection()
