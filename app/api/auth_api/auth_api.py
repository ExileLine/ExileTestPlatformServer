# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 11:26 上午
# @Author  : ShaHeTop-Almighty-ares
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
            return api_result(code=400, message=f'token失效:{token}', data={})

        user_id = R.get(user)  # 通过手机号或其他字段获取用户id  // redis命令: get yyx
        user = Admin.query.get(user_id)  # 通过id查询用户->获取用户对象
        return api_result(code=200, message='操作成功', data=user.to_json())