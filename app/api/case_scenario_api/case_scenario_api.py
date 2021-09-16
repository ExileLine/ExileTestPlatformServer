# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_scenario_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario


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
        case_obj_list = []
        if case_id_list:
            for case in case_id_list:
                query_case = TestCase.query.get(case)
                if query_case:
                    case_obj_list.append(query_case.to_json())
            result['case_list'] = case_obj_list
        return api_result(code=200, message='操作成功', data=result)

    def post(self):
        """用例场景新增"""

        data = request.get_json()
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])

        query_scenario = TestCaseScenario.query.filter_by(scenario_title=scenario_title).first()

        if query_scenario:
            return api_result(code=400, message='用例场景标题:{} 已经存在'.format(scenario_title))

        if not case_list or len(case_list) <= 1:
            return api_result(code=400, message='用例列表不能为空,或需要一条以上的用例组成')

        new_scenario = TestCaseScenario(
            scenario_title=scenario_title,
            case_list=case_list,
            creator='调试',
            creator_id=1
        )
        new_scenario.save()
        return api_result(code=201, message='创建成功')

    def put(self):
        """用例场景编辑"""

        data = request.get_json()
        scenario_id = data.get('scenario_id')
        scenario_title = data.get('scenario_title')
        case_list = data.get('case_list', [])

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
        query_scenario.modifier = "调试"
        query_scenario.modifier_id = 1
        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例场景删除"""

        data = request.get_json()
        scenario_id = data.get('scenario_id')
        query_scenario = TestCaseScenario.query.get(scenario_id)

        if not query_scenario:
            return api_result(code=400, message='场景id:{}数据不存在'.format(scenario_id))

        query_scenario.is_deleted = query_scenario.id
        query_scenario.modifier = "调试"
        query_scenario.modifier_id = 1
        db.session.commit()
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
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_test_case_scenario  
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
