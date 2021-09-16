# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:49 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_data_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCaseData
from app.api.case_api.case_api import check_var


class CaseReqDataApi(MethodView):
    """
    用例req数据Api
    GET: 用例req数据详情
    POST: 用例req数据新增
    PUT: 用例req数据编辑
    DELETE: 用例req数据删除
    """

    def get(self, req_data_id):
        """用例req数据详情"""

        query_req_case_data = TestCaseData.query.get(req_data_id)

        if not query_req_case_data:
            return api_result(code=400, message='用例req_id:{}数据不存在'.format(req_data_id))

        return api_result(code=200, message='操作成功', data=query_req_case_data.to_json())

    def post(self):
        """用例req数据新增"""

        data = request.get_json()
        data_list = data.get('data_list', [])

        if not isinstance(data_list, list) or not data_list:
            return ab_code(400)

        for d in data_list:
            var_list = d.get('var_list')
            _bool, _msg = check_var(var_list=var_list)

            if not _bool:
                return api_result(code=400, message=_msg)

            new_case_data = TestCaseData(
                data_name=d.get('data_name'),
                request_params=d.get('request_params'),
                request_headers=d.get('request_headers'),
                request_body=d.get('request_body'),
                request_body_type=d.get('request_body_type'),
                var_list=var_list,
                creator='调试',
                creator_id=1
            )
            db.session.add(new_case_data)

        db.session.commit()

        return api_result(code=201, message='创建成功')

    def put(self):
        """用例req数据编辑"""

        data = request.get_json()
        req_data_id = data.get('req_data_id')
        req_data_json = data.get('req_data_json', {})

        if isinstance(req_data_json, dict):
            _check_bool = check_keys(
                req_data_json, 'data_name', 'request_params', 'request_headers', 'request_body', 'request_body_type',
                'var_list'
            )
        else:
            _check_bool = False

        if not _check_bool:
            return ab_code(400)

        query_test_case = TestCaseData.query.get(req_data_id)

        if not query_test_case:
            return api_result(code=400, message='用例req数据id:{}数据不存在'.format(req_data_id))

        for d in [req_data_json]:
            var_list = d.get('var_list')
            _bool, _msg = check_var(var_list=var_list)

            if not _bool:
                return api_result(code=400, message=_msg)

            data_name = d.get('data_name')

            if query_test_case.data_name != data_name:
                if TestCaseData.query.filter_by(data_name=data_name).all():
                    return api_result(code=400, message='测试数据名称:{} 已经存在'.format(data_name))

            query_test_case.data_name = data_name,
            query_test_case.request_params = d.get('request_params'),
            query_test_case.request_headers = d.get('request_headers'),
            query_test_case.request_body = d.get('request_body'),
            query_test_case.request_body_type = d.get('request_body_type'),
            query_test_case.var_list = var_list,
            query_test_case.modifier = "调试"
            query_test_case.modifier_id = 1
            db.session.commit()

            return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例req数据删除"""

        data = request.get_json()
        req_data_id = data.get('req_data_id')

        query_req_case_data = TestCaseData.query.get(req_data_id)

        if not query_req_case_data:
            return api_result(code=400, message='用例req数据id:{}数据不存在'.format(req_data_id))

        query_req_case_data.is_deleted = query_req_case_data.id
        query_req_case_data.modifier = "调试"
        query_req_case_data.modifier_id = 1
        db.session.commit()
        return api_result(code=204, message='删除成功')


class CaseReqDataPageApi(MethodView):
    """
    case req data page api
    POST: 用例req数据分页模糊查询
    """

    def post(self):
        """用例req数据分页模糊查询"""

        data = request.get_json()
        data_id = data.get('data_id')
        data_name = data.get('data_name')
        is_deleted = data.get('is_deleted', False)
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_test_case_data  
        WHERE 
        id LIKE"%%" 
        and case_name LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCaseData,
            field_list=['id', 'data_name'],
            query_list=[data_id, data_name],
            is_deleted=is_deleted,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)
