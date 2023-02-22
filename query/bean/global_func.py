#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 13:53
# FileName:

import flask


# 设置或取出全局参数g
def g_args(args):
    value = flask.g.get(args, None)
    if value is None:
        setattr(flask.g, args, {})
    return getattr(flask.g, args)
