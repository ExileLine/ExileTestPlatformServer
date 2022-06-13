# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:05 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_db_api.py
# @Software: PyCharm

import redis

from all_reference import *
from common.libs.db import MyPyMysql, MyPostgreSql, MySqlServer
from app.models.test_case_db.models import TestDatabases

db_list = ("mysql", "redis", "postgresql", "sqlserver")

db_ping_dict = {
    "mysql": {
        "class": MyPyMysql,
        "func": "ping"
    },
    "redis": {
        "class": redis.Redis,
        "func": "ping"
    },
    "postgresql": {
        "class": MyPostgreSql,
        "func": "ping"
    },
    "sqlserver": {
        "class": MySqlServer,
        "func": "ping"
    }
}


def db_ping(db_type, db_connection):
    """
    db ping
    :param db_type: db类型
    :param db_connection: db连接信息
    :return:
    """

    if db_type not in db_list:
        return False, f'暂未支持：{db_type}'
    try:
        main = db_ping_dict.get(db_type).get('class')(**db_connection)
        func = db_ping_dict.get(db_type).get('func')
        getattr(main, func)()
        return True, 'Ping成功'
    except BaseException as e:
        return False, 'db 连接失败，请检查配置'


class CaseDBApi(MethodView):
    """
    用例关联 db api
    GET: db详情
    POST: db新增
    PUT: db编辑
    DELETE: db删除
    """

    def get(self, db_id):
        """db详情"""

        query_db = TestDatabases.query.get(db_id)

        if not query_db:
            return api_result(code=400, message='db_id:{}数据不存在'.format(db_id))

        return api_result(code=200, message='操作成功', data=query_db.to_json())

    def post(self):
        """db新增"""
        data = request.get_json()
        name = data.get('name')
        db_type = data.get('db_type')
        db_connection = data.get('db_connection')
        remark = data.get('remark')

        if str(db_type).lower() not in db_list:
            return api_result(code=400, message='不存在数据库类型:{}'.format(db_type))

        query_var = TestDatabases.query.filter_by(name=name).first()

        if query_var:
            return api_result(code=200, message='db名称:【{}】已存在'.format(name))

        new_mysql = TestDatabases(
            name=name,
            db_type=db_type,
            db_connection=db_connection,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_mysql.save()
        return api_result(code=201, message='创建成功')

    def put(self):
        """db编辑"""

        data = request.get_json()
        db_id = data.get('id')
        name = data.get('name')
        db_type = data.get('db_type')
        db_connection = data.get('db_connection')
        remark = data.get('remark')

        if str(db_type).lower() not in db_list:
            return api_result(code=400, message='不存在数据库类型:{}'.format(db_type))

        query_db_filter = TestDatabases.query.filter_by(name=name).first()
        query_db = TestDatabases.query.get(db_id)

        if query_db_filter and query_db.to_json().get('name') != name:
            return api_result(code=400, message='db名称:{} 已存在'.format(name))

        if query_db:
            query_db.name = name
            query_db.db_type = db_type
            query_db.db_connection = db_connection
            query_db.remark = remark
            query_db.modifier = g.app_user.username
            query_db.modifier_id = g.app_user.id
            db.session.commit()
            return api_result(code=203, message='编辑成功')
        else:
            return api_result(code=400, message='db_id:{}数据不存在'.format(db_id))

    def delete(self):
        """db删除"""

        data = request.get_json()
        db_id = data.get('db_id')

        query_db = TestDatabases.query.get(db_id)

        if not query_db:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(db_id))

        query_db.modifier_id = g.app_user.id
        query_db.modifier = g.app_user.username
        query_db.delete()
        return api_result(code=204, message='删除成功')


class CaseDBPageApi(MethodView):
    """
    case db page api
    POST: 用例关联 db 分页模糊查询
    """

    def post(self):
        """用例关联 db 分页模糊查询"""

        data = request.get_json()
        db_id = data.get('db_id')
        name = data.get('name')
        db_type = data.get('db_type')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_databases  
        WHERE 
        id = "id" 
        and name LIKE"%yyx%" 
        and db_type = "db_type" 
        and is_deleted = 0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": db_id,
            "db_type": db_type,
            "is_deleted": is_deleted
        }

        result_data = general_query(
            model=TestDatabases,
            field_list=['name'],
            query_list=[name],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)


class CaseDBPingApi(MethodView):
    """
    db ping api
    """

    def get(self, db_id):
        """db ping"""

        query_db = TestDatabases.query.get(db_id)

        if not query_db:
            return api_result(code=400, message='db_id:{}数据不存在'.format(db_id))

        db_type = query_db.to_json().get('db_type', {})
        db_connection = query_db.to_json().get('db_connection', {})
        _bool, _result = db_ping(db_type=db_type, db_connection=db_connection)

        return api_result(code=200 if _bool else 400, message=_result, data=_result)
