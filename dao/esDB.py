#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/12/13 11:18
# FileName:

from config import conf
from dao import poolDB, db


class Elasticsearch:

    def __init__(self, db_conf, use_pool) -> None:
        if use_pool:
            self.__conn = poolDB.get_coon(mode='elasticsearch', db_conf=db_conf)
        else:
            self.__conn = db.Db('elasticsearch', db_conf=db_conf)

    @property
    def coon(self):
        return self.__conn

    def execute(self, index_name: str, action: str, *args, **kwargs):
        """

        :param index_name: 指定的索引
        :param action: 执行的命令
        :param args:
        :param kwargs:
        :return:
        """
        with self.__conn as coon:
            try:
                ok = True

                res = getattr(coon, action)(index=index_name, *args, **kwargs)
            except Exception as e:
                ok = False
                res = e
        return res, ok


def execute(
    index_name: str, action: str, *args,
    db_conf: dict = None,
    use_pool=False, **kwargs,
):
    if db_conf is None:
        db_conf = {
            'host': conf.ES_HOST,
            'port': conf.ES_PORT,
            'user': conf.ES_USER,
            'password': conf.ES_PWD,
        }
    es = Elasticsearch(db_conf, use_pool)
    return es.execute(index_name, action, *args, **kwargs)


if __name__ == '__main__':
    # result, _ = execute('demo', 'index', {'name': 'test_01'})
    # print(result)
    ...