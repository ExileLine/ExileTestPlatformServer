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
from app.models.test_project.models import TestProjectVersion, TestVersionTask, MidTaskCase, MidTaskScenario


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
            return api_result(code=400, message=f"任务: {task_id} 不存在")

        query_user_list = Admin.query.filter(Admin.id.in_(query_task.user_list)).all()
        user_list = [user.to_json() for user in query_user_list]

        case_id_list = [mid.case_id for mid in MidTaskCase.query.filter_by(task_id=task_id).all()]
        query_case = TestCase.query.filter(TestCase.id.in_(case_id_list)).all()
        case_list = [case.to_json() for case in query_case if query_case]

        scenario_id_list = [mid.scenario_id for mid in MidTaskScenario.query.filter_by(task_id=task_id).all()]
        query_scenario = TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()
        scenario_list = [scenario.to_json() for scenario in query_scenario if query_scenario]

        result = query_task.to_json()
        result['user_list'] = user_list
        result['case_list'] = case_list
        result['scenario_list'] = scenario_list

        return api_result(code=200, message="操作成功", data=result)

    def post(self):
        """迭代任务新增"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_id = data.get('version_id', '')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        user_list = data.get('user_list', [])
        case_list = data.get('case_list', [])
        scenario_list = data.get('scenario_list', [])
        remark = data.get('remark')

        if not TestProjectVersion.query.get(version_id):
            return api_result(code=400, message=f"版本迭代: {version_id} 不存在")

        for user_id in user_list:
            if not Admin.query.get(user_id):
                return api_result(code=400, message=f"用户: {user_id} 不存在")

        if not task_name:
            return api_result(code=400, message="任务名称不能为空")

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

        if case_list:
            list(map(lambda case_id: db.session.add(
                MidTaskCase(
                    task_id=task_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     case_list))

        if scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidTaskScenario(
                    task_id=task_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     scenario_list))

        db.session.commit()
        return api_result(code=201, message="操作成功")

    def put(self):
        """迭代任务编辑"""

        data = request.get_json()
        task_id = data.get('id')
        project_id = data.get('project_id', 0)
        version_id = data.get('version_id', '')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        user_list = data.get('user_list', [])
        case_list = data.get('case_list', [])
        scenario_list = data.get('scenario_list', [])
        remark = data.get('remark')

        query_task = TestVersionTask.query.get(task_id)
        if not query_task:
            return api_result(code=400, message=f"任务: {task_id} 不存在")

        if not TestProjectVersion.query.get(version_id):
            return api_result(code=400, message=f"版本迭代: {version_id} 不存在")

        for user_id in user_list:
            if not Admin.query.get(user_id):
                return api_result(code=400, message=f"用户: {user_id} 不存在")

        if not task_name:
            return api_result(code=400, message="任务名称不能为空")

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

        if case_list:
            list(map(lambda case_id: db.session.add(
                MidTaskCase(
                    task_id=task_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     case_list))

        if scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidTaskScenario(
                    task_id=task_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     scenario_list))

        db.session.commit()
        return api_result(code=203, message="操作成功")

    def delete(self):
        """迭代任务删除"""

        data = request.get_json()
        task_id = data.get('id')

        query_task = TestVersionTask.query.get(task_id)
        if not query_task:
            return api_result(code=400, message=f"任务: {task_id} 不存在")

        query_task.is_deleted = query_task.id
        query_task.modifier = g.app_user.username
        query_task.modifier_id = g.app_user.id

        db.session.query(MidTaskCase).filter(MidTaskCase.task_id == task_id).delete(synchronize_session=False)
        db.session.query(MidTaskScenario).filter(MidTaskScenario.task_id == task_id).delete(
            synchronize_session=False)
        db.session.commit()
        return api_result(code=204, message="操作成功")


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
            return api_result(code=400, message=f"版本迭代id: {version_id} 不存在")

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

        return api_result(code=200, message="操作成功", data=result_data)
