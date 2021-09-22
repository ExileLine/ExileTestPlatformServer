# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from app.models.test_case_scenario.models import TestCaseScenario
from common.libs.StringIOLog import sio

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
        """
        用例执行

        用例执行
        {
            "execute_id": 14,
            "execute_type": "case",
            "data_driven": False
        }

        场景执行
        {
            "execute_id": 3,
            "execute_type": "scenario",
            "data_driven": false
        }
        :return:
        """
        execute_type_em = ("case", "scenario")
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')
        data_driven = data.get('data_driven', False)

        send_test_case_list = []

        if execute_type not in execute_type_em:
            return api_result(code=400, message='execute_type:{}不存在'.format(execute_type))

        if execute_type == "case":
            result = query_case_zip(case_id=execute_id)
            if not result:
                return api_result(code=400, message='用例id:{}不存在'.format(execute_id))
            send_test_case_list = [result]

        if execute_type == "scenario":
            result = TestCaseScenario.query.get(execute_id)
            if not result:
                return api_result(code=400, message='场景id:{}不存在'.format(execute_id))

            case_list = result.to_json().get('case_list')
            send_test_case_list = [query_case_zip(case_id=case_id) for case_id in case_list]

        test_obj = {
            "case_list": send_test_case_list,
            "data_driven": data_driven
        }
        logger.info('=== stringio init ===')
        sio.get_stringio()
        main_test = MainTest(test_obj=test_obj)
        executor.submit(main_test.main)
        return api_result(code=200, message='操作成功,请前往日志查看执行结果')
