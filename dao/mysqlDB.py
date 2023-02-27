#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/11/22 14:14
# FileName:

import json
import logging

from utils import DataEncoder, log_sls
from dao import poolDB, db, db_execption
from config import conf


class Mysql:

    def __init__(self, db_name, db_conf, use_pool) -> None:
        if use_pool:
            self.__conn = poolDB.get_coon(mode='mysql', db_name=db_name, db_conf=db_conf)
        else:
            self.__conn = db.Db('mysql', db_name, db_conf)

    @property
    def coon(self):
        return self.__conn

    def execute(self, sql, args, **kwargs):
        to_json = kwargs.pop('to_json') if 'to_json' in kwargs else True  # 是否进行json转换
        raise_error = kwargs.pop('raise_error') if 'raise_error' in kwargs else True    # 是否扔出异常
        log_key = kwargs.pop('log_key') if 'log_key' in kwargs else None

        res = {'result': None, 'success': True}
        with self.__conn as conn:
            try:
                conn.begin()
                cursor = conn.cursor()
                sql = sql.replace('\'%s\'', '%s').strip()
                logging_sql(sql, args, key=log_key)
                if sql.startswith('SELECT') or sql.startswith('select'):
                    cursor.execute(sql, args)
                    result = cursor.fetchall()
                    if to_json:
                        result = json.loads(json.dumps(result, cls=DataEncoder.MySQLEncoder))
                else:
                    if not args:
                        result = cursor.execute(sql, args)
                    elif isinstance(args[0], (list, tuple)):
                        result = cursor.executemany(sql, args)
                    else:
                        result = cursor.execute(sql, args)
                conn.commit()
                res['result'] = result
            except Exception as e:
                conn.rollback()
                res['success'] = False
                res['result'] = e
                if raise_error:
                    raise db_execption.DbException(e)

        return res

    def execute_many(self, sql_with_args_list: list, **kwargs):
        to_json = kwargs.pop('to_json') if 'to_json' in kwargs else True  # 是否进行json转换
        raise_error = kwargs.pop('raise_error') if 'raise_error' in kwargs else True  # 是否扔出异常
        log_key = kwargs.pop('log_key') if 'log_key' in kwargs else None

        res = {'result': None, 'success': True}
        with self.__conn as conn:
            try:
                conn.begin()
                cursor = conn.cursor()
                result = [[]] * len(sql_with_args_list)
                for sql_with_args in sql_with_args_list:
                    sql = sql_with_args['sql'].replace('\'%s\'', '%s').strip()
                    args_list = sql_with_args.get('args', [])
                    logging_sql(sql, args_list, key=log_key)
                    if sql.startswith('SELECT'):
                        cursor.execute(sql, args_list)
                        result_ = cursor.fetchall()
                        if to_json:
                            result_ = json.loads(json.dumps(result_, cls=DataEncoder.MySQLEncoder))
                        result[sql_with_args_list.index(sql_with_args)] = result_
                    else:
                        if not args_list:
                            res_line = cursor.execute(sql, args_list)
                        elif isinstance(args_list[0], (list, tuple)):
                            res_line = cursor.executemany(sql, args_list)
                        else:
                            res_line = cursor.execute(sql, args_list)
                        result[sql_with_args_list.index(sql_with_args)] = res_line
                conn.commit()
                res['result'] = result
            except Exception as e:
                conn.rollback()
                res['success'] = False
                res['result'] = e
                if raise_error:
                    raise db_execption.DbException(e)

        return res


def execute(
    sql: str, args: list = [],
    db_name: str = None, db_conf: dict = None,
    use_pool: bool = True, **kwargs,
):
    """
    单条sql语句
    :param sql: SELECT * FROM `demo` WHERE `id` = %s AND `name` = %s
    :param args: [1, 'test']
    :param db_name: 指定库
    :param db_conf:数据库配置
    :param use_pool: 是否使用连接池
    :return:
    """
    if db_name is None:
        db_name = conf.MYSQL_DB
    if db_conf is None:
        db_conf = {
            'host': conf.MYSQL_HOST,
            'port': conf.MYSQL_PORT,
            'user': conf.MYSQL_USER,
            'password': conf.MYSQL_PWD,
        }
    return Mysql(db_name, db_conf, use_pool).execute(sql, args, **kwargs)


def execute_many(
    sql_with_args_list,
    db_name: str = None, db_conf: dict = None,
    use_pool: bool = True, **kwargs
):
    """
    一个事务中的多条sql语句
    :param sql_with_args_list: [{'sql': sql, 'args': args}, ...]
    :param db_name: 指定库
    :param db_conf:数据库配置
    :param use_pool: 是否使用连接池
    :return:
    """
    if db_name is None:
        db_name = conf.MYSQL_DB
    if db_conf is None:
        db_conf = {
            'host': conf.MYSQL_HOST,
            'port': conf.MYSQL_PORT,
            'user': conf.MYSQL_USER,
            'password': conf.MYSQL_PWD,
        }
    return Mysql(db_name, db_conf, use_pool).execute_many(sql_with_args_list, **kwargs)


def logging_sql(sql, args, key: str = None):
    for item in args:
        if isinstance(item, int) or isinstance(item, float):
            sql = sql.replace('%s', str(item), 1)
        else:
            if item and (item.find('"') > -1 or item.find("'") > -1):
                item = item.replace('"', r'\"').replace("'", r"\'")
            sql = sql.replace('%s', f"'{item}'", 1)

    kwargs = {
        'sql': sql
    }
    if key is not None:
        kwargs['key'] = key

    # logging.info(f'sql: {sql}')
    log_sls.info('sql', '执行sql', **kwargs)


if __name__ == "__main__":
    ...

    # tmp_sql = 'show database;'
    # tmp_res = execute(tmp_sql, use_pool=True)
    # # tmp_res = execute_many([{'sql': sql}], use_pool=use_pool)
    #
    # print(tmp_res)
