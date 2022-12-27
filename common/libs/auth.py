# -*- coding: utf-8 -*-
# @Time    : 2021/5/21 下午3:11
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : auth.py
# @Software: PyCharm

import json
import uuid

from flask import g
from loguru import logger

from common.libs.db import project_db, R
from common.libs.customException import method_view_ab_code as ab_code
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

    def gen_token(self):
        """
        生成token
        :return:
        """

        token = str(uuid.uuid1()).replace('-', self.mix)
        self.token = token
        return token

    def set_token(self, user):
        """
        缓存token
        :param user:
        :return:
        """

        self.gen_token()
        R.hset(name=f'user:{user}', mapping={"token": self.token})
        R.set(f'token:{self.token}', user)
        R.expire('user:{}'.format(user), 3600 * 24 * 30)
        R.expire(f'token:{self.token}', 3600 * 24 * 30)

    @classmethod
    def del_token(cls, token):
        """删除token"""

        """
        通过token查找user
        Input:
            get token:05885a4aYYxa18aYYx11ebYYxa1f9YYxacde48001122
        Output:
            yangyuexiong
            
        
        获取token
        Input:
            hget user:yangyuexiong token
        Output:
            05885a4aYYxa18aYYx11ebYYxa1f9YYxacde48001122
        """

        user = R.get(f'token:{token}')
        kv = f'user:{user}'
        user_token = R.hget(kv, 'token')

        """
        删除
        del yangyuexiong
        del user:yangyuexiong
        del token:13894378YYxa19bYYx11ebYYxa996YYxacde48001122
        """
        if user and user_token:
            R.delete(user)
            R.delete(kv, 'token')
            R.delete(f'token:{user_token}')
            return True
        else:
            return False

    def check_token(self, user, user_id):
        """
        检验token
        :param user:
        :param user_id:
        :return:
        """

        """
        Input:
            hget user:yangyuexiong token
            
        Output:
            05885a4aYYxa18aYYx11ebYYxa1f9YYxacde48001122
        """
        kv = f'user:{user}'
        user_token = R.hget(kv, 'token')
        if user_token:
            self.del_token(token=user_token)  # 删除旧token

        self.set_token(user=user)  # 生成新的token
        R.set(user, user_id, 3600 * 24 * 30)  # 用户(手机,名称等):id


def check_user(token, model):
    """

    :param token: token
    :param model: 用户模型类
    :return:
    """
    # 通过token获取手机号或者username
    # redis命令: get token:7d86561d3742e605e4c0ee42111995cd
    user = R.get('token:{}'.format(token))
    if not user:  # token错误或者失效
        g.app_user = None
        ab_code(401)
    else:
        user_id = R.get(user)  # 通过手机号或其他字段获取用户id  // redis命令: get yyx
        user = model.query.get(user_id)  # 通过id查询用户->获取用户对象
        g.app_user = user  # 创建全局对象


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
    """
    [redis]
    REDIS_HOST = localhost
    REDIS_PORT = 6379
    REDIS_PWD = 123456
    REDIS_DB = 1
    DECODE_RESPONSES = True
    """

    t = Token()
    t.check_token(user='yangyuexiong', user_id=33)
    print(t.token)
