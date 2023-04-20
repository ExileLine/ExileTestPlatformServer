# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:38 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_scenario_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp, MidProjectScenario, \
    MidVersionScenario, MidTaskScenario, MidModuleScenario
from app.api.case_api.case_api import new_check_version, new_check_module


def zip_case(before_id_list, before_obj_list):
    """
    id_list = [1, 2, 5, 6, 1, 2, 7]

    obj_list = [
        {"id": 1},
        {"id": 2},
        {"id": 5},
        {"id": 6},
        {"id": 7}
    ]
    :param before_id_list:
    :param before_obj_list:
    :return:

    new_list = [
        {"id": 1},
        {"id": 2},
        {"id": 5},
        {"id": 6},
        {"id": 1},
        {"id": 2},
        {"id": 7}
    ]
    """
    current_dict = {case.get("id"): case for case in before_obj_list}
    new_list = [current_dict.get(i) for i in before_id_list if i in current_dict]
    return new_list


def query_case_order_by_field(case_id_list):
    """
    查询用例根据in排序
    :param case_id_list: 用例id列表
    :return:
    """

    sql = f"""SELECT * FROM exile5_test_case WHERE id in {tuple(case_id_list)} ORDER BY FIELD(id,{','.join(list(map(str, case_id_list)))});"""
    result = project_db.select(sql)

    if len(set(case_id_list)) != len(case_id_list):
        return zip_case(before_id_list=case_id_list, before_obj_list=result)
    else:
        return result


def scenario_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        project_id = data.get('project_id')
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=NO_DATA, message=f'项目: {project_id} 不存在')

        if version_list:
            result = new_check_version(project_id, version_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目:{query_project.project_name}下不存在->版本迭代id:{result}')

        if module_list:
            result = new_check_module(project_id, module_list)
            if result:
                return api_result(code=NO_DATA, message=f'项目:{query_project.project_name}下不存在->模块id:{result}')

        if not scenario_title:
            return api_result(code=REQUIRED, message='场景名称不能为空')

        if not isinstance(case_list, list) or not case_list or len(case_list) <= 1:
            return api_result(code=BUSINESS_ERROR, message='用例列表不能为空或需要一条以上的用例组成')

        case_sleep_list = []
        for case in case_list:
            case_index = case.get('index')
            case_id = case.get('case_id')
            if not case_index:
                case['index'] = case_id

            case_sleep = case.get('sleep', 0)
            if case_sleep >= 30:
                case_sleep_list.append(True)

        if case_sleep_list:
            return api_result(code=BUSINESS_ERROR, message='执行后等待时间不能大于30秒')

        return func(*args, **kwargs)

    return wrapper


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
            return api_result(code=NO_DATA, message=f'场景不存在:{scenario_id}')

        result = query_scenario.to_json()
        case_list = result.get('case_list')
        if not case_list:
            return api_result(code=DATA_ERROR, message='异常的数据')

        # TODO 后面新增中间表后修改这个逻辑
        sorted_case_id_list = sorted(case_list, key=lambda x: x.get("index", x.get('case_id')), reverse=True)

        # sorted_case_hash_map = {}
        # for i in sorted_case_id_list:
        #     case_id = i.get('case_id')
        #     sorted_case_hash_map[case_id] = i
        # query_case_id_list = [k for k in sorted_case_hash_map.keys()]
        # query_case_list = query_case_order_by_field(query_case_id_list)

        # for case in query_case_list:
        #     case_id = case.get('id')
        #     if sorted_case_hash_map.get(case_id):
        #         case.update(sorted_case_hash_map.get(case_id))

        query_case_id_list = [i.get('case_id') for i in sorted_case_id_list]
        query_case_list = query_case_order_by_field(query_case_id_list)

        if len(sorted_case_id_list) == len(query_case_list):
            d = {}
            case_list = []
            for index, case in enumerate(query_case_list):
                case_id = case.get('id')
                if case_id in d:
                    case = copy.deepcopy(case)
                    case.update(sorted_case_id_list[index])
                else:
                    case.update(sorted_case_id_list[index])
                    d[case_id] = ''
                case_list.append(case)
        else:
            return api_result(code=DATA_ERROR, message='数据异常')

        version_id_list = [m.version_id for m in MidVersionScenario.query.filter_by(scenario_id=scenario_id).all()]
        version_list = [m.to_json() for m in
                        TestProjectVersion.query.filter(TestProjectVersion.id.in_(version_id_list)).all()]

        module_id_list = [m.module_id for m in MidModuleScenario.query.filter_by(scenario_id=scenario_id).all()]
        module_list = [m.to_json() for m in TestModuleApp.query.filter(TestModuleApp.id.in_(module_id_list)).all()]

        result['case_list'] = case_list
        result["version_list"] = version_list
        result["module_list"] = module_list
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    @scenario_decorator
    def post(self):
        """用例场景新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_scenario = TestCaseScenario.query.filter_by(scenario_title=scenario_title, is_deleted=0).first()
        if query_scenario:
            return api_result(code=UNIQUE_ERROR, message=f'用例场景标题: {scenario_title} 已经存在')

        new_scenario = TestCaseScenario(
            scenario_title=scenario_title,
            case_list=case_list,
            is_public=is_public,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_scenario.save()
        scenario_id = new_scenario.id

        version_id_list = [obj.get('id') for obj in version_list]
        module_id_list = [obj.get('id') for obj in module_list]

        mid_pc = MidProjectScenario(
            project_id=project_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id
        )
        db.session.add(mid_pc)
        list(map(lambda version_id: db.session.add(
            MidVersionScenario(
                version_id=version_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 version_id_list))
        list(map(lambda module_id: db.session.add(
            MidModuleScenario(
                module_id=module_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 module_id_list))
        db.session.commit()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    @scenario_decorator
    def put(self):
        """用例场景编辑"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_id = data.get('id')
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_scenario = TestCaseScenario.query.get(scenario_id)
        query_is_public = bool(query_scenario.is_public)

        if not query_scenario:
            return api_result(code=NO_DATA, message=f'场景不存在: {scenario_id}')

        if not query_is_public and query_scenario.creator_id != g.app_user.id:
            return api_result(code=NOT_CREATOR_ERROR, message=NOT_CREATOR_ERROR_MESSAGE)

        if query_scenario.scenario_title != scenario_title:
            if TestCaseScenario.query.join(
                    MidProjectScenario, TestCaseScenario.id == MidProjectScenario.scenario_id
            ).filter(
                TestCaseScenario.is_deleted == 0,
                TestCaseScenario.scenario_title == scenario_title,
                MidProjectScenario.project_id == project_id
            ).all():
                return api_result(code=UNIQUE_ERROR, message=f'用例场景标题: {scenario_title} 已经存在')

        query_scenario.scenario_title = scenario_title
        query_scenario.case_list = case_list
        query_scenario.is_public = is_public
        query_scenario.modifier = g.app_user.username
        query_scenario.modifier_id = g.app_user.id
        query_scenario.remark = remark

        db.session.query(MidVersionScenario).filter(MidVersionScenario.scenario_id == scenario_id).delete(
            synchronize_session=False)

        db.session.query(MidModuleScenario).filter(MidModuleScenario.scenario_id == scenario_id).delete(
            synchronize_session=False)

        if version_list:
            version_id_list = [obj.get('id') for obj in version_list]
            list(map(lambda version_id: db.session.add(
                MidVersionScenario(
                    version_id=version_id, scenario_id=scenario_id, modifier=g.app_user.username,
                    modifier_id=g.app_user.id)),
                     version_id_list))

        if module_list:
            module_id_list = [obj.get('id') for obj in module_list]
            list(map(lambda module_id: db.session.add(
                MidModuleScenario(
                    module_id=module_id, scenario_id=scenario_id, modifier=g.app_user.username,
                    modifier_id=g.app_user.id)),
                     module_id_list))

        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """用例场景删除"""

        data = request.get_json()
        scenario_id = data.get('id')

        query_scenario = TestCaseScenario.query.get(scenario_id)
        if not query_scenario:
            return api_result(code=NO_DATA, message=f'场景不存在:{scenario_id}')

        if query_scenario.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的用例场景！')

        db.session.query(MidProjectScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidVersionScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidModuleScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidTaskScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        query_scenario.modifier_id = g.app_user.id
        query_scenario.modifier = g.app_user.username
        query_scenario.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class CaseScenarioPageApi(MethodView):
    """
    case scenario page api
    POST: 用例场景分页模糊查询
    """

    def post(self):
        """用例场景分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_id = data.get('version_id')
        module_id = data.get('module_id')
        scenario_id = data.get('scenario_id')
        scenario_title = data.get('scenario_title', '')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')
        limit = page_size(page=page, size=size)

        sql = f"""
        SELECT
            *
        FROM
            exile5_test_case_scenario
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile5_test_case_scenario AS A
                    INNER JOIN exile5_test_mid_project_scenario AS B ON A.id = B.scenario_id
                    {'INNER JOIN exile5_test_mid_version_scenario AS C ON A.id = C.scenario_id' if version_id else ''}
                    {'INNER JOIN exile5_test_mid_module_scenario AS D ON A.id = D.scenario_id' if module_id else ''}
                WHERE
                    A.is_deleted = 0
                    AND B.project_id = {project_id}
                    {f'AND C.version_id={version_id}' if version_id else ''}
                    {f'AND D.module_id={module_id}' if module_id else ''}
                )
            AND is_deleted = 0
            AND scenario_title LIKE "%{scenario_title}%"
            {f'AND creator_id={creator_id}' if creator_id else ''}
        ORDER BY
            create_time DESC
        LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            exile5_test_case_scenario
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile5_test_case_scenario AS A
                    INNER JOIN exile5_test_mid_project_scenario AS B ON A.id = B.scenario_id
                    {'INNER JOIN exile5_test_mid_version_scenario AS C ON A.id = C.scenario_id' if version_id else ''}
                    {'INNER JOIN exile5_test_mid_module_scenario AS D ON A.id = D.scenario_id' if module_id else ''}
                WHERE
                    A.is_deleted = 0
                    AND B.project_id = {project_id}
                    {f'AND C.version_id={version_id}' if version_id else ''}
                    {f'AND D.module_id={module_id}' if module_id else ''}
                )
            AND is_deleted = 0
            AND scenario_title LIKE "%{scenario_title}%"
            {f'AND creator_id={creator_id}' if creator_id else ''}
        """

        result_list = project_db.select(sql)
        result_count = project_db.select(sql_count)

        result_data = {
            'records': result_list if result_list else [],
            'now_page': page,
            'total': result_count[0].get('COUNT(*)')
        }

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
