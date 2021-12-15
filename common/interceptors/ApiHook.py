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

from app.api import api
from app.models.admin.models import Admin
from common.libs.public_func import print_logs
from common.libs.auth import check_user
from common.libs.customException import method_view_ab_code as ab_code


@api.before_request
def before_request_api():
    g.log_uuid = "{}_{}".format(str(int(time.time())), shortuuid.uuid())
    logger.info('api_before_request')
    logger.info('request log_uuid:{}'.format(g.log_uuid))
    print_logs()

    white_list = ['/api/login']
    if request.path in white_list:
        return

    if '/api' in request.path:
        is_token = request.headers.get('Token', None)  # 是否存在token
        logger.info('headers是否存在key:token -> {}'.format(is_token))

        # TODO 开发阶段使用的万能鉴权
        if is_token == 'yangyuexiong':
            user = Admin.query.get(1)
            g.app_user = user
            return

        if not is_token:
            ab_code(401)

        token = request.headers.get('token', '')  # 提取token
        logger.info('{}'.format(token))
        check_user(token=token, model=Admin)  # 通过 token 查找 user,将 user 存放在全局 g 对象中


@api.after_request
def after_request_api(response):
    logger.info('after_request_api')
    logger.info('response log_uuid:{}'.format(g.log_uuid))
    logger.info('=== response ===')
    response.headers['log_uuid'] = g.log_uuid
    return response
