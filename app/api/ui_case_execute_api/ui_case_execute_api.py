# -*- coding: utf-8 -*-
# @Time    : 2023/2/15 15:16
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_execute_api.py
# @Software: PyCharm


from all_reference import *

from app.models.ui_test_case.models import MidProjectAndUiCase
from tasks.execute_ui_case import execute_ui_case
from common.libs.ui_test_runner.test.meta_data import meta_data as md


class UiCaseExecuteApi(MethodView):
    """
    执行UI用例 Api
    POST: 执行UI用例
    """

    def get(self):
        """调试"""
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=[])

    def post(self):
        """执行"""

        data = request.get_json()
        project_id = data.get('project_id')
        execute_id = data.get('execute_id')
        execute_key = data.get('execute_key')
        execute_name = data.get('execute_name')
        execute_type = data.get('execute_type')
        execute_label = data.get('execute_label')

        meta_data_list = [md]
        results = execute_ui_case.delay(meta_data_list=meta_data_list)
        print(results)
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=[str(results)])
