# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:38 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_scenario_api.py
# @Software: PyCharm

from functools import wraps

from all_reference import *
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProject, TestProjectVersion, TestModuleApp, MidProjectAndScenario, \
    MidVersionAndScenario, MidTaskAndScenario, MidModuleAndScenario
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

    sql = f"""SELECT * FROM exile_test_case WHERE id in {tuple(case_id_list)} ORDER BY FIELD(id,{','.join(list(map(str, case_id_list)))});"""
    result = project_db.select(sql)

    if len(set(case_id_list)) != len(case_id_list):
        return zip_case(before_id_list=case_id_list, before_obj_list=result)
    else:
        return result


def scenario_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        query_project = TestProject.query.get(project_id)

        if not query_project:
            return api_result(code=400, message=f'项目: {project_id} 不存在')

        if version_list:
            _bool, _msg = new_check_version(project_id, version_list)
            if not _bool:
                return api_result(code=400, message=f'版本迭代:{_msg}不存在或不在项目:{project_id}下关联')

        if module_list:
            _bool, _msg = new_check_module(project_id, module_list)
            if not _bool:
                return api_result(code=400, message=f'模块:{_msg}不存在或不在项目:{project_id}下关联')

        if not scenario_title:
            return api_result(code=400, message='场景名称不能为空')

        if not case_list or len(case_list) <= 1:
            return api_result(code=400, message='用例列表不能为空,或需要一条以上的用例组成')

        if len(set(map(lambda obj: obj.get('index'), case_list))) != len(case_list):
            return api_result(code=400, message='用例排序不能为空或重复')

        if False in list(map(lambda obj: obj.get('sleep') if obj.get('sleep', 0) <= 30 else False, case_list)):
            return api_result(code=400, message='执行后等待时间不能大于30秒')

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
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

        result = query_scenario.to_json()
        case_id_list = result.get('case_list')

        if not case_id_list:
            return api_result(code=400, message='异常的数据')

        # TODO 后面新增中间表后修改这个逻辑
        sorted_case_id_list = sorted(case_id_list, key=lambda x: x.get("index", x.get('case_id')), reverse=True)

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
            return api_result(code=400, message='数据异常')

        version_id_list = [m.version_id for m in MidVersionAndScenario.query.filter_by(scenario_id=scenario_id).all()]
        version_list = [m.to_json() for m in
                        TestProjectVersion.query.filter(TestProjectVersion.id.in_(version_id_list)).all()]

        module_id_list = [m.module_id for m in MidModuleAndScenario.query.filter_by(scenario_id=scenario_id).all()]
        module_list = [m.to_json() for m in TestModuleApp.query.filter(TestModuleApp.id.in_(module_id_list)).all()]

        result['case_list'] = case_list
        result["version_list"] = version_list
        result["module_list"] = module_list
        return api_result(code=200, message='操作成功', data=result)

    @scenario_decorator
    def post(self):
        """用例场景新增"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        query_scenario = TestCaseScenario.query.filter_by(scenario_title=scenario_title).first()

        if query_scenario:
            return api_result(code=400, message=f'用例场景标题: {scenario_title} 已经存在')

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

        version_id_list = [obj.get('id') for obj in version_list]
        module_id_list = [obj.get('id') for obj in module_list]

        mid_pc = MidProjectAndScenario(
            project_id=project_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id
        )
        db.session.add(mid_pc)
        list(map(lambda version_id: db.session.add(
            MidVersionAndScenario(
                version_id=version_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 version_id_list))
        list(map(lambda module_id: db.session.add(
            MidModuleAndScenario(
                module_id=module_id, scenario_id=scenario_id, creator=g.app_user.username, creator_id=g.app_user.id)),
                 module_id_list))
        db.session.commit()
        return api_result(code=201, message='创建成功')

    @scenario_decorator
    def put(self):
        """用例场景编辑"""

        data = request.get_json()
        project_id = data.get('project_id', 0)
        version_list = data.get('version_list', [])
        module_list = data.get('module_list', [])
        scenario_id = data.get('id')
        scenario_title = data.get('scenario_title', '').strip()
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message=f'场景id:{scenario_id}数据不存在')

        if query_scenario.scenario_title != scenario_title:
            if TestCaseScenario.query.filter_by(scenario_title=scenario_title).all():
                return api_result(code=400, message=f'用例场景:{scenario_title} 已经存在')

        query_scenario.scenario_title = scenario_title
        query_scenario.case_list = case_list
        query_scenario.is_shared = is_shared
        query_scenario.is_public = is_public
        query_scenario.modifier = g.app_user.username
        query_scenario.modifier_id = g.app_user.id

        db.session.query(MidVersionAndScenario).filter(MidVersionAndScenario.scenario_id == scenario_id).delete(
            synchronize_session=False)

        db.session.query(MidModuleAndScenario).filter(MidModuleAndScenario.scenario_id == scenario_id).delete(
            synchronize_session=False)

        if version_list:
            version_id_list = [obj.get('id') for obj in version_list]
            list(map(lambda version_id: db.session.add(
                MidVersionAndScenario(
                    version_id=version_id, scenario_id=scenario_id, modifier=g.app_user.username,
                    modifier_id=g.app_user.id)),
                     version_id_list))

        if module_list:
            module_id_list = [obj.get('id') for obj in module_list]
            list(map(lambda module_id: db.session.add(
                MidModuleAndScenario(
                    module_id=module_id, scenario_id=scenario_id, modifier=g.app_user.username,
                    modifier_id=g.app_user.id)),
                     module_id_list))

        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例场景删除"""

        data = request.get_json()
        scenario_id = data.get('id')
        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message=f'场景id:{scenario_id}数据不存在')

        if query_scenario.creator_id != g.app_user.id:
            return api_result(code=400, message='非管理员不能删除其他人的用例场景！')

        db.session.query(MidProjectAndScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidVersionAndScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidModuleAndScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
        db.session.query(MidTaskAndScenario).filter_by(scenario_id=scenario_id).delete(synchronize_session=False)
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
            exile_test_case_scenario
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile_test_case_scenario AS A
                    INNER JOIN exile_test_mid_project_scenario AS B ON A.id = B.scenario_id
                    {'INNER JOIN exile_test_mid_version_iter_scenario AS C ON A.id = C.scenario_id' if version_id else ''}
                    {'INNER JOIN exile_test_mid_module_scenario AS D ON A.id = D.scenario_id' if module_id else ''}
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
            exile_test_case_scenario
        WHERE
            id in( SELECT DISTINCT
                    A.id FROM exile_test_case_scenario AS A
                    INNER JOIN exile_test_mid_project_scenario AS B ON A.id = B.scenario_id
                    {'INNER JOIN exile_test_mid_version_iter_scenario AS C ON A.id = C.scenario_id' if version_id else ''}
                    {'INNER JOIN exile_test_mid_module_scenario AS D ON A.id = D.scenario_id' if module_id else ''}
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

        return api_result(code=200, message='操作成功', data=result_data)
