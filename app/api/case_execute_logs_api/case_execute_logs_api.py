# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 1:27 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_execute_logs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class CaseExecuteLogsApi(MethodView):
    """
    用例/场景
    GET: 日志明细
    POST: 最新日志明细
    """

    def get(self, redis_key):
        """日志明细"""

        result = R.get(redis_key)
        if not result:
            return api_result(code=400, message='暂无日志', data={})
        else:
            data = json.loads(result)
            return api_result(code=200, message='操作成功', data=data)

    def post(self):
        """最新日志明细"""
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')

        if execute_id and execute_type:
            current_get_dict = gen_redis_first_logs(execute_id=execute_id)
            key = current_get_dict.get(execute_type)
            if not key:
                return api_result(code=400, message=f'执行类型错误:{execute_type}')

            result = R.get(key)
            if not result:
                return api_result(code=400, message='暂无日志', data={})

            return api_result(code=200, message='操作成功', data=json.loads(result))


class CaseExecuteLogsPageApi(MethodView):
    """
    执行日志分页模糊查询
    """

    def post(self):
        """
        执行日志分页模糊查询
        :return:
        """
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_name = data.get('execute_name')
        trigger_type = data.get('trigger_type')
        execute_type = data.get('execute_type')
        execute_status = data.get('execute_status')
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_execute_logs  
        WHERE 
        and execute_name LIKE"%B1%" 
        and execute_id = "execute_id" 
        and execute_type = "execute_type"  
        and creator_id = "creator_id" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "execute_id": execute_id,
            "trigger_type": trigger_type,
            "execute_type": execute_type,
            "execute_status": execute_status,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestExecuteLogs,
            field_list=['execute_name'],
            query_list=[execute_name],
            where_dict=where_dict,
            field_order_by='create_time',
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
