# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 5:11 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : public_func.py
# @Software: PyCharm

import time
import json
from functools import wraps

from flask import request
from loguru import logger


def print_logs():
    """logs"""
    host = request.host
    ip_address = request.headers.get('X-Forwarded-For')
    method = request.method
    path = request.path
    headers = {k: v for k, v in request.headers.items()}
    params = request.args.to_dict()
    form_data = request.form.to_dict()
    logger.info(f"host:{host}")
    logger.info(f"ip_address:{ip_address}")
    logger.info(f"method:{method}")
    logger.info(f"path:{path}")
    logger.info('=== headers ===')
    json_format(headers)
    logger.info('=== params ===')
    json_format(params)
    logger.info('=== data ===')
    json_format(form_data)
    logger.info('=== json ===')
    try:
        json_format(request.get_json())
    except BaseException as e:
        print({})
    logger.info('=== end print_logs ===')


def check_keys(dic, *keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True


def json_format(data):
    """json格式打印"""
    try:
        result = json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False)
        logger.info(f'\n{result}')
    except BaseException as e:
        logger.info(f'\n{data}')


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('func name:{}'.format(func.__name__))
        print('func doc:{}'.format(func.__doc__))
        print('func param:{}'.format(args))
        print('func param:{}'.format(kwargs))
        print("计时开始")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print("计时结束")
        print(f"程序用时{int(total_time // 60)}分{total_time % 60:.2f}秒")

    return wrapper


class RequestParamKeysCheck:
    """
    入参检验必须要传递的kay

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
        """

        :param req_json: 请求参数
        :param key_list: 需要检验的key列表
        """
        if not isinstance(req_json, dict):
            raise TypeError(f'req_json 类型应该为:dict, 而不是:{type(req_json)}')

        if not isinstance(key_list, list):
            raise TypeError(f'key_list 类型应该为:list, 而不是:{type(key_list)}')

        self.req_json = req_json
        self.key_list = key_list

    def result(self):
        """结果"""

        if not self.req_json or not self.key_list:
            return True, "pass"

        for key in self.key_list:
            if not isinstance(key, tuple):
                key = (key, key)

            if key[0] not in self.req_json.keys():
                return False, f"缺少必须参数:{key[1]}"
        return True, "pass"


class ActionSet:

    @classmethod
    def gen_intersection(cls, l_list, r_list):
        """交集"""
        jj = list(set(l_list).intersection(set(r_list)))
        return jj

    @classmethod
    def gen_difference(cls, l_list, r_list):
        """差集"""
        cj = list(set(l_list).difference(set(r_list)))
        return cj

    @classmethod
    def gen_union(cls, l_list, r_list):
        """并集"""
        bj = list(set(l_list).union(r_list))
        return bj

    @classmethod
    def check_difference(cls, l_list, r_list):
        """检查差集"""
        r1 = bool(cls.gen_intersection(l_list, r_list))
        r2 = bool(cls.gen_intersection(r_list, l_list))
        if r1 and r2:
            return True
        return False


if __name__ == '__main__':
    d = {"a": "b"}
    print(check_keys(d, *["b"]))

    l1 = [1, 2, 3]
    l2 = [1, 2, 5, 6]

    print("交集:", ActionSet.gen_intersection(l1, l2))
    print("交集:", ActionSet.gen_intersection(l2, l1))

    print("差集l1-l2:", ActionSet.gen_difference(l1, l2))
    print("差集l2-l1:", ActionSet.gen_difference(l2, l1))

    print("并集:", ActionSet.gen_union(l1, l2))
    print("并集:", ActionSet.gen_union(l2, l1))

    print(ActionSet.check_difference(l1, l2))
