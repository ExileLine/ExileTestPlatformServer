# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:11 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : public_func.py
# @Software: PyCharm

import json

from flask import request
from loguru import logger


def print_logs():
    """logs"""
    host = request.host
    method = request.method
    path = request.path
    logger.info(host)
    logger.info(method)
    logger.info(path)
    logger.info('=== headers ===')
    headers = {k: v for k, v in request.headers.items()}
    json_format(headers)
    logger.info('=== params ===')
    json_format(request.args.to_dict())
    logger.info('=== data ===')
    json_format(request.form.to_dict())
    logger.info('=== json ===')
    json_format(request.get_json())
    logger.info('=== end print_logs ===')


def check_keys(dic, *keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True


def json_format(d, msg=None):
    """json格式打印"""
    try:
        logger.info(
            '{}\n'.format(msg) + json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        # print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    except BaseException as e:
        logger.info('{}\n{}'.format(msg, d))
        # print(d)


class RequestParamKeysCheck:
    """
    入参检验
    req_json:

        d = {
                "username":"yang",
                "password":123456
            }

    key_list:

        demo1:
            l = [("username","用户名称"),("password","密码")]
            username: 是需要检查的kay,
            用户名称: 是返回给前端的文字描述

        demo2:
            l2 =  ["username", "password"]
            默认: [("username","username"), ("password","password")]


    _bool, _msg = RequestParamKeysCheck(req_json=d, key_list=l).ck()

    """

    def __init__(self, req_json, key_list):
        if not isinstance(req_json, dict):
            raise TypeError('req_json 类型应该为:dict, 而不是:{}'.format(type(req_json)))

        if not isinstance(key_list, list):
            raise TypeError('key_list 类型应该为:list, 而不是:{}'.format(type(key_list)))

        self.req_json = req_json
        self.key_list = key_list

    @staticmethod
    def __check_keys(dic, *keys):
        for k in keys:
            if k[0] not in dic.keys():
                return False, "缺少参数:{}".format(k[1])
        return True, "pass"

    def ck(self):
        """ck"""
        if self.req_json and self.key_list:
            for k in self.key_list:
                if not isinstance(k, tuple):
                    k = (k, k)
                if k[0] not in self.req_json.keys():
                    return False, "缺少参数:{}".format(k[1])
            return True, "pass"


if __name__ == '__main__':
    d = {"a": "b"}
    print(check_keys(d, *["b"]))
