# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:05 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_db_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case_config.models import TestDatabases

db_list = ["mysql", "redis"]


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
        db_id = data.get('db_id')
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

        query_db.is_deleted = query_db.id
        query_db.modifier = g.app_user.username
        query_db.modifier_id = g.app_user.id
        db.session.commit()
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
        is_deleted = data.get('is_deleted', False)
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_test_databases  
        WHERE 
        id LIKE"%%" 
        and name LIKE"%yyx%" 
        and db_type LIKE"%sql%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestDatabases,
            field_list=['id', 'name', 'db_type'],
            query_list=[db_id, name, db_type],
            is_deleted=is_deleted,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
