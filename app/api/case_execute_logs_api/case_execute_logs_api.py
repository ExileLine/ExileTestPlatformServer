# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 1:27 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_execute_logs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class CaseExecuteLogsPageApi(MethodView):
    """
    执行日志分页模糊查询
    """

    def post(self):
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_name = data.get('execute_name')
        execute_type = data.get('execute_type')
        creator = data.get('creator')
        creator_id = data.get('creator_id')
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_test_execute_logs  
        WHERE 
        execute_id LIKE"%%" 
        and execute_name LIKE"%B1%" 
        and execute_type LIKE"%B1%" 
        and creator LIKE"%B1%" 
        and creator_id LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestExecuteLogs,
            field_list=['execute_id', 'execute_name', 'execute_type', 'creator', 'creator_id'],
            query_list=[execute_id, execute_name, execute_type, creator, creator_id],
            is_deleted=False,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
