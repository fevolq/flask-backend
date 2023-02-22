#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/11/28 18:52
# FileName:

from config import conf
from dao import poolDB, db


class Mongo:

    def __init__(self, db_name, db_conf, use_pool) -> None:
        if use_pool:
            self.__conn = poolDB.get_coon(mode='mongo', db_name=db_name, db_conf=db_conf)
            pass
        else:
            self.__conn = db.Db('mongo', db_name, db_conf)

    @property
    def coon(self):
        return self.__conn

    def execute(self, collection_name: str, action: str, *args, **kwargs):
        """

        :param action: 执行的命令
        :param collection_name: 指定的集合
        :param args:
        :param kwargs:
        :return:
        """
        with self.__conn as coon:
            try:
                ok = True

                cursor = coon[collection_name]
                res = getattr(cursor, action)(*args, **kwargs)
                if action.lower().startswith('find'):   # 查询操作，必须在关闭游标前拿出结果
                    res = list(res)
            except Exception as e:
                ok = False
                res = e
        return res, ok


def execute(
    collection_name: str, action: str, *args,
    db_name: str = None, db_conf: dict = None,
    use_pool=True, **kwargs,
):
    use_pool = False        # 强制使用Db实现
    if db_name is None:
        db_name = conf.MONGO_DB
    if db_conf is None:
        db_conf = {
            'host': conf.MONGO_HOST,
            'port': conf.MONGO_PORT,
            'user': conf.MONGO_USER,
            'password': conf.MONGO_PWD,
        }
    mongo = Mongo(db_name, db_conf, use_pool)
    return mongo.execute(collection_name, action, *args, **kwargs)


if __name__ == '__main__':
    # result, _ = execute('user', 'find', '', db_name='log')
    # result, _ = execute('user', 'insert_many', [{'name': 'test_01'}], db_name='log').acknowledged
    # print(result)
    ...
