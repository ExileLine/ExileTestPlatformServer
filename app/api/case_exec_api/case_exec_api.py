# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from app.models.test_case_scenario.models import TestCaseScenario


executor = ThreadPoolExecutor(10)


class CaseExecApi(MethodView):
    """
    用例执行Api
    GET:
    POST: 用例执行
    PUT:
    DELETE:
    """

    def post(self):
        """用例执行"""
        # TODO 用例场景执行
        execute_type_em = ("case", "scenario")
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')

        if execute_type not in execute_type_em:
            return api_result(code=400, message='execute_type:{}不存在'.format(execute_type))

        if execute_type == "case":
            result = query_case_zip(case_id=execute_id)
            if not result:
                return api_result(code=400, message='用例id:{}不存在'.format(execute_id))

        if execute_type == "scenario":
            result = TestCaseScenario.query.get(id=execute_id)
            if not result:
                return api_result(code=400, message='场景id:{}不存在'.format(execute_id))

        cdr = CaseDrivenResult(case=result)
        executor.submit(cdr.main)
        return api_result(code=200, message='操作成功,请前往日志查看执行结果')
