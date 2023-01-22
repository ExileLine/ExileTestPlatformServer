# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 11:26 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : auth_api.py
# @Software: PyCharm

from all_reference import *
from app.models.admin.models import Admin


class AuthApi(MethodView):
    """
    鉴权api
    GET: 验证token
    """

    def get(self):
        """验证token"""

        token = request.headers.get('token', '')  # 提取token
        user = R.get(f'token:{token}')
        if not user:
            return api_result(code=UNAUTHORIZED, message=f'token失效:{token}')

        user_id = R.get(user)  # 通过手机号或其他字段获取用户id  // redis命令: get yyx
        user = Admin.query.get(user_id)  # 通过id查询用户->获取用户对象
        user_obj = user.to_json()
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=user_obj)
