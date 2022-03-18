# -*- coding: utf-8 -*-
# @Time    : 2022/3/2 6:23 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : module_app_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestModuleApp, TestProject


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
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')
        project_id = query_module.project_id
        case_list = query_module.case_list
        scenario_list = query_module.scenario_list
        result = query_module.to_json()
        query_project = TestProject.query.get(project_id)
        if query_project:
            result['project_obj'] = query_project.to_json()

        cl = [case.to_json() for case in TestCase.query.filter(TestCase.id.in_(case_list)).all()]
        sl = [case.to_json() for case in TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_list)).all()]

        result['case_list'] = cl if cl else []
        result['scenario_list'] = sl if sl else []

        return api_result(code=200, message='操作成功', data=result)

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
        if project_id and not query_project:
            return api_result(code=400, message=f"项目: {project_id} 不存在")

        query_module = TestModuleApp.query.filter_by(module_code=module_code).first()

        if query_module:
            return api_result(code=400, message="应用编号已存在")

        if not isinstance(case_list, list):
            return api_result(code=400, message=f'参数错误:{case_list}')

        if not isinstance(scenario_list, list):
            return api_result(code=400, message=f'参数错误:{scenario_list}')

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
        return api_result(code=201, message='操作成功')

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
        if project_id and not query_project:
            return api_result(code=400, message=f"项目: {project_id} 不存在")

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')

        if query_module.module_code != module_code:
            query_module_code = TestModuleApp.query.filter_by(module_code=module_code).all()
            if query_module_code:
                return api_result(code=400, message="应用编号已存在")

        if not isinstance(case_list, list):
            return api_result(code=400, message=f'参数错误:{case_list}')

        if not isinstance(scenario_list, list):
            return api_result(code=400, message=f'参数错误:{scenario_list}')

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
        db.session.commit()
        return api_result(code=203, message='操作成功')

    def delete(self):
        """模块应用删除"""

        data = request.get_json()
        module_id = data.get('id')
        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')
        query_module.modifier = g.app_user.username,
        query_module.modifier_id = g.app_user.id
        query_module.delete()
        return api_result(code=204, message='操作成功')

    def patch(self):
        return api_result(code=200, message='patch')


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
        FROM exile_test_module_app  
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

        return api_result(code=200, message="操作成功", data=result_data)
