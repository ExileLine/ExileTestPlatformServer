# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

from loguru import logger
from flask import request, g

from app.api import api
from app.models.admin.models import Admin
from common.libs.public_func import print_logs
from common.libs.auth import check_user
from common.libs.customException import ab_code_2


@api.before_request
def before_request_api():
    logger.info('api_before_request')
    print_logs()

    white_list = ['/api/login']
    if request.path in white_list:
        return

    if '/api' in request.path:
        is_token = request.headers.get('Token', None)  # 是否存在token
        logger.info('headers是否存在key:token -> {}'.format(is_token))

        # TODO 开发阶段使用的万能鉴权
        if is_token == 'yangyuexiong':
            g.app_user = Admin.query.get(1)
            return

        if not is_token:
            ab_code_2(666)

        token = request.headers.get('token', '')  # 提取token
        logger.info('{}'.format(token))
        check_user(token=token, model=Admin)  # 通过 token 查找 user,将 user 存放在全局 g 对象中
