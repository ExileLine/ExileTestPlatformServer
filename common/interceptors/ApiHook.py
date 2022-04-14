# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

import time

import shortuuid
from loguru import logger
from flask import request, g

from app.models.admin.models import Admin
from common.libs.public_func import print_logs
from common.libs.auth import check_user
from common.libs.customException import method_view_ab_code as ab_code


def api_before_request():
    g.log_uuid = "{}_{}".format(str(int(time.time())), shortuuid.uuid())
    logger.info('api_before_request')
    logger.info('request log_uuid:{}'.format(g.log_uuid))
    print_logs()

    dev_host_list = ['0.0.0.0', 'localhost']
    open_api_list = ['/api/open_exec']
    white_list = ['/api/login', '/api/auth', '/api/tourist', '/api/platform_conf', '/scheduler', '/jobs']

    if request.path in white_list:
        return

    if '/api' in request.path:
        is_token = request.headers.get('Token', None)  # 是否存在token
        logger.info('headers是否存在key:token -> {}'.format(is_token))

        # TODO 开发环境忽略鉴权
        if (request.host.split(':')[0] in dev_host_list) or (request.path in open_api_list):
            print('=== dev host ===')
            print(request.host.split(':')[0])
            print('=== open api ===')
            print(request.path)
            user = Admin.query.get(1)
            g.app_user = user
            return

        if not is_token:
            ab_code(401)

        token = request.headers.get('token', '')  # 提取token
        logger.info('{}'.format(token))
        check_user(token=token, model=Admin)  # 通过 token 查找 user,将 user 存放在全局 g 对象中


def api_after_request(response):
    logger.info('after_request_api')
    logger.info('response log_uuid:{}'.format(g.log_uuid))
    logger.info('=== response ===')
    response.headers['log_uuid'] = g.log_uuid
    return response
