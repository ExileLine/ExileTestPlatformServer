# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from app.all_reference import *
from app.models.test_case.models import TestCase

executor = ThreadPoolExecutor(10)


def _case_exec(**kwargs):
    """1"""
    print('yyx')
    print(time.time())
    time.sleep(5)
    print(kwargs)
    print(time.time())


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
        executor.submit(_case_exec, **{"key": "val"})
        return api_result(code=200, message='操作成功', data=case)
