# -*- coding: utf-8 -*-
# @Time    : 2021/10/14 1:27 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_execute_logs_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class LatestLogsApi(MethodView):
    """最新10条日志"""

    def post(self):
        """10"""

        data = request.get_json()
        project_id = data.get('project_id')
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')
        query_10 = TestExecuteLogs.query.filter_by(
            project_id=project_id,
            execute_id=execute_id,
            execute_type=execute_type
        ).order_by(TestExecuteLogs.id.desc()).limit(10).all()

        if not query_10:
            return api_result(code=NO_DATA, message='暂无日志')

        if execute_type == "ui_case":
            ui_case = []
            for q in query_10:
                if R.get(q.redis_key):
                    ui_case.append(json.loads(R.get(q.redis_key)))

            if not ui_case:
                return api_result(code=NO_DATA, message='暂无日志(日志仅保存7天)')

            return api_result(code=POST_SUCCESS, message=f"操作成功: {len(ui_case)} 条", data=ui_case)

        else:  # api case
            case_logs = []
            scenario_logs = []
            for q in query_10:
                if R.get(q.redis_key):
                    case_logs += json.loads(R.get(q.redis_key)).get('case_logs')
                    scenario_logs += json.loads(R.get(q.redis_key)).get('scenario_logs')

            if not case_logs and not scenario_logs:
                return api_result(code=NO_DATA, message='暂无日志(日志仅保存7天)')

            result = {
                "case_logs": case_logs,
                "scenario_logs": scenario_logs
            }
            return api_result(code=POST_SUCCESS, message=f"操作成功: {len(case_logs)} 条", data=result)


class CaseExecuteLogsApi(MethodView):
    """
    用例/场景最新日志
    GET: 指定日志明细
    POST: 最新日志明细
    """

    def get(self, redis_key):
        """指定日志明细"""

        result = R.get(redis_key)
        if not result:
            return api_result(code=NO_DATA, message='暂无日志(日志仅保存7天)', data={})
        else:
            data = json.loads(result)
            return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=data)

    def post(self):
        """最新日志明细"""

        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')
        logs_key = GlobalsDict.redis_first_logs_dict(execute_id=execute_id)
        redis_key = logs_key.get(execute_type)
        if not redis_key:
            return api_result(code=NO_DATA, message=f'执行类型: {execute_type} 不存在')

        result = R.get(redis_key)
        if not result:
            return api_result(code=NO_DATA, message='暂无日志(日志仅保存7天)', data={})

        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=json.loads(result))


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
        return api_result(code=200, message=SUCCESS_MESSAGE, data=result_data)
