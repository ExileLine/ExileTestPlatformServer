# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from app.all_reference import *

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

        data = request.get_json()
        case_id = data.get('case_id')
        result = query_case_zip(case_id=case_id)
        if not result:
            return api_result(code=400, message='用例id:{}不存在'.format(case_id))

        cdr = CaseDrivenResult(case=result)
        executor.submit(cdr.main)
        return api_result(code=200, message='操作成功,请前往日志查看执行结果')
