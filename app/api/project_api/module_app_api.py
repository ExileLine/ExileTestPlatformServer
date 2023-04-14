# -*- coding: utf-8 -*-
# @Time    : 2022/3/2 6:23 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : module_app_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestModuleApp, TestProject, MidModuleCase, MidModuleScenario


class ModuleAppApi(MethodView):
    """
    模块应用 api
    GET: 模块应用详情
    POST: 模块应用新增
    PUT: 模块应用编辑
    DELETE: 模块应用删除
    """

    def get(self, module_id):
        """模块应用详情"""

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=NO_DATA, message=f'功能模块或应用不存在:{module_id}')

        case_id_list = [mid.case_id for mid in MidModuleCase.query.filter_by(module_id=module_id).all()]
        query_case = TestCase.query.filter(TestCase.id.in_(case_id_list)).all()
        case_list = [case.to_json() for case in query_case if query_case]

        scenario_id_list = [mid.scenario_id for mid in MidModuleScenario.query.filter_by(module_id=module_id).all()]
        query_scenario = TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()
        scenario_list = [scenario.to_json() for scenario in query_scenario if query_scenario]

        result = query_module.to_json()
        result['case_list'] = case_list
        result['scenario_list'] = scenario_list

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    def post(self):
        """模块应用新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        module_name = data.get('module_name')
        module_type = data.get('module_type')
        module_code = data.get('module_code', f"默认{int(time.time())}")
        module_source = data.get('module_source')
        case_list = data.get('case_list')
        scenario_list = data.get('scenario_list')
        remark = data.get('remark')

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=NO_DATA, message=f"项目: {project_id} 不存在")

        query_module = TestModuleApp.query.filter_by(module_code=module_code).first()
        if query_module:
            return api_result(code=UNIQUE_ERROR, message=f"应用编号:{module_code}已存在")

        if not isinstance(case_list, list):
            return api_result(code=TYPE_ERROR, message=f'参数错误:{case_list}')

        if not isinstance(scenario_list, list):
            return api_result(code=TYPE_ERROR, message=f'参数错误:{scenario_list}')

        new_module = TestModuleApp(
            project_id=project_id,
            module_name=module_name,
            module_type=module_type,
            module_code=module_code,
            module_source=module_source,
            case_list=case_list,
            scenario_list=scenario_list,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_module.save()
        module_id = new_module.id

        if case_list:
            list(map(lambda case_id: db.session.add(
                MidModuleCase(
                    module_id=module_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     case_list))

        if scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidModuleScenario(
                    module_id=module_id, scenario_id=scenario_id, creator=g.app_user.username,
                    creator_id=g.app_user.id)),
                     scenario_list))

        db.session.commit()
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE)

    def put(self):
        """模块应用编辑"""

        data = request.get_json()
        project_id = data.get('project_id')
        module_id = data.get('id')
        module_name = data.get('module_name')
        module_type = data.get('module_type')
        module_code = data.get('module_code', f"默认{int(time.time())}")
        module_source = data.get('module_source')
        case_list = data.get('case_list')
        scenario_list = data.get('scenario_list')
        remark = data.get('remark')

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=NO_DATA, message=f"项目: {project_id} 不存在")

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=NO_DATA, message=f'功能模块或应用不存在:{module_id}')

        if query_module.module_code != module_code:
            query_module_code = TestModuleApp.query.filter_by(module_code=module_code).all()
            if query_module_code:
                return api_result(code=UNIQUE_ERROR, message="应用编号已存在")

        if not isinstance(case_list, list):
            return api_result(code=TYPE_ERROR, message=f'参数错误:{case_list}')

        if not isinstance(scenario_list, list):
            return api_result(code=TYPE_ERROR, message=f'参数错误:{scenario_list}')

        query_module.project_id = project_id
        query_module.module_name = module_name
        query_module.module_type = module_type
        query_module.module_code = module_code
        query_module.module_source = module_source
        query_module.case_list = case_list
        query_module.scenario_list = scenario_list
        query_module.remark = remark
        query_module.modifier = g.app_user.username,
        query_module.modifier_id = g.app_user.id

        db.session.query(MidModuleCase).filter(MidModuleCase.module_id == module_id).delete(
            synchronize_session=False)

        db.session.query(MidModuleScenario).filter(MidModuleScenario.module_id == module_id).delete(
            synchronize_session=False)

        if case_list:
            list(map(lambda case_id: db.session.add(
                MidModuleCase(
                    module_id=module_id, case_id=case_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                     case_list))

        if scenario_list:
            list(map(lambda scenario_id: db.session.add(
                MidModuleScenario(
                    module_id=module_id, scenario_id=scenario_id, creator=g.app_user.username,
                    creator_id=g.app_user.id)),
                     scenario_list))

        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=SUCCESS_MESSAGE)

    def delete(self):
        """模块应用删除"""

        data = request.get_json()
        module_id = data.get('id')
        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=NO_DATA, message=f'功能模块或应用不存在:{module_id}')

        query_module.is_deleted = query_module.id
        query_module.modifier = g.app_user.username,
        query_module.modifier_id = g.app_user.id

        db.session.query(MidModuleCase).filter(MidModuleCase.module_id == module_id).delete(
            synchronize_session=False)
        db.session.query(MidModuleScenario).filter(MidModuleScenario.module_id == module_id).delete(
            synchronize_session=False)
        db.session.commit()
        return api_result(code=DEL_SUCCESS, message=SUCCESS_MESSAGE)


class ModuleAppPageApi(MethodView):
    """
    模块应用分页模糊查询 api
    POST: 模块应用新增
    """

    def post(self):
        """模块应用分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        module_id = data.get('id')
        module_name = data.get('module_name')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile5_test_module_app  
        WHERE 
        id = "id" 
        and module_name LIKE"%%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": module_id,
            "project_id": project_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestModuleApp,
            field_list=['module_name'],
            query_list=[module_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
