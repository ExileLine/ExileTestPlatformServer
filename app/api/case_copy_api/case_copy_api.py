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


class CaseCopyApi(MethodView):
    """
    用例复制Api
    POST: 用例复制
    """

    def post(self):
        """用例复制"""

        data = request.get_json()
        case_id = data.get('case_id')
        is_current = data.get('is_current', True)
        project_id = data.get('project_id', 0)
        version_id = data.get('version_id', 0)
        module_id = data.get('module_id', 0)

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=NO_DATA, message=f'用例id:{case_id}不存在')

        new_test_case = TestCase(
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
        new_test_case.save()
        new_test_case_id = new_test_case.id

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id, is_deleted=0).all()

        if query_bind:
            for index, d in enumerate(query_bind, 1):
                new_bind = TestCaseDataAssBind(
                    case_id=new_test_case_id,
                    data_id=d.data_id,
                    ass_resp_id_list=d.ass_resp_id_list,  # TODO 检查 ass_resp_id_list 中的 id 是否存在
                    ass_field_id_list=d.ass_field_id_list,  # TODO 检查 ass_field_id_list 中的 id 是否存在
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
                db.session.add(new_bind)

        if not is_current:  # 当前项目-迭代

            query_pc = MidProjectAndCase.query.filter_by(case_id=case_id).all()
            query_vc = MidVersionCase.query.filter_by(case_id=case_id).all()
            query_mc = MidModuleCase.query.filter_by(case_id=case_id).all()

            if query_pc:
                list(map(lambda mid_obj: db.session.add(
                    MidProjectAndCase(project_id=mid_obj.project_id, case_id=new_test_case_id,
                                      creator=g.app_user.username,
                                      creator_id=g.app_user.id, remark="复制用例生成")), query_pc))
            if query_vc:
                list(map(lambda mid_obj: db.session.add(
                    MidVersionCase(version_id=mid_obj.version_id, case_id=new_test_case_id,
                                   creator=g.app_user.username,
                                   creator_id=g.app_user.id, remark="复制用例生成")), query_vc))
            if query_mc:
                list(map(lambda mid_obj: db.session.add(
                    MidModuleCase(module_id=mid_obj.module_id, case_id=new_test_case_id, creator=g.app_user.username,
                                  creator_id=g.app_user.id, remark="复制用例生成")), query_mc))
        else:
            if not TestProject.query.get(project_id):
                return api_result(code=NO_DATA, message=f'项目id: {project_id} 不存在')

            if version_id:
                if not TestProjectVersion.query.filter_by(id=version_id, project_id=project_id).first():
                    return api_result(code=NO_DATA, message=f'版本id: {version_id} 不存在')

            if module_id:
                if not TestModuleApp.query.filter_by(id=module_id, project_id=project_id).first():
                    return api_result(code=NO_DATA, message=f'模块id: {module_id} 不存在')

            db.session.add(
                MidProjectAndCase(
                    project_id=project_id,
                    case_id=new_test_case_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
            )
            db.session.add(
                MidVersionCase(
                    version_id=version_id,
                    case_id=new_test_case_id,
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="复制用例生成"
                )
            )
            db.session.add(
                MidModuleCase(
                    module_id=module_id,
                    case_id=new_test_case_id,
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
