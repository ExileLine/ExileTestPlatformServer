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
        version_id_list = data.get('version_id_list', [])
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        query_scenario = TestCaseScenario.query.filter_by(scenario_title=scenario_title).first()

        if not isinstance(version_id_list, list) or not version_id_list:
            return api_result(code=400, message='版本迭代不能为空')

        if not check_version(version_id_list):
            return api_result(code=400, message='版本迭代不存在')

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

        for version_obj in version_id_list:
            version_id = version_obj.get('id')
            new_mid = MidProjectVersionAndScenario(
                version_id=version_id,
                scenario_id=scenario_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_mid)

        db.session.commit()

        return api_result(code=201, message='创建成功')

    def put(self):
        """用例场景编辑"""

        data = request.get_json()
        version_id_list = data.get('version_id_list', [])
        scenario_id = data.get('id')
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)

        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not isinstance(version_id_list, list) or not version_id_list:
            return api_result(code=400, message='版本迭代不能为空')

        if not check_version(version_id_list):
            return api_result(code=400, message='版本迭代不存在')

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

        new_version_id_list = [version_obj.get('id') for version_obj in version_id_list]

        query_mid_all = MidProjectVersionAndScenario.query.filter_by(scenario_id=scenario_id).all()

        remain_list = []

        for q in query_mid_all:
            if q.version_id not in new_version_id_list:
                q.is_deleted = q.id
                q.modifier = g.app_user.username
                q.modifier_id = g.app_user.id
                q.remark = "源数据差集(逻辑删除)"
            else:
                remain_list.append(q.version_id)

        jj = ActionSet.gen_intersection(remain_list, new_version_id_list)
        cj = ActionSet.gen_difference(new_version_id_list, remain_list)

        for version_id in jj:  # 激活
            update_mid = MidProjectVersionAndScenario.query.filter_by(version_id=version_id,
                                                                      scenario_id=scenario_id).first()
            update_mid.modifier = g.app_user.username
            update_mid.modifier_id = g.app_user.id
            update_mid.is_deleted = 0
            update_mid.remark = '交集(激活)'

        for version_id in cj:  # 创建新的
            new_mid = MidProjectVersionAndScenario(
                version_id=version_id,
                scenario_id=scenario_id,
                creator=g.app_user.username,
                creator_id=g.app_user.id,
                remark="新数据差集(创建)"
            )
            db.session.add(new_mid)

        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例场景删除"""

        data = request.get_json()
        scenario_id = data.get('scenario_id')
        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

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
        scenario_id = data.get('scenario_id')
        scenario_title = data.get('scenario_title')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_case_scenario  
        WHERE 
        id LIKE"%%" 
        and scenario_title LIKE"%A%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCaseScenario,
            field_list=['id', 'scenario_title'],
            query_list=[scenario_id, scenario_title],
            is_deleted=is_deleted,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
