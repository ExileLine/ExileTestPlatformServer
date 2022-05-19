# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 15:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_cicd_api.py
# @Software: PyCharm


from all_reference import *

from .case_exec_api import QueryExecuteData, save_test_logs
from tasks.task03 import execute_main


class CaseCICDApi(MethodView):
    """
    CICD Api
    """

    def post(self):
        """1"""
        data = request.get_json()
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        mirror = data.get('mirror')
        url = data.get('url')

        # result_bool, result_data = QueryExecuteData.execute_all(
        #     **{"execute_dict_key": "task", "query": {"task_id": "47"}, "model_id": 47}
        # )
        # print(result_bool)
        # print(result_data)
        #
        # test_obj = {
        #     "execute_id": 47,
        #     "execute_name": result_data.get("execute_name"),
        #     "execute_type": "task_all",
        #     "execute_label": "all",
        #     "execute_user_id": 8888,
        #     "execute_username": "CICD",
        #     "use_base_url": False,
        #     # "is_execute_all": is_execute_all,
        #     # "case_list": send_test_case_list,
        #     # "execute_dict": execute_dict,
        #     # "is_dd_push": True,
        #     # "dd_push_id": dd_push_id,
        #     # "ding_talk_url": ding_talk_url,
        #     "trigger_type": "CICD_execute"
        # }
        # results = execute_main.delay(test_obj)
        # print(results)
        return api_result(code=200, message='操作成功')
