# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_env.models import TestEnv
from app.models.test_logs.models import TestLogs
from app.models.test_case_scenario.models import TestCaseScenario
from common.libs.StringIOLog import StringIOLog

executor = ThreadPoolExecutor(10)


class CaseReqTestApi(MethodView):
    """
    test send
    """

    def post(self):
        data = request.get_json()
        method = data.get('method')
        base_url = data.get('base_url')
        url = data.get('url')
        headers = data.get('headers', {})
        req_type = data.get('req_type')
        body = data.get('body', {})

        send = {
            "url": base_url + url if base_url else url,
            "headers": headers,
            req_type: body
        }

        if req_type not in ["params", "data", "json"]:
            return api_result(code=400, message='req_type 应该为:{}'.format(["params", "data", "json"]))

        try:
            if hasattr(requests, method):
                response = getattr(requests, method)(**send, verify=False)
                data = {
                    "response": response.json(),
                    "response_headers": dict(response.headers)
                }
                return api_result(code=200, message='操作成功', data=data)
            else:
                return api_result(code=400, message='请求方式:{}不存在'.format(method))
        except BaseException as e:
            return api_result(code=400, message='请求方式失败:{}'.format(str(e)))


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
            "base_url_id": 1
        }

        场景执行
        {
            "execute_id": 3,
            "execute_type": "scenario",
            "data_driven": false
            "base_url_id": 1
        }
        :return:
        """
        execute_type_em = ("case", "scenario")
        data = request.get_json()
        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')
        data_driven = data.get('data_driven', False)
        base_url_id = data.get('base_url_id', None)

        send_test_case_list = []

        query_base_url = TestEnv.query.get(base_url_id)

        if not query_base_url:
            return api_result(code=400, message='base_url_id:{}不存在'.format(base_url_id))

        if execute_type not in execute_type_em:
            return api_result(code=400, message='execute_type:{}不存在'.format(execute_type))

        if execute_type == "case":
            result = query_case_zip(case_id=execute_id)
            if not result:
                return api_result(code=400, message='用例id:{}不存在'.format(execute_id))

            TestCase.query.get(execute_id).add_total_execution()
            send_test_case_list = [result]

        if execute_type == "scenario":
            result = TestCaseScenario.query.get(execute_id)
            if not result:
                return api_result(code=400, message='场景id:{}不存在'.format(execute_id))

            case_list = result.to_json().get('case_list')

            if not case_list:  # 防止手动修改数据导致,在场景创建的接口中有对应的校验
                return api_result(code=400, message='场景id:{}用例为空'.format(execute_id))

            send_test_case_list = []
            for case_id in case_list:
                result = query_case_zip(case_id=case_id)
                if not result:
                    return api_result(code=400, message='场景中,用例id:{}不存在'.format(case_id))
                send_test_case_list.append(result)

            update_case = TestCase.query.filter(TestCase.id.in_(case_list)).all()
            for u in update_case:
                u.add_total_execution()

        sio = StringIOLog()
        test_obj = {
            "base_url": query_base_url.env_url,
            "execute_type": execute_type,
            "case_list": send_test_case_list,
            "data_driven": data_driven,
            "sio": sio
        }
        main_test = MainTest(test_obj=test_obj)
        executor.submit(main_test.main)
        tl = TestLogs(
            log_type=execute_type,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        tl.save()
        return api_result(code=200, message='操作成功,请前往日志查看执行结果', data=[id(sio)])
