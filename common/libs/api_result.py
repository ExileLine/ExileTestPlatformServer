# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 12:00 PM
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : api_result.py
# @Software: PyCharm


from flask import jsonify


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
