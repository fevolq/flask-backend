#!-*coding:utf-8 -*-
# python3.7
# CreateTime: 2023/2/22 10:57
# FileName:

from flask import Blueprint, request, jsonify

from module import template_logic

template_route = Blueprint('template', __name__)


@template_route.route('info', methods=['GET', 'POST'])
def template():
    res = template_logic.Template().info(request)
    return jsonify(res)


@template_route.route('config', methods=['GET'])
def filter_config():
    query = request.args.getlist('query')
    res = template_logic.Template().filters(query)
    return jsonify(res)
