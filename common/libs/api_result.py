# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 12:00 PM
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : api_result.py
# @Software: PyCharm


from flask import jsonify

SUCCESS = 200
POST_SUCCESS = 201
PUT_SUCCESS = 203
DEL_SUCCESS = 204

REQUIRED = 10001  # 必传
NO_DATA = 10002  # 未找到
UNIQUE_ERROR = 10003  # 唯一的
TYPE_ERROR = 10004  # 类型错误
BUSINESS_ERROR = 10005  # 业务检验错误


def api_result(code=None, message=None, data=None, details=None, status=None):
    """
    返回格式
    :param code:
    :param message:
    :param data:
    :param details:
    :param status:
    :return:
    """
    result = {
        "code": code,
        "message": message,
        "data": data,
    }

    if not result.get('data'):
        result.pop('data')

    return jsonify(result)
