# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 1:37 下午
# @Author  : ShaHeTop-Almighty-ares
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
        data = request.get_json()
        if check_keys(data, 'username', 'password'):
            username = data.get('username', '')
            password = data.get('password', '')
            admin = Admin.query.filter_by(username=username, is_deleted=0).first()

            if not admin:
                return api_result(code=200, message='用户不存在或被禁用')

            if not admin.check_password(password):
                return api_result(code=200, message='账号或密码错误')

            """
            检查是否存在旧token并且生成新token覆盖旧token,或创建一个新的token。然后添加至返回值。
            """
            admin_obj = admin.to_json(*['_password'])
            t = Token()
            t.check_token(user=admin.username, user_id=admin.id)
            admin_obj['token'] = t.token
            return api_result(code=200, message='登录成功', data=admin_obj)

        else:
            ab_code_2(1000001)

    def delete(self):
        # print(request.headers.get('Token'))
        Token.del_token(request.headers.get('Token'))
        return api_result(code=204, message='退出成功')
