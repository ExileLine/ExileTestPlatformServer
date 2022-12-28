# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午3:11
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : auth.py
# @Software: PyCharm

import json
import uuid

from loguru import logger

from common.libs.db import project_db, R
from app.models.admin.models import Admin, Role, Permission, MidAdminAndRole, MidPermissionAndRole, ApiResource

"""
test:

import redis

redis_obj = {
    # 'host': conf.get('redis', 'REDIS_HOST'),
    # 'port': conf.get('redis', 'REDIS_PORT'),
    # 'password': conf.get('redis', 'REDIS_PWD'),
    # 'decode_responses': conf.getboolean('redis', 'DECODE_RESPONSES'),
    # 'db': conf.getint('redis', 'REDIS_DB')

    'host': 'localhost',
    'port': 6379,
    'password': 123456,
    'decode_responses': True,
    'db': 10
}
POOL = redis.ConnectionPool(**redis_obj)
R = redis.Redis(connection_pool=POOL)

"""


class Token:
    """
    Token
    """

    def __init__(self):
        self.token = None
        self.mix = "Y"
        self.timeout = 3600 * 24 * 30

    def gen_token(self):
        """
        生成token
        :return:
        """

        token = str(uuid.uuid1()).replace('-', self.mix)
        self.token = token
        return token

    def set_token(self, user_info: dict):
        """
        缓存token
        :param user_info:
        :return:

        1.生成:token
        2.写入:token
        3.写入:user_info

        Redis command
            Input:
                hset user:1-admin "token" "d9d116fcY8671Y11edYa559Yacde48001122"

            Input:
                hset token:d9d116fcY8671Y11edYa559Yacde48001122 "user_info" '{"id":1,"username":"admin"}'
        """

        self.gen_token()
        user_id = user_info.get('id')
        username = user_info.get('username')
        token_key = f"user:{user_id}-{username}"
        user_key = f"token:{self.token}"
        R.hset(name=token_key, mapping={"token": self.token})
        R.hset(name=user_key, mapping={"user_info": json.dumps(user_info, ensure_ascii=False)})
        R.expire(token_key, self.timeout)
        R.expire(user_key, self.timeout)

    @classmethod
    def del_cache(cls, token):
        """
        删除缓存
        :param token:
        :return:

        1.通过token查找user_info
        2.删除token
        3.删除user_info

        Redis command
            Input:
                hget token:d9d116fcY8671Y11edYa559Yacde48001122 user_info

            Output:
                {"id":"1","username":"admin"...}

            Input:
                del user:1-admin

            Input:
                del token:d9d116fcY8671Y11edYa559Yacde48001122

        """

        user_key = f"token:{token}"
        query_user_info = R.hget(user_key, 'user_info')
        if query_user_info:
            user_info = json.loads(query_user_info)
            user_id = user_info.get('id')
            username = user_info.get('username')
            token_key = f"user:{user_id}-{username}"
            R.delete(user_key)
            R.delete(token_key)

    def refresh_cache(self, user_info: dict):
        """
        刷新缓存
        :param user_info:
        :return:

        1.通过用户id-用户名称获取token
        2.删除旧的token与user_info
        3.更新写入token与user_info

        Redis command
            Input:
                hget user:1-admin token

            Output:
                d9d116fcY8671Y11edYa559Yacde48001122
        """

        user_id = user_info.get('id')
        username = user_info.get('username')
        token_key = f'user:{user_id}-{username}'
        old_token = R.hget(token_key, 'token')
        if old_token:
            self.del_cache(token=old_token)  # 删除旧token

        self.set_token(user_info=user_info)  # 生成新的token并写入Redis

    @staticmethod
    def get_user_info(token):
        """
        通过token或用户信息
        :param token:
        :return:
        """

        query_token = R.hget(f"token:{token}", 'user_info')
        if query_token:
            user_info = json.loads(query_token)
            return user_info
        else:
            return None


class AdminRefreshCache:
    """获取用户角色权限并Redis缓存"""

    admin_id_list = []

    @classmethod
    def query_admin_permission_info(cls, admin_id):
        """
        获取用户角色权限并Redis缓存
        :param admin_id:
        :return:
        """
        query_admin = """
            SELECT 
            id,username,phone,mail,code,creator,modifier,create_time,update_time,is_deleted,status,remark 
            FROM ec_crm_admin 
            WHERE is_deleted=0 and id={};""".format(admin_id)
        admin_res = project_db.select(query_admin, only=True)
        logger.success(query_admin)
        # print(admin_res)

        if admin_res:
            query_role = """
            SELECT 
            id,name,creator,modifier,create_time,update_time,is_deleted,status,remark 
            FROM ec_crm_role 
            WHERE is_deleted=0 and id in (SELECT role_id FROM ec_crm_mid_admin_role WHERE admin_id={});""".format(
                admin_id)
            role_res = project_db.select(query_role)
            logger.success(query_role)
            # print(role_res)
            if role_res:
                role_id_list = [r_id.get('id') for r_id in role_res]
                # print(tuple(role_id_list))

                to_role_id_list = str(tuple(role_id_list)).replace(',', '') if len(role_id_list) == 1 else tuple(
                    role_id_list)
                # print(to_role_id_list)

                query_permission = """
                SELECT 
                P.id,
                P.name,
                P.resource_id,
                P.resource_type,
                API.name,
                API.url,
                API.method,
                API.is_url_var,
                P.is_deleted,
                P.creator,
                P.modifier,
                P.create_time,
                P.update_time,
                P.remark,
                API.remark
                FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id  
                WHERE P.is_deleted=0 and P.id in (SELECT permission_id FROM ec_crm_mid_permission_role WHERE role_id in {});
                """.format(to_role_id_list)
                permission_res = project_db.select(query_permission)
                logger.success(query_permission)
                # print(permission_res)

                if permission_res:
                    url_list = []
                    url_is_var_list = []
                    url_tuple_list = []
                    url_is_var_tuple_list = []
                    route_list = []
                    other_list = []
                    for p in permission_res:
                        method = p.get('method')
                        url = p.get('url')
                        is_url_var = p.get('is_url_var')
                        resource_type = p.get('resource_type')
                        if resource_type == 'SERVER_API':
                            t = (method, url)
                            if bool(is_url_var):
                                url_is_var_list.append(url)
                                url_is_var_tuple_list.append(t)
                            else:
                                url_list.append(url)
                                url_tuple_list.append(t)
                        elif resource_type == 'WEB_ROUTE':
                            route_list.append(url)
                        else:
                            other_list.append(url)

                    admin_res['role_list'] = role_res
                    admin_res['role_id_list'] = role_id_list
                    admin_res['permission_list'] = permission_res
                    admin_res['url_list'] = url_list
                    admin_res['url_is_var_list'] = url_is_var_list
                    admin_res['url_tuple_list'] = url_tuple_list
                    admin_res['url_is_var_tuple_list'] = url_is_var_tuple_list
                    admin_res['route_list'] = route_list
                    admin_res['other_list'] = other_list

                    redis_key = 'auth:{}'.format(admin_id)
                    R.set(redis_key, json.dumps(admin_res))
                    return admin_res
                else:
                    return admin_res
            else:
                return admin_res
        else:
            return admin_res

    @classmethod
    def query_admin_id_from_role(cls, role_id):
        """
        查询包含角色的所有用户
        :param role_id:
        :return:
        """
        cls.admin_id_list = [m.admin_id for m in MidAdminAndRole.query.filter_by(role_id=role_id).all()]

    @classmethod
    def query_admin_id_from_permission(cls, permission_id):
        """
        查询包含权限的所有用户
        :param permission_id:
        :return:
        """
        role_id_list = [m.role_id for m in MidPermissionAndRole.query.filter_by(permission_id=permission_id).all()]
        cls.admin_id_list = [
            m.admin_id for m in MidAdminAndRole.query.filter(MidAdminAndRole.role_id.in_(role_id_list)).all()
        ]

    @classmethod
    def query_admin_id_from_api_resource(cls, api_resource_id):
        """
        查询包含api_resource的所有用户
        :param api_resource_id:
        :return:
        """
        sql = """SELECT P.id 
        FROM ec_crm_permission P LEFT JOIN ec_crm_api_resource API ON P.resource_id=API.id  
        WHERE API.id={};""".format(api_resource_id)
        result = project_db.select(sql, only=True)
        permission_id = result.get('id')
        role_id_list = [role.id for role in MidPermissionAndRole.query.filter_by(permission_id=permission_id).all()]
        cls.admin_id_list = [
            m.admin_id for m in MidAdminAndRole.query.filter(MidAdminAndRole.role_id.in_(role_id_list)).all()
        ]

    @classmethod
    def refresh(cls, *args):
        """
        刷新缓存
        :param args:
        :return:
        """
        logger.success('===refresh===')

        if args:
            [cls.query_admin_permission_info(admin_id=admin_id) for admin_id in args]
        else:
            [cls.query_admin_permission_info(admin_id=admin_id) for admin_id in cls.admin_id_list]


if __name__ == '__main__':
    t = Token()
    d = {
        "id": 1,
        "is_deleted": 0,
        "code": "00001",
        "status": 1,
        "login_type": None,
        "username": "admin",
        "creator": "shell",
        "create_time": "2021-11-11 11:15:29",
        "nickname": "yyx",
        "creator_id": 0,
        "modifier": "admin",
        "create_timestamp": 1636600147,
        "phone": "15013038818",
        "modifier_id": 1,
        "update_time": "2022-08-17 17:53:07",
        "mail": "yang@126.com",
        "remark": "游客",
        "update_timestamp": 1660729764
    }
    t.refresh_cache(user_info=d)
    print(t.token)
    user_info = t.get_user_info(token=t.token)
    print(user_info)
