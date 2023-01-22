# -*- coding: utf-8 -*-
# @Time    : 2019/4/19 12:00 PM
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : api_result.py
# @Software: PyCharm

from enum import Enum

from flask import jsonify


def _result(*args):
    """格式化"""
    try:
        return {"code": args[0], "message": args[1]}
    except IndexError:
        return {"code": 0, "message": "内部异常:枚举异常"}


class ResponseCode(Enum):
    """响应码"""

    SUCCESS = _result(200, "操作成功")


SUCCESS, SUCCESS_MESSAGE = 200, "操作成功"
POST_SUCCESS = 201
PUT_SUCCESS = 203
DEL_SUCCESS = 204

Unauthorized = 401  # 未授权

REQUIRED = 10001  # 必传
NO_DATA = 10002  # 未找到
UNIQUE_ERROR = 10003  # 唯一校验
TYPE_ERROR = 10004  # 类型错误
BUSINESS_ERROR = 10005  # 业务校验错误
DATA_ERROR = 10006  # 请求参数错误


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


if __name__ == '__main__':
    print(ResponseCode.SUCCESS.value)
    print(ResponseCode.SUCCESS.name)
