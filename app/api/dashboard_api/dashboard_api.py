# -*- coding: utf-8 -*-
# @Time    : 2022/9/21 16:29
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : dashboard_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_project.models import MidProjectAndCase, MidProjectScenario
from app.models.test_variable.models import TestVariable
from app.models.test_case_assert.models import TestCaseAssertion
from app.models.test_logs.models import TestExecuteLogs


class DashboardApi(MethodView):
    """
    仪表盘 Api
    """

    def post(self):
        """仪表盘数据"""

        data = request.get_json()
        project_id = data.get('project_id')
        env = data.get('env')
        if env:
            data = {
                "total_case": 7198705,
                "total_scenario": 637568,
                "total_assert": 666666,
                "total_variable": 999999,
                "total_execute_count": 1111110,
                "total_execute_success": 888888,
                "total_execute_fail": 200000,
                "total_execute_error": 22222,
                "total_the_day_execute": 888,
                "total_current_month_execute": 666
            }
            return api_result(code=POST_SUCCESS, message='操作成功(dev)', data=data)

        total_case = MidProjectAndCase.query.filter_by(project_id=project_id).count()
        total_scenario = MidProjectScenario.query.filter_by(project_id=project_id).count()
        total_variable = TestVariable.query.filter_by(project_id=project_id).count()
        total_assert = TestCaseAssertion.query.filter_by(project_id=project_id).count()
        total_execute_success = TestExecuteLogs.query.filter_by(project_id=project_id, execute_status=1).count()
        total_execute_fail = TestExecuteLogs.query.filter_by(project_id=project_id, execute_status=0).count()

        l_time_1 = TimeTool.the_day_timestamp()
        r_time_1 = l_time_1 + 86400 - 1
        total_the_day_execute = TestExecuteLogs.query.filter(TestExecuteLogs.id.between(l_time_1, r_time_1)).count()

        l_time_2 = TimeTool.current_month_timestamp()
        r_time_2 = TimeTool.next_month_first_timestamp() - 1
        total_current_month_execute = TestExecuteLogs.query.filter(
            TestExecuteLogs.id.between(l_time_2, r_time_2)
        ).count()

        data = {
            "total_case": total_case,
            "total_scenario": total_scenario,
            "total_assert": total_assert,
            "total_variable": total_variable,
            "total_execute_count": total_execute_success + total_execute_fail,
            "total_execute_success": total_execute_success,
            "total_execute_fail": total_execute_fail,
            "total_execute_error": 0,
            "total_the_day_execute": total_the_day_execute,
            "total_current_month_execute": total_current_month_execute
        }
        return api_result(code=POST_SUCCESS, message='操作成功', data=data)
