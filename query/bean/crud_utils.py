#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2022/12/28 14:11
# FileName:

from typing import List

from dao import sql_builder, mysqlDB


def check_conflict(table, unique_fields: List, check_values: dict, cols: List = None, only_update: bool = True) -> (dict, bool):
    """
    冲突校验
    :param table:
    :param unique_fields: 索引唯一行的字段
    :param check_values: 校验的键值对，需要包含unique_fields的键值对。{field: value}
    :param cols: 查询的字段
    :param only_update: 是否为更新已有记录。当记录为空时，若为False，则为不冲突
    :return: dict, bool
    """
    cols = list(check_values.keys()) if cols is None else cols
    cols.extend(list(check_values.keys()))

    condition = {}
    for field in unique_fields:
        op = 'IS NULL' if check_values[field] is None else '='
        condition[field] = {op: check_values[field]}
    sql, args = sql_builder.gen_select_sql(table, list(set(cols)), condition=condition, limit=1)
    res, ok = mysqlDB.execute(sql, args)
    if not ok:
        return res, True
    if not res:
        if only_update:
            return res, True
        else:
            return res, False

    is_conflict = False
    for field in check_values:
        check_value = check_values[field]
        value = res[0][field]
        if check_value != value:
            is_conflict = True
            break
    return res[0], is_conflict


def gen_where_str(filter_name, filter_conf, values) -> (str, List):
    """
    根据过滤器配置生成where语句
    :param filter_name: 过滤器名称
    :param filter_conf: 过滤器配置
    :param values: 过滤器的值
    :return: where语句, 值
    """
    where_str, args_arr = '', []
    if isinstance(filter_conf, dict):
        where_str, args_arr = one_filter(filter_name, filter_conf, values)
    elif isinstance(filter_conf, list):
        # 一个过滤器查询多个字段，or连接
        where_arr = []
        for one_filter_conf in filter_conf:
            tmp_where_str, tmp_args_arr = one_filter(filter_name, one_filter_conf, values)
            where_arr.append(tmp_where_str)
            args_arr.extend(tmp_args_arr)
        where_str = f'({" OR ".join(where_arr)})'
    else:
        raise Exception('过滤器配置格式异常')
    return where_str, args_arr


def one_filter(filter_name, filter_conf, values):
    """
    filter_conf = {
        'table': str,表,
        'relate_field': str,对应字段,
        'mode': str,匹配模式,
        'type': Any,值的类型，可选,
        'time_field': bool,是否为时间字段,默认false,
        'accurate_second': bool,是否精确到秒,默认false,
    }
    """
    table = filter_conf['table']
    relate_field = filter_conf['relate_field']
    mode = filter_conf['mode'].lower()

    if filter_conf.get('time_field', False) and not filter_conf.get('accurate_second', False):
        values[-1] = f'{values[-1]} 23:59:59'

    if filter_conf.get('type', None) == int:
        # 当数据库字段为整型时，若查询字段为字符串，则会自动转变为0
        tmp_values = []
        for value in values:
            try:
                value = int(value)
                tmp_values.append(value)
            except ValueError:
                raise Exception(f'过滤器{filter_name}传值异常')
            except Exception as e:
                raise e
        values = tmp_values

    if mode == 'in':
        where_str = f'(`{table}`.`{relate_field}` IN ({",".join(["%s"] * len(values))}))'
        args_arr = values
    elif mode == '=':
        where_str = f'(`{table}`.`{relate_field}` = %s)'
        args_arr = [values[0]]
    elif mode == '>==<':
        where_str = f'(`{table}`.`{relate_field}` >= %s AND `{table}`.{relate_field} <= %s)'
        args_arr = [values[0], values[-1]]
    elif mode == 'isnull':
        value = 'NOT NULL' if values[0] else 'NULL'
        where_str = f'(`{table}`.`{relate_field}` IS {value})'
        args_arr = []
    elif mode == 'like':
        one_str = f'`{table}`.`{relate_field}` LIKE %s'
        where_str = f'({" OR ".join([one_str] * len(values))})'
        args_arr = [f'%{item}%' for item in values]
    else:
        raise Exception(f'未实现{mode}模式')
    return where_str, args_arr
