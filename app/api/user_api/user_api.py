# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 1:45 下午
# @Author  : yangyuexiong
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

        # user_ip = request.remote_addr
        user_ip = request.headers.get('X-Forwarded-For', '0.0.0.0')
        print('===user_ip===', user_ip)
        query_tourist = R.get(user_ip)
        print('===query_tourist===', query_tourist)

        if query_tourist:
            return api_result(code=200, message='操作成功', data=json.loads(query_tourist))

        code = str(Admin.query.count() + 1).zfill(5)  # TODO
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
        """用户详情"""

        return api_result(code=SUCCESS, message="操作成功")

    def post(self):
        """创建用户"""

        data = request.get_json()
        username = data.get('username')
        nickname = data.get('nickname')
        mail = data.get('mail')
        phone = data.get('phone')
        password = data.get('password', '123456')

        if not username:
            return api_result(code=NO_DATA, message=f"用户名不能为空")

        if not mail:
            return api_result(code=NO_DATA, message=f"邮箱不能为空")

        query_admin = Admin.query.filter(or_(Admin.username == username, Admin.mail == mail)).first()
        if query_admin:
            if query_admin.username == username:
                return api_result(code=UNIQUE_ERROR, message=f"用户名: {username} 已存在")
            elif query_admin.mail == mail:
                return api_result(code=UNIQUE_ERROR, message=f"邮箱: {mail} 已存在")
            return api_result(code=UNIQUE_ERROR, message=f"用户名或邮箱已存在")

        new_admin = Admin(
            username=username,
            nickname=nickname,
            password=password,
            mail=mail,
            phone=phone,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_admin.set_code()
        new_admin.save()
        return api_result(code=POST_SUCCESS, message='操作成功')

    def put(self):
        """编辑用户信息"""

        data = request.get_json()
        user_id = data.get('id')
        nickname = data.get('nickname')
        phone = data.get('phone')
        mail = data.get('mail')

        user = Admin.query.get(user_id)

        if not user:
            return api_result(code=NO_DATA, message="用户不存在")

        if user.id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message="只能修改自己的用户信息")

        if not nickname:
            return api_result(code=BUSINESS_ERROR, message="昵称不能为空")

        user.nickname = nickname
        user.phone = phone
        user.mail = mail
        user.modifier = g.app_user.username
        user.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message='操作成功')

    def delete(self):
        """禁用用户信息"""

        data = request.get_json()
        user_id = data.get('id')
        status = data.get('status')
        query_admin = Admin.query.get(user_id)
        query_admin.status = status
        db.session.commit()
        return api_result(code=DEL_SUCCESS, message='操作成功')


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
        return api_result(code=200, message="操作成功", data=user.to_json())

    def post(self):
        """创建用户"""

        data = request.get_json()
        username = data.get('username')
        nickname = data.get('nickname')
        mail = data.get('mail')
        password = data.get('password', '123456')

        if not username:
            return api_result(code=400, message=f"用户名不能为空")

        if not mail:
            return api_result(code=400, message=f"邮箱不能为空")

        query_admin = Admin.query.filter(or_(Admin.username == username, Admin.mail == mail)).first()
        if query_admin:
            if query_admin.username == username:
                return api_result(code=400, message=f"用户名: {username} 已存在")
            elif query_admin.mail == mail:
                return api_result(code=400, message=f"邮箱: {mail} 已存在")
            return api_result(code=400, message=f"用户名或邮箱已存在")

        new_admin = Admin(
            username=username,
            nickname=nickname,
            password=password,
            mail=mail,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_admin.set_code()
        new_admin.save()
        return api_result(code=200, message='操作成功')

    def put(self):
        """编辑用户信息"""

        data = request.get_json()
        user_id = data.get('id')
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
        """用户分页模糊查询"""

        data = request.get_json()
        user_id = data.get('user_id')
        code = data.get('code')
        # phone = data.get('phone')
        username = data.get('username')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_auth_admin  
        WHERE 
        id = "id" 
        or username LIKE"%admin%" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": user_id,
        }

        result_data = general_query(
            model=Admin,
            field_list=['username', 'code'],
            query_list=[username, code],
            where_dict=where_dict,
            page=page,
            size=size
        )
        # records = result_data.get('records')
        # current_user = g.app_user.to_json()
        # records.pop(size - 1)
        # records.insert(0, current_user)
        return api_result(code=SUCCESS, message='操作成功', data=result_data)
