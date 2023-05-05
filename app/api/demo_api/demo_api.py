# -*- coding: utf-8 -*-
# @Time    : 2021/12/9 4:27 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : demo_api.py
# @Software: PyCharm


from all_reference import *
from tasks.task01 import send_email
from tasks.task02 import send_message
from tasks.task03 import test_context
from tasks.web_ui import web_ui


class TestApi(MethodView):
    """
    test api
    """

    def get(self):
        from common.libs.db import R, project_db

        data = {
            "redis_id": f"{id(R)}-{type(R)}",
            "mysql_id": f"{id(project_db)}-{project_db.example_type}",
            "redis_query_id": id(R.get),
            "mysql_query_id": id(project_db.select),
            "threading": threading.get_ident()
        }
        return api_result(code=200, message='GET: test api', data=data)

    def post(self):
        """test post"""

        data = request.get_json()
        print(data)
        return api_result(code=200, message='POST: test api', data=True)

    def put(self):
        """test put"""

        data = request.get_json()
        return api_result(code=203, message='PUT: test api', data=True)

    def delete(self):
        """test delete"""

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
        results2 = send_message.delay('yyx456')
        results3 = test_context.delay()
        results4 = web_ui.delay()
        data = [str(results1), str(results2), str(results3), str(results4)]
        print(data)
        return api_result(code=200, message='调试Celery异步任务', data=data)
