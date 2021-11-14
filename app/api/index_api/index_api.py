# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index_api.py
# @Software: PyCharm

import asyncio
from sqlalchemy.sql import func

from all_reference import *
from app.models.admin.models import Admin
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_scenario.models import TestCaseScenario


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
        data = request.get_json()
        d = data
        return api_result(code=200, message='index', data=d)
