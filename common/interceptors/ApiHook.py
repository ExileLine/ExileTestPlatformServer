# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

import time

import shortuuid
from loguru import logger
from flask import request, g

from app.models.admin.models import Admin
from common.libs.public_func import print_logs
from common.libs.auth import Token
from common.libs.response_code import UNAUTHORIZED
from common.libs.customException import method_view_ab_code as ab_code
from common.interceptors.ProjectHook import check_project_auth


def api_before_request():
    g.log_uuid = "{}_{}".format(str(int(time.time())), shortuuid.uuid())
    logger.info('api_before_request')
    logger.info('request log_uuid:{}'.format(g.log_uuid))
    print_logs()

    dev_host_list = ['0.0.0.0', 'localhost']
    open_api_list = ['/api/open_exec', '/api/open_cicd']
    white_list = ['/api/login', '/api/auth', '/api/tourist', '/api/platform_conf']

    if request.path in white_list:
        return

    if '/api' in request.path:
        token = request.headers.get('token', '')
        logger.info(f'headers token -> {token}')

        # TODO 开发环境忽略鉴权
        if (request.host.split(':')[0] in dev_host_list) or (request.path in open_api_list):
            print('=== dev host ===')
            print(request.host.split(':')[0])
            print('=== open api ===')
            print(request.path)
            user = Admin.query.get(1)
            if not user:
                g.app_user = type('A', (object,), {"id": 1, "username": "admin"})
            else:
                g.app_user = user

            # return check_project_auth()
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
