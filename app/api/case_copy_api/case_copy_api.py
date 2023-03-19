# -*- coding: utf-8 -*-
# @Time    : 2023/3/9 17:17
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_copy_api.py
# @Software: PyCharm


from all_reference import *

from app.models.test_case.models import TestCase
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp, MidProjectAndCase, \
    MidVersionCase, MidModuleCase
from app.models.test_case_assert.models import TestCaseDataAssBind


class CopyGenExample:
    """复制生成对象"""

    def __init__(self, case_obj: TestCase = None, is_commit=False):
        """

        :param case_obj: 用例orm实例
        :param is_commit:
        """
        self.case_obj = case_obj
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
        version_id = data.get('version_id', 0)
        module_id = data.get('module_id', 0)

        query_case = TestCase.query.get(case_id)
        if not query_case:
            return api_result(code=NO_DATA, message=f'用例id:{case_id}不存在')

        if not is_cross:  # 复制到当前项目

            query_project = TestProject.query.get(project_id)
            if not query_project:
                return api_result(code=NO_DATA, message=f'项目id: {project_id} 不存在')

            if version_id:
                query_version = TestProjectVersion.query.filter_by(id=version_id, project_id=project_id).first()
                if not query_version:
                    return api_result(code=NO_DATA, message=f'版本id: {version_id} 不存在')

            if module_id:
                query_module = TestModuleApp.query.filter_by(id=module_id, project_id=project_id).first()
                if not query_module:
                    return api_result(code=NO_DATA, message=f'模块id: {module_id} 不存在')

            cge = CopyGenExample(case_obj=query_case)
            cge.gen_case_and_bind()
            new_case_id = cge.new_case_id

            db.session.add(
                MidProjectAndCase(
                    project_id=project_id,
                    case_id=new_case_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
            )
            db.session.add(
                MidVersionCase(
                    version_id=version_id,
                    case_id=new_case_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
            )
            db.session.add(
                MidModuleCase(
                    module_id=module_id,
                    case_id=new_case_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
            )

        else:  # TODO 复制到其他项目

            query_project = TestProject.query.get(cross_project_id)
            if not query_project:
                return api_result(code=NO_DATA, message=f'跨项目id: {cross_project_id} 不存在')

            if version_id:
                query_version = TestProjectVersion.query.filter_by(id=version_id, project_id=cross_project_id).first()
                if not query_version:
                    return api_result(code=NO_DATA, message=f'跨项目版本id: {version_id} 不存在')

            if module_id:
                query_module = TestModuleApp.query.filter_by(id=module_id, project_id=cross_project_id).first()
                if not query_module:
                    return api_result(code=NO_DATA, message=f'跨项目模块id: {module_id} 不存在')

            # query_pc = MidProjectAndCase.query.filter_by(case_id=case_id).all()
            # query_vc = MidVersionCase.query.filter_by(case_id=case_id).all()
            # query_mc = MidModuleCase.query.filter_by(case_id=case_id).all()
            #
            # if query_pc:
            #     list(map(lambda mid_obj: db.session.add(
            #         MidProjectAndCase(project_id=mid_obj.project_id, case_id=new_case_id,
            #                           creator=g.app_user.username,
            #                           creator_id=g.app_user.id, remark="复制用例生成")), query_pc))
            # if query_vc:
            #     list(map(lambda mid_obj: db.session.add(
            #         MidVersionCase(version_id=mid_obj.version_id, case_id=new_case_id,
            #                        creator=g.app_user.username,
            #                        creator_id=g.app_user.id, remark="复制用例生成")), query_vc))
            # if query_mc:
            #     list(map(lambda mid_obj: db.session.add(
            #         MidModuleCase(module_id=mid_obj.module_id, case_id=new_case_id, creator=g.app_user.username,
            #                       creator_id=g.app_user.id, remark="复制用例生成")), query_mc))

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
