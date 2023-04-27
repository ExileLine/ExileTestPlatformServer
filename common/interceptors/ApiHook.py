# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

import re
import time

import shortuuid
from loguru import logger
from flask import request, g, current_app

from common.libs.public_func import print_logs
from common.libs.auth import Token
from common.libs.response_code import UNAUTHORIZED
from common.libs.customException import method_view_ab_code as ab_code


def api_before_request():
    g.log_uuid = "{}_{}".format(str(int(time.time())), shortuuid.uuid())
    logger.info('api_before_request')
    logger.info('request log_uuid:{}'.format(g.log_uuid))
    print_logs()

    open_api_list = ['/api/open_exec', '/api/open_cicd']
    white_list = ['/api/login', '/api/auth', '/api/tourist', '/api/platform_conf']

    PROJECT_ENV = current_app.config.get("PROJECT_ENV")

    if request.path in white_list:
        return

    if re.match(r'/api/case_report/.*', request.path):
        return

    if '/api' in request.path:
        token = request.headers.get('token', '')
        logger.info(f'headers token -> {token}')

        if PROJECT_ENV == "development":  # 开发环境忽略鉴权
            g.app_user = type('A', (object,), {"id": 1, "username": "admin", "is_tourist": 1})
            return

        user_info = Token.get_user_info(token=token)
        if not user_info:
            g.app_user = None
            ab_code(UNAUTHORIZED)

        g.app_user = type('UserInfo', (object,), user_info)


def api_after_request(response):
    logger.info('api_after_request')
    logger.info('response log_uuid:{}'.format(g.log_uuid))
    logger.info('=== response ===')
    response.headers['log_uuid'] = g.log_uuid
    return response
