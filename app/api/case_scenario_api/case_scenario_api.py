# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_scenario_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProjectVersion, MidProjectVersionAndScenario
from app.api.case_api.case_api import check_version


def create_mid_scenario(project_id, version_id, scenario_id, module_id):
    new_mid = MidProjectVersionAndScenario(
        project_id=project_id,
        version_id=version_id,
        task_id=0,
        scenario_id=scenario_id,
        module_id=module_id,
        creator=g.app_user.username,
        creator_id=g.app_user.id
    )
    db.session.add(new_mid)


class CaseScenarioApi(MethodView):
    """
    用例场景Api
    GET: 用例场景详情
    POST: 用例场景新增
    PUT: 用例场景编辑
    DELETE: 用例场景删除
    """

    def get(self, scenario_id):
        """用例场景详情"""

        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

        result = query_scenario.to_json()
        case_id_list = result.get('case_list')

        if not case_id_list:
            return api_result(code=400, message='异常的数据')

        gen_case_id_list = sorted(case_id_list, key=lambda x: x.get("index", x.get('case_id')), reverse=True)
        case_obj_list = []

        if case_id_list:
            for case in gen_case_id_list:
                case_id = case.get('case_id')
                index = case.get('index', case_id)
                query_case = TestCase.query.get(case_id)
                if query_case:
                    case_obj = query_case.to_json()
                    case_obj['index'] = index
                    case_obj_list.append(case_obj)
            result['case_list'] = case_obj_list

        query_mid = MidProjectVersionAndScenario.query.filter_by(scenario_id=scenario_id, is_deleted=0).all()
        version_id_list = [mid.version_id for mid in query_mid]
        version_model_list = TestProjectVersion.query.filter(
            TestProjectVersion.id.in_(version_id_list),
            TestProjectVersion.is_deleted == 0).all()
        version_obj_list = [v.to_json() for v in version_model_list]
        result["version_id_list"] = version_obj_list

        return api_result(code=200, message='操作成功', data=result)

    def post(self):
        """用例场景新增"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        module_id = data.get('module_id', 0)
        version_id_list = data.get('version_id_list', [])
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        if not isinstance(project_id, int):
            return api_result(code=400, message='project_id 错误')

        if not isinstance(module_id, int):
            return api_result(code=400, message='module_id 错误')

        if version_id_list and not check_version(project_id=project_id, version_id_list=version_id_list):
            return api_result(code=400, message=f'版本迭代不存在或不在项目id: {project_id} 关联')

        query_scenario = TestCaseScenario.query.filter_by(scenario_title=scenario_title).first()

        if query_scenario:
            return api_result(code=400, message='用例场景标题:{} 已经存在'.format(scenario_title))

        if not case_list or len(case_list) <= 1:
            return api_result(code=400, message='用例列表不能为空,或需要一条以上的用例组成')

        new_scenario = TestCaseScenario(
            scenario_title=scenario_title,
            case_list=case_list,
            is_shared=is_shared,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_scenario.save()
        scenario_id = new_scenario.id

        if version_id_list:
            for version_obj in version_id_list:
                version_id = version_obj.get('id')
                create_mid_scenario(
                    project_id=project_id,
                    version_id=version_id,
                    scenario_id=scenario_id,
                    module_id=module_id
                )
        else:
            create_mid_scenario(project_id=project_id, version_id=0, scenario_id=scenario_id, module_id=module_id)
        db.session.commit()
        return api_result(code=201, message='创建成功')

    def put(self):
        """用例场景编辑"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        module_id = data.get('module_id', 0)
        version_id_list = data.get('version_id_list', [])
        scenario_id = data.get('id')
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        if not isinstance(project_id, int):
            return api_result(code=400, message='project_id 错误')

        if not isinstance(module_id, int):
            return api_result(code=400, message='module_id 错误')

        if version_id_list and not check_version(project_id=project_id, version_id_list=version_id_list):
            return api_result(code=400, message=f'版本迭代不存在或不在项目id: {project_id} 关联')

        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not case_list or len(case_list) <= 1:
            return api_result(code=400, message='用例列表不能为空,或需要一条以上的用例组成')

        if not query_scenario:
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

        if query_scenario.scenario_title != scenario_title:
            if TestCaseScenario.query.filter_by(scenario_title=scenario_title).all():
                return api_result(code=400, message='用例场景:{} 已经存在'.format(scenario_title))

        query_scenario.scenario_title = scenario_title
        query_scenario.case_list = case_list
        query_scenario.is_shared = is_shared
        query_scenario.is_public = is_public
        query_scenario.modifier = g.app_user.username
        query_scenario.modifier_id = g.app_user.id

        query_mid_all = MidProjectVersionAndScenario.query.filter_by(scenario_id=scenario_id, task_id=0).all()

        obj_id_list = list(map(lambda obj: obj.id, query_mid_all))

        db.session.query(MidProjectVersionAndScenario).filter(MidProjectVersionAndScenario.id.in_(obj_id_list)).delete(
            synchronize_session=False)

        if version_id_list:
            for version_obj in version_id_list:
                version_id = version_obj.get('id')
                create_mid_scenario(
                    project_id=project_id,
                    version_id=version_id,
                    scenario_id=scenario_id,
                    module_id=module_id
                )
        else:
            create_mid_scenario(project_id=project_id, version_id=0, scenario_id=scenario_id, module_id=module_id)
        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例场景删除"""

        data = request.get_json()
        scenario_id = data.get('id')
        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

        if query_case.creator_id != g.app_user.id:
            return api_result(code=400, message='非管理员不能删除其他人的用例场景！')

        query_scenario.modifier_id = g.app_user.id
        query_scenario.modifier = g.app_user.username
        query_scenario.delete()
        return api_result(code=204, message='删除成功')


class CaseScenarioPageApi(MethodView):
    """
    case scenario page api
    POST: 用例场景分页模糊查询
    """

    def post(self):
        """用例场景分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_id = data.get('version_id')
        scenario_id = data.get('scenario_id')
        scenario_title = data.get('scenario_title', '')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        # TODO 旧数据 version_id 为 0,后续去除
        if not version_id:
            query_version = TestProjectVersion.query.filter_by(project_id=project_id).all()
            version_id_list = (0,) + tuple([version.id for version in query_version])
        else:
            version_id_list = (0, version_id)

        limit = page_size(page=page, size=size)

        sql = f"""
        SELECT
            A.id,
            A.scenario_title,
            A.is_public,
            A.is_shared,
            A.total_execution,
            A.case_list,
            A.creator,
            A.create_time,
            A.create_timestamp,
            A.modifier,
            A.update_time,
            A.update_timestamp
        FROM
            exile_test_case_scenario A
        WHERE
            EXISTS (
                SELECT
                    B.id, B.scenario_id, B.version_id
                FROM
                    exile_test_mid_version_scenario B
                WHERE
                    B.scenario_id = A.id 
                    AND B.is_deleted = 0
                    AND B.version_id in {version_id_list})
                {f'AND creator_id={creator_id}' if creator_id else ''}
                AND is_deleted = {is_deleted}
                AND scenario_title LIKE"%{scenario_title}%"
            ORDER BY
                A.create_timestamp DESC
            LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT 
            COUNT(*)
        FROM
            exile_test_case_scenario A
        WHERE
            EXISTS (
                SELECT
                    B.id, B.scenario_id, B.version_id
                FROM
                    exile_test_mid_version_scenario B
                WHERE
                    B.scenario_id = A.id
                    AND B.is_deleted = 0 
                    AND B.version_id in {version_id_list})
                {f'AND creator_id={creator_id}' if creator_id else ''}
                AND is_deleted = {is_deleted}
                AND scenario_title LIKE"%{scenario_title}%";
        """

        result_list = project_db.select(sql)
        result_count = project_db.select(sql_count)

        result_data = {
            'records': result_list if result_list else [],
            'now_page': page,
            'total': result_count[0].get('COUNT(*)')
        }

        return api_result(code=200, message='操作成功', data=result_data)
