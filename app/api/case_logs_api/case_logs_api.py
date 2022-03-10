# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 12:48 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_logs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestLogs


class CaseLogsPageApi(MethodView):
    """
    操作日志分页模糊查询
    """

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_logs  
        WHERE 
        creator_id = 1 
        and is_deleted=0
        and creator LIKE"%B1%" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "creator_id": user_id
        }

        result_data = general_query(
            model=TestLogs,
            field_list=['creator'],
            query_list=[username],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
