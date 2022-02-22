# -*- coding: utf-8 -*-
# @Time    : 2021/12/9 4:27 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : demo_api.py
# @Software: PyCharm

from all_reference import *


class DemoApi(MethodView):
    """
    demo api
    """

    def get(self):
        return api_result(code=200)

    def post(self):
        return api_result(code=200)

    def put(self):
        return api_result(code=200)

    def delete(self):
        return api_result(code=200)


class TestApi(MethodView):
    """
    test api
    """

    def get(self):
        return api_result(code=200, message='test api', data=True)
