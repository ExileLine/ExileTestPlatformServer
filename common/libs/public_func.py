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


def json_format(d):
    """json格式打印"""
    try:
        logger.info('\n' + json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        # print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    except BaseException as e:
        logger.info(d)
        # print(d)
