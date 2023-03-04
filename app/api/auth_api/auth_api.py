# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 11:26 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : auth_api.py
# @Software: PyCharm

from all_reference import *


class AuthApi(MethodView):
    """
    鉴权api
    GET: 验证token
    """

    def get(self):
        """验证token"""

        token = request.headers.get('token', '')
        user = Token.get_user_info(token)
        if not user:
            return api_result(code=UNAUTHORIZED, message=f'token失效:{token}')
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=user)
