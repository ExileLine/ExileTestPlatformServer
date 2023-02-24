# -*- coding: utf-8 -*-
# @Time    : 2023/2/15 15:16
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_execute_api.py
# @Software: PyCharm


from all_reference import *

from app.models.ui_test_case.models import UiTestCase, MidProjectAndUiCase, MidVersionUiCase, MidTaskUiCase, \
    MidModuleUiCase
from tasks.execute_ui_case import execute_ui_case
from app.api.case_execute_api.case_execute_api import create_execute_logs


class UiCaseExecuteQuery:
    """执行数据查询组装"""

    def __init__(self, execute_key: str = None, query_id: int = None):
        self.execute_key = execute_key  # case,project,version,task,module...
        self.query_id = query_id
        self.query_func_dict = {
            "ui_case": self.query_single_case,
            "ui_project_all": self.query_project_case,
            "ui_version_all": self.query_version_case,
            "ui_task_all": self.query_task_case,
            "ui_module_all": self.query_module_case
        }
        self.use_func = self.query_func_dict.get(self.execute_key)

    def query_single_case(self):
        """单个UI用例"""

        ui_case = UiTestCase.query.filter_by(id=self.query_id, is_deleted=0).first()
        result = [ui_case.to_json()] if ui_case else []
        return result

    def query_project_case(self):
        """项目下所有UI用例"""

        query_ui_case = UiTestCase.query.join(MidProjectAndUiCase, UiTestCase.id == MidProjectAndUiCase.case_id).filter(
            UiTestCase.is_deleted == 0,
            MidProjectAndUiCase.project_id == self.query_id
        ).all()
        result = [ui_case.to_json() for ui_case in query_ui_case]
        return result

    def query_version_case(self):
        """版本下所有UI用例"""

        query_ui_case = UiTestCase.query.join(MidVersionUiCase, UiTestCase.id == MidVersionUiCase.case_id).filter(
            UiTestCase.is_deleted == 0,
            MidVersionUiCase.version_id == self.query_id
        ).all()
        result = [ui_case.to_json() for ui_case in query_ui_case]
        return result

    def query_task_case(self):
        """任务下所有UI用例"""

        query_ui_case = UiTestCase.query.join(MidTaskUiCase, UiTestCase.id == MidTaskUiCase.case_id).filter(
            UiTestCase.is_deleted == 0,
            MidTaskUiCase.task_id == self.query_id
        ).all()
        result = [ui_case.to_json() for ui_case in query_ui_case]
        return result

    def query_module_case(self):
        """模块下所有UI用例"""

        query_ui_case = UiTestCase.query.join(MidModuleUiCase, UiTestCase.id == MidModuleUiCase.case_id).filter(
            UiTestCase.is_deleted == 0,
            MidModuleUiCase.module_id == self.query_id
        ).all()
        result = [ui_case.to_json() for ui_case in query_ui_case]
        return result


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
        trigger_type = data.get('trigger_type', 'user_execute')

        execute_query = UiCaseExecuteQuery(execute_key=execute_key, query_id=execute_id)
        ui_case_list = execute_query.use_func()
        test_obj = {
            "project_id": project_id,
            "execute_id": execute_id,
            "execute_name": execute_name,
            "execute_type": execute_type,
            "execute_label": execute_label,
            "execute_user_id": g.app_user.id,
            "execute_username": g.app_user.username,
            "ui_case_list": ui_case_list,
            # "use_dd_push": use_dd_push,
            # "dd_push_id": dd_push_id,
            # "ding_talk_url": ding_talk_url,
            # "use_mail": use_mail,
            # "mail_list": mail_list,
            "trigger_type": trigger_type,
        }
        execute_logs_id = create_execute_logs(**test_obj)
        test_obj['execute_logs_id'] = execute_logs_id

        results = execute_ui_case.delay(test_obj)
        print(results)
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=test_obj)


if __name__ == '__main__':
    @set_app_context
    def test_ExecuteQuery():
        """测试"""

        execute_query = UiCaseExecuteQuery(execute_key='ui_case', query_id=6)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_project_all', query_id=30)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_version_all', query_id=1)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_task_all', query_id=1)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_module_all', query_id=1)
        print(execute_query.use_func())


    test_ExecuteQuery()
