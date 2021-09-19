# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 1:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : user_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin


class TouristApi(MethodView):
    """
    游客api
    GET: 获取游客账号密码
    """

    def get(self):
        """获取游客账号密码"""

        user_ip = request.remote_addr

        query_tourist = R.get(user_ip)

        if query_tourist:
            return api_result(code=200, message='操作成功', data=json.loads(query_tourist))

        code = str(Admin.query.count() + 1).zfill(5)
        username = "user_{}".format(code)
        password = shortuuid.uuid()[0:6]
        query_user = Admin.query.filter_by(username=username).first()
        if query_user:
            username = "user_{}".format(code)

        new_admin = Admin(
            username=username,
            password=password,
            phone=None,
            mail=None,
            code=code,
            creator='shell',
            creator_id='0',
            remark='游客')
        new_admin.save()

        tourist_obj = {
            "username": username,
            "password": password
        }

        R.set(user_ip, json.dumps(tourist_obj))
        return api_result(code=200, message='操作成功', data=tourist_obj)
