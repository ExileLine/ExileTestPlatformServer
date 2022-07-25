# -*- coding: utf-8 -*-
# @Time    : 2021/12/9 4:27 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : demo_api.py
# @Software: PyCharm


from all_reference import *
from tasks.task01 import send_email
from tasks.task02 import send_msg


class TestApi(MethodView):
    """
    test api
    """

    def get(self):
        return api_result(code=200, message='GET: test api', data=True)

    def post(self):
        data = request.get_json()
        print(data)
        return api_result(code=200, message='POST: test api', data=True)

    def delete(self):
        """1"""
        data = request.get_json()
        p1 = request.args.get('p1')
        p2 = request.args.get('p2')
        p3 = request.args.get('p3')
        p4 = request.args.get('p4')
        return api_result(code=204, message='DELETE: test api', data=[p1, p2, p3, p4, data])


class TestCeleryAsyncTaskApi(MethodView):
    """
    调试Celery异步任务
    GET: 触发
    """

    def get(self):
        """调试Celery异步任务"""
        results1 = send_email.delay('yyx123')
        results2 = send_msg.delay('yyx456')
        print(results1)
        print(results2)
        return api_result(code=200, message='调试Celery异步任务')
