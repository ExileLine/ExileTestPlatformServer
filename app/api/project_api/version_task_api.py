# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 1:46 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : version_task_api.py
# @Software: PyCharm


from all_reference import *
from app.models.admin.models import Admin
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import (
    TestProjectVersion, TestVersionTask, MidTaskCase, MidTaskScenario, MidModuleCase, MidModuleScenario
)
from app.models.ui_test_case.models import UiTestCase, MidTaskUiCase, MidModuleUiCase


class SaveMid:
    """写入关联关系"""

    def __init__(self, save_type: str, case_list: list, scenario_list: list, ui_case_list: list, task_id: int = None,
                 module_id: int = None):
        """

        :param save_type: 类型(task,module)
        :param case_list: 用例列表
        :param scenario_list: 场景列表
        :param ui_case_list: ui用例列表
        :param task_id: 任务id
        :param module_id: 模块id
        """

        self.save_type = save_type
        self.case_list = case_list
        self.scenario_list = scenario_list
        self.ui_case_list = ui_case_list
        self.task_id = task_id
        self.module_id = module_id
        self.d = {
            "task": self.save_task_mid,
            "module": self.save_module_mid
        }
        if self.save_type not in ("task", "module"):
            raise KeyError("save_type 应为 task 或 module")

    def save_task_mid(self):
        """写入任务关联关系"""

        if self.case_list:
            list(map(lambda case_id: db.session.add(
                MidTaskCase(
                    task_id=self.task_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     self.case_list))

        if self.scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidTaskScenario(
                    task_id=self.task_id, scenario_id=scenario_id, creator=g.app_user.username,
                    creator_id=g.app_user.id)),
                     self.scenario_list))

        if self.ui_case_list:
            list(map(lambda ui_case_id: db.session.add(
                MidTaskUiCase(
                    task_id=self.task_id, case_id=ui_case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     self.ui_case_list))

        db.session.commit()

    def save_module_mid(self):
        """写入模块关联关系"""

        if self.case_list:
            list(map(lambda case_id: db.session.add(
                MidModuleCase(
                    module_id=self.module_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     self.case_list))

        if self.scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidModuleScenario(
                    module_id=self.module_id, scenario_id=scenario_id, creator=g.app_user.username,
                    creator_id=g.app_user.id)),
                     self.scenario_list))

        if self.ui_case_list:
            list(map(lambda ui_case_id: db.session.add(
                MidModuleUiCase(
                    module_id=self.module_id, case_id=ui_case_id, creator=g.app_user.username,
                    creator_id=g.app_user.id)),
                     self.ui_case_list))

        db.session.commit()

    def main(self):
        """main"""

        f = self.d.get(self.save_type)
        f()


def vt_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_id = data.get('version_id', '')
        task_name = data.get('task_name', '')
        user_list = data.get('user_list', [])

        query_version = TestProjectVersion.query.get(version_id)
        if not query_version:
            return api_result(code=NO_DATA, message=f"版本迭代: {version_id} 不存在")

        if query_version.project_id != project_id:
            return api_result(code=NO_DATA, message=f"版本迭代: {query_version.version_name} 不存在该项目中")

        if not task_name:
            return api_result(code=REQUIRED, message="任务名称不能为空")

        for user_id in user_list:
            query_user = Admin.query.get(user_id)
            if not query_user:
                return api_result(code=NO_DATA, message=f"用户: {user_id} 不存在")

        return func(*args, **kwargs)

    return wrapper


class VersionTaskApi(MethodView):
    """
    版本迭代任务 api
    GET: 迭代任务详情
    POST: 迭代任务新增
    PUT: 迭代任务编辑
    DELETE: 迭代任务删除
    """

    def get(self, task_id):
        """迭代任务详情"""

        query_task = TestVersionTask.query.get(task_id)
        if not query_task:
            return api_result(code=NO_DATA, message=f"任务: {task_id} 不存在")

        query_user_list = Admin.query.filter(Admin.id.in_(query_task.user_list)).all()
        user_list = [user.to_json() for user in query_user_list]

        # 用例
        case_id_list = [mid.case_id for mid in MidTaskCase.query.filter_by(task_id=task_id).all()]
        query_case = TestCase.query.filter(TestCase.id.in_(case_id_list)).all()
        case_list = [case.to_json() for case in query_case if query_case]

        # 场景
        scenario_id_list = [mid.scenario_id for mid in MidTaskScenario.query.filter_by(task_id=task_id).all()]
        query_scenario = TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()
        scenario_list = [scenario.to_json() for scenario in query_scenario if query_scenario]

        # UI用例
        ui_case_id_list = [mid.case_id for mid in MidTaskUiCase.query.filter_by(task_id=task_id).all()]
        query_ui_case = UiTestCase.query.filter(UiTestCase.id.in_(ui_case_id_list)).all()
        ui_case_list = [ui_case.to_json() for ui_case in query_ui_case if query_ui_case]

        result = query_task.to_json()
        result['user_list'] = user_list
        result['case_list'] = case_list
        result['scenario_list'] = scenario_list
        result['ui_case_list'] = ui_case_list

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    @vt_decorator
    def post(self):
        """迭代任务新增"""

        data = request.get_json()
        version_id = data.get('version_id', '')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        user_list = data.get('user_list', [])
        case_list = data.get('case_list', [])
        scenario_list = data.get('scenario_list', [])
        ui_case_list = data.get('ui_case_list', [])
        remark = data.get('remark')

        new_version_task = TestVersionTask(
            version_id=version_id,
            task_name=task_name,
            task_type=task_type,
            user_list=user_list,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_version_task.save()
        task_id = new_version_task.id

        SaveMid(
            save_type="task",
            task_id=task_id,
            case_list=case_list,
            scenario_list=scenario_list,
            ui_case_list=ui_case_list,
        ).main()
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE)

    @vt_decorator
    def put(self):
        """迭代任务编辑"""

        data = request.get_json()
        task_id = data.get('id')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        user_list = data.get('user_list', [])
        case_list = data.get('case_list', [])
        scenario_list = data.get('scenario_list', [])
        ui_case_list = data.get('ui_case_list', [])
        remark = data.get('remark')

        query_task = TestVersionTask.query.get(task_id)
        if not query_task:
            return api_result(code=NO_DATA, message=f"任务: {task_id} 不存在")

        query_task.task_name = task_name
        query_task.task_type = task_type
        query_task.user_list = user_list
        query_task.remark = remark
        query_task.modifier = g.app_user.username,
        query_task.modifier_id = g.app_user.id

        db.session.query(MidTaskCase).filter(MidTaskCase.task_id == task_id).delete(
            synchronize_session=False)

        db.session.query(MidTaskScenario).filter(MidTaskScenario.task_id == task_id).delete(
            synchronize_session=False)

        db.session.query(MidTaskUiCase).filter(MidTaskUiCase.task_id == task_id).delete(
            synchronize_session=False)

        SaveMid(
            save_type="task",
            task_id=task_id,
            case_list=case_list,
            scenario_list=scenario_list,
            ui_case_list=ui_case_list,
        ).main()
        return api_result(code=PUT_SUCCESS, message=SUCCESS_MESSAGE)

    def delete(self):
        """迭代任务删除"""

        data = request.get_json()
        task_id = data.get('id')

        query_task = TestVersionTask.query.get(task_id)
        if not query_task:
            return api_result(code=NO_DATA, message=f"任务: {task_id} 不存在")

        query_task.is_deleted = query_task.id
        query_task.modifier = g.app_user.username
        query_task.modifier_id = g.app_user.id

        db.session.query(MidTaskCase).filter(MidTaskCase.task_id == task_id).delete(synchronize_session=False)
        db.session.query(MidTaskScenario).filter(MidTaskScenario.task_id == task_id).delete(
            synchronize_session=False)
        db.session.query(MidTaskUiCase).filter(MidTaskUiCase.task_id == task_id).delete(synchronize_session=False)
        db.session.commit()
        return api_result(code=DEL_SUCCESS, message=SUCCESS_MESSAGE)


class VersionTaskPageApi(MethodView):
    """
    迭代任务分页模糊查询 api
    version task page api
    POST: 迭代任务分页模糊查询
    """

    def post(self):
        """迭代任务分页模糊查询"""

        data = request.get_json()
        version_id = data.get('version_id')
        task_id = data.get('id')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        if not version_id:
            return api_result(code=NO_DATA, message=f"版本迭代id: {version_id} 不存在")

        where_dict = {
            "id": task_id,
            "task_type": task_type,
            "version_id": version_id,
            "creator_id": creator_id,
            "is_deleted": is_deleted
        }

        result_data = general_query(
            model=TestVersionTask,
            field_list=['task_name'],
            query_list=[task_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
