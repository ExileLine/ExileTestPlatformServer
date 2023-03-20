# -*- coding: utf-8 -*-
# @Time    : 2023/3/9 17:17
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_copy_api.py
# @Software: PyCharm


from all_reference import *

from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProject, MidProjectAndCase
from app.models.test_case_assert.models import TestCaseDataAssBind


class CopyGenExample:
    """复制生成对象"""

    def __init__(self, case_obj: TestCase = None, scenario_obj: TestCaseScenario = None, is_commit: bool = False):
        """

        :param case_obj: 用例orm实例
        :param scenario_obj: 场景orm实例
        :param is_commit: 是否进行一次事务提交
        """
        self.case_obj = case_obj
        self.scenario_obj = scenario_obj
        self.is_commit = is_commit
        self.new_case_id = None

    def gen_case_and_bind(self):
        """生成新的用例"""

        query_case = self.case_obj
        new_case = TestCase(
            case_name=query_case.case_name,
            request_method=query_case.request_method,
            request_base_url=query_case.request_base_url,
            request_url=query_case.request_url,
            case_status=query_case.case_status,
            is_shared=query_case.is_shared,
            is_public=query_case.is_public,
            is_copy=1,
            remark="复制用例: {}-{}".format(query_case.id, query_case.case_name),
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_case.save()
        self.new_case_id = new_case.id

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=query_case.id, is_deleted=0).all()
        if query_bind:
            for bind in query_bind:
                new_bind = TestCaseDataAssBind(
                    case_id=self.new_case_id,
                    data_id=bind.data_id,
                    ass_resp_id_list=bind.ass_resp_id_list,
                    ass_field_id_list=bind.ass_field_id_list,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark=f"复制用例: {self.new_case_id} 生成"
                )
                db.session.add(new_bind)

        if self.is_commit:
            db.commit()

    def gen_scenario(self):
        """生成新的场景"""


class CaseCopyApi(MethodView):
    """
    用例复制Api
    POST: 用例复制
    """

    def post(self):
        """用例复制"""

        data = request.get_json()
        case_id = data.get('id')
        is_cross = data.get('is_cross', False)
        cross_project_id = data.get('cross_project_id', 0)
        project_id = data.get('project_id', 0)

        query_case = TestCase.query.get(case_id)
        if not query_case:
            return api_result(code=NO_DATA, message=f'用例id:{case_id}不存在')

        if not is_cross:  # 复制到当前项目
            query_project = TestProject.query.get(project_id)
            save_project_id = project_id
            err_message = f'项目id: {project_id} 不存在'
        else:  # 跨项目复制
            query_project = TestProject.query.get(cross_project_id)
            save_project_id = cross_project_id
            err_message = f'跨项目id: {cross_project_id} 不存在'

        if not query_project:
            return api_result(code=NO_DATA, message=err_message)

        cge = CopyGenExample(case_obj=query_case)
        cge.gen_case_and_bind()
        new_case_id = cge.new_case_id

        db.session.add(
            MidProjectAndCase(
                project_id=save_project_id,
                case_id=new_case_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id,
                remark="复制用例生成"
            )
        )
        db.session.commit()
        return api_result(code=SUCCESS, message=POST_MESSAGE)


class ScenarioCopyApi(MethodView):
    """
    场景复制Api
    POST: 场景复制
    """

    def post(self):
        """场景复制"""

        return api_result(code=SUCCESS, message=POST_MESSAGE)
