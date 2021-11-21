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
            creator='shell',
            creator_id='0',
            remark='游客')
        new_admin.set_code()
        new_admin.save()

        tourist_obj = {
            "username": username,
            "password": password
        }

        R.set(user_ip, json.dumps(tourist_obj))
        return api_result(code=200, message='操作成功', data=tourist_obj)


class UserApi(MethodView):
    """
    用户信息 Api
    """

    def get(self, user_id):
        """1"""
        return api_result(code=200, message="user api")


class UserPasswordApi(MethodView):
    """
    用户密码 Api
    POST: 修改密码
    PUT: 重置密码
    """

    def post(self):
        """修改密码"""

        data = request.get_json()
        user_id = data.get('user_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        raw_password = data.get('raw_password')

        user = Admin.query.get(user_id)

        if not user:
            return api_result(code=400, message="用户:{} 不存在".format(user_id))

        if not user.check_password(old_password):
            return api_result(code=400, message="旧密码错误")

        if new_password != raw_password:
            return api_result(code=400, message="新密码不一致")

        user.password = new_password
        user.modifier = g.app_user.username
        user.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=201, message='操作成功')

    def put(self):
        """重置密码"""

        data = request.get_json()
        user_id = data.get('user_id')

        user = Admin.query.get(user_id)

        if not user:
            return api_result(code=400, message="用户:{} 不存在".format(user_id))

        if g.app_user.id != 1:
            return api_result(code=400, message="非管理员,无法重置!")

        new_password = shortuuid.uuid()[0:6]
        user.password = new_password
        user.modifier = g.app_user.username
        user.modifier_id = g.app_user.id
        db.session.commit()
        # TODO 邮件发送,短信
        return api_result(code=203, message='操作成功', data=[new_password])


class UserProfileApi(MethodView):
    """
    用户信息 Api
    GET: 获取用户信息
    PUT: 编辑用户信息
    """

    def get(self, user_id):
        """获取用户信息"""

        user = Admin.query.get(user_id)

        if not user:
            return api_result(code=400, message="用户:{} 不存在".format(user_id))
        return api_result(code=200, message="操作成功", data=user.to_json(*["_password"]))

    def put(self):
        """编辑用户信息"""

        data = request.get_json()
        user_id = data.get('user_id')
        nickname = data.get('nickname')
        phone = data.get('phone')
        mail = data.get('mail')

        user = Admin.query.get(user_id)

        if not user:
            return api_result(code=400, message="用户:{} 不存在".format(user_id))

        if user.id != g.app_user.id:
            return api_result(code=400, message="只能修改自己的用户信息")

        if not nickname:
            return api_result(code=400, message="昵称不能为空")

        user.nickname = nickname
        user.phone = phone
        user.mail = mail
        user.modifier = g.app_user.username
        user.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=203, message='操作成功')


class UserPageApi(MethodView):
    """
    user page api
    POST: 用户分页模糊查询
    """

    def post(self):
        """用例分页模糊查询"""

        data = request.get_json()
        user_id = data.get('user_id')
        code = data.get('code')
        username = data.get('username')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_auth_admin  
        WHERE 
        id LIKE"%%" 
        and username LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=Admin,
            field_list=['id', 'username', 'code'],
            query_list=[user_id, username, code],
            is_deleted=is_deleted,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)
