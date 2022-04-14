# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index_api.py
# @Software: PyCharm

from all_reference import *
from app.models.admin.models import Admin
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_logs.models import TestLogs


class IndexApi(MethodView):
    """
    index Api
    """

    async def get(self):
        """统计"""

        total_user = Admin.query.count()
        total_case = TestCase.query.count()
        total_case_execute = TestCase.query.with_entities(func.sum(TestCase.total_execution)).scalar()
        total_case_data = TestCaseData.query.count()
        total_scenario = TestCaseScenario.query.count()
        total_scenario_execute = TestCaseScenario.query.with_entities(
            func.sum(TestCaseScenario.total_execution)).scalar()

        data = {
            "total_user": total_user,
            "total_case": total_case,
            "total_case_execute": total_case_execute,
            "total_case_data": total_case_data,
            "total_scenario": total_scenario,
            "total_scenario_execute": total_scenario_execute,
            "total_execute_success": 9999,
            "total_execute_fail": 7777
        }

        return api_result(code=200, message='index', data=data)

    async def post(self):
        """2"""
        data = request.get_json()
        return api_result(code=200, message='index', data=data)

    async def put(self):
        """3"""
        tl = TestLogs(
            log_type='index',
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        tl.save()
        return api_result(code=203, message='index')

    async def delete(self):
        """4"""
        r1 = R.keys(pattern="test_log_*")
        r2 = R.keys(pattern="case_first_log:*")
        r3 = R.keys(pattern="scenario_first_log:*")
        __len = len(r1)
        list(map(lambda x: R.delete(x), r1))
        list(map(lambda x: R.delete(x), r2))
        list(map(lambda x: R.delete(x), r3))
        ex1 = project_db.execute_sql("""TRUNCATE exile_test_logs;""")
        ex2 = project_db.execute_sql("""TRUNCATE exile_test_execute_logs;""")
        return api_result(code=203, message='index', data=[__len, ex1, ex2])
