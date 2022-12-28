# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 1:37 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : login_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin


class LoginApi(MethodView):
    """
    login api
    POST: 登录
    DELETE: 退出
    """

    def post(self):
        """登录"""

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return api_result(code=REQUIRED, message='用户名、密码不能为空')

        admin = Admin.query.filter_by(username=username, is_deleted=0).first()

        if not admin:
            return api_result(code=NO_DATA, message='用户不存在或被禁用')

        if not admin.check_password(password):
            return api_result(code=BUSINESS_ERROR, message='密码错误')

        """
        检查是否存在旧token并且生成新token覆盖旧token,或创建一个新的token。然后添加至返回值。
        """
        admin_obj = admin.to_json()
        t = Token()
        t.check_token(user=admin.username, user_id=admin.id)
        admin_obj['token'] = t.token
        return api_result(code=SUCCESS, message='登录成功', data=admin_obj)

    def delete(self):
        """退出"""

        token = request.headers.get('token')
        Token.del_token(token)
        return api_result(code=DEL_SUCCESS, message='退出成功', data={"token": token})
