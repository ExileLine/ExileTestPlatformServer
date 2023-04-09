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
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
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

        return api_result(code=SUCCESS, message='调试:执行UI用例', data=[])

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
        use_client = data.get('use_client', False)
        client = data.get('client')
        use_dd_push = data.get('use_dd_push', False)
        dd_push_id = data.get('dd_push_id')
        ding_talk_url = ""
        use_mail = data.get('use_mail', False)
        mail_send_all = data.get('mail_send_all', False)
        mail_list = data.get('mail_list', [])

        if use_client:  # TODO PC端执行
            print(client)
            return api_result(code=SUCCESS, message='调用PC端成功', data=client)

        if use_dd_push:
            query_dd_push = DingDingConfModel.query.get(dd_push_id)
            if not query_dd_push:
                return api_result(code=NO_DATA, message="钉钉群不存在")
            if query_dd_push.is_deleted != 0:
                return api_result(code=BUSINESS_ERROR, message=f"钉钉群: {query_dd_push.title} 被禁用")

            ding_talk_url = query_dd_push.ding_talk_url

        if use_mail:
            if mail_send_all:
                mail_list = [m.mail for m in MailConfModel.query.filter_by(is_deleted=0).all()]
            else:
                mail_list = [m.mail for m in MailConfModel.query.filter(
                    MailConfModel.id.in_(mail_list),
                    MailConfModel.is_deleted == 0
                ).all()]

        if mail_send_all and not mail_list:
            return api_result(code=BUSINESS_ERROR, message="邮件不能为空，或者邮件已禁用")

        execute_query = UiCaseExecuteQuery(execute_key=execute_key, query_id=execute_id)
        ui_case_list = execute_query.use_func()
        test_obj = {
            "project_id": project_id,
            "execute_id": execute_id,
            "execute_name": execute_name,
            "execute_key": execute_key,
            "execute_type": execute_type,
            "execute_label": execute_label,
            "execute_user_id": g.app_user.id,
            "execute_username": g.app_user.username,
            "ui_case_list": ui_case_list,
            "use_dd_push": use_dd_push,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "use_mail": use_mail,
            "mail_list": mail_list,
            "trigger_type": trigger_type,
        }
        execute_logs_id = create_execute_logs(**test_obj)
        test_obj['execute_logs_id'] = execute_logs_id

        results = execute_ui_case.delay(test_obj)
        print(results)
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=[str(results)])


if __name__ == '__main__':
    @set_app_context
    def test_ExecuteQuery():
        """测试"""

        execute_query = UiCaseExecuteQuery(execute_key='ui_case', query_id=19)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_project_all', query_id=30)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_version_all', query_id=1)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_task_all', query_id=1)
        # execute_query = UiCaseExecuteQuery(execute_key='ui_module_all', query_id=1)
        print(execute_query.use_func())


    test_ExecuteQuery()
