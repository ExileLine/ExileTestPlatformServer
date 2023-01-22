# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:05 下午
# @Author  : yangyuexiong
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

    try:
        main = db_ping_dict.get(db_type).get('class')(**db_connection)
        print(main)
        func = db_ping_dict.get(db_type).get('func')
        print(func)
        getattr(main, func)()
        return True, 'Ping成功'
    except BaseException as e:
        print(str(e))
        return False, 'db 连接失败，请检查配置'


def case_db_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        db_type = data.get('db_type')

        if str(db_type).lower() not in db_list:
            return api_result(code=BUSINESS_ERROR, message=f'暂未支持: {db_type} 数据库')

        return func(*args, **kwargs)

    return wrapper


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
            return api_result(code=NO_DATA, message='数据库不存在')

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_db.to_json())

    @case_db_decorator
    def post(self):
        """db新增"""

        data = request.get_json()
        name = data.get('name')
        db_type = data.get('db_type')
        db_connection = data.get('db_connection')
        remark = data.get('remark')

        query_var = TestDatabases.query.filter_by(name=name, is_deleted=0).first()
        if query_var:
            return api_result(code=UNIQUE_ERROR, message=f'数据库名称: {name} 已存在')

        new_db = TestDatabases(
            name=name,
            db_type=db_type,
            db_connection=db_connection,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_db.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    @case_db_decorator
    def put(self):
        """db编辑"""

        data = request.get_json()
        db_id = data.get('id')
        name = data.get('name')
        db_type = data.get('db_type')
        db_connection = data.get('db_connection')
        remark = data.get('remark')

        query_db = TestDatabases.query.get(db_id)
        if not query_db:
            return api_result(code=NO_DATA, message='数据库不存在')

        query_db_filter = TestDatabases.query.filter_by(name=name, is_deleted=0).first()
        if query_db_filter and query_db.to_json().get('name') != name:
            return api_result(code=UNIQUE_ERROR, message=f'数据库名称: {name} 已存在')

        query_db.name = name
        query_db.db_type = db_type
        query_db.db_connection = db_connection
        query_db.remark = remark
        query_db.modifier = g.app_user.username
        query_db.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """db删除"""

        data = request.get_json()
        db_id = data.get('id')

        query_db = TestDatabases.query.get(db_id)
        if not query_db:
            return api_result(code=NO_DATA, message='数据库不存在')

        query_db.modifier_id = g.app_user.id
        query_db.modifier = g.app_user.username
        query_db.delete()
        return api_result(code=DEL_SUCCESS, message='删除成功')


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
        creator_id = data.get('creator_id')
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
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestDatabases,
            field_list=['name'],
            query_list=[name],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)


class CaseDBPingApi(MethodView):
    """
    db ping api
    """

    def get(self, db_id):
        """db ping"""

        query_db = TestDatabases.query.get(db_id)
        if not query_db:
            return api_result(code=NO_DATA, message='数据库不存在')

        db_type = query_db.to_json().get('db_type', {})
        if db_type not in db_list:
            return api_result(code=BUSINESS_ERROR, message=f'暂未支持: {db_type} 数据库')

        db_connection = query_db.to_json().get('db_connection', {})
        print(db_connection)
        if db_type == 'sqlserver':
            db_connection = {
                "server": f"{db_connection['host']}:{db_connection['port']}",
                "user": db_connection['user'],
                "password": db_connection['password']
            }
            print(db_connection)
        _bool, _result = db_ping(db_type=db_type, db_connection=db_connection)

        return api_result(code=SUCCESS if _bool else BUSINESS_ERROR, message=_result, data=_result)
