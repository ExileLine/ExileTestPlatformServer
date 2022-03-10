# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 1:27 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_execute_logs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class CaseExecuteLogsApi(MethodView):
    """
    用例/场景最新日志
    """

    def post(self):
        data = request.get_json()
        case_id = data.get('case_id')
        scenario_id = data.get('scenario_id')
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')

        if execute_id and execute_type:
            current_get_dict = gen_redis_first_logs(execute_id=execute_id)
            key = current_get_dict.get(execute_type)
            if not key:
                return api_result(code=400, message='执行类型错误')

            result = R.get(key)
            if not result:
                return api_result(code=200, message='操作成功', data={})

            return api_result(code=200, message='操作成功', data=json.loads(result))

        if case_id:
            query_case_logs = TestExecuteLogs.query.filter_by(execute_id=case_id).order_by(
                TestExecuteLogs.create_timestamp.desc()).first()
            if not query_case_logs:
                return api_result(code=200, message='操作成功', data={})

            case_logs_obj = query_case_logs.to_json()
            redis_key = case_logs_obj.get('redis_key')
            result = R.get(redis_key)
            if not result:
                return api_result(code=200, message='操作成功', data={})

            return api_result(code=200, message='操作成功', data=json.loads(result))

        if scenario_id:
            query_scenario_logs = TestExecuteLogs.query.filter_by(execute_id=scenario_id).order_by(
                TestExecuteLogs.create_timestamp.desc()).first()
            if not query_scenario_logs:
                return api_result(code=200, message='操作成功', data={})

            scenario_logs_obj = query_scenario_logs.to_json()
            redis_key = scenario_logs_obj.get('redis_key')
            result = R.get(redis_key)
            if not result:
                return api_result(code=200, message='操作成功', data={})

            return api_result(code=200, message='操作成功', data=json.loads(result))


class CaseExecuteLogsPageApi(MethodView):
    """
    执行日志分页模糊查询
    """

    def post(self):
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_name = data.get('execute_name')
        execute_type = data.get('execute_type')
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
            "execute_type": execute_type,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestExecuteLogs,
            field_list=['execute_name'],
            query_list=[execute_name],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
