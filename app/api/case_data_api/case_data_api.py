# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:49 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_data_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCaseData
from app.api.case_api.case_api import check_var, check_update_var

p = [
    ("data_name", "数据名称"),
    ("request_headers", "headers"),
    ("request_params", "params"),
    ("request_body", "body"),
    ("request_body_type", "请求参数类型"),
    ("var_list", "变量"),
    ("update_var_list", "关系变量")
]


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
            is_public = d.get('is_public', True)
            _bool, _msg = check_var(var_list=var_list)

            check_bool, check_msg = RequestParamKeysCheck(d, p).ck()
            if not check_bool:
                return api_result(code=400, message=check_msg)

            if not _bool:
                return api_result(code=400, message=_msg)

            new_case_data = TestCaseData(
                data_name=d.get('data_name'),
                request_params=d.get('request_params'),
                request_headers=d.get('request_headers'),
                request_body=d.get('request_body'),
                request_body_type=d.get('request_body_type'),
                var_list=var_list,
                update_var_list=d.get('update_var_list', []),
                is_public=is_public if isinstance(is_public, bool) else True,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_case_data)

        db.session.commit()

        return api_result(code=201, message='创建成功')

    def put(self):
        """用例req数据编辑"""

        data = request.get_json()
        req_data_id = data.get('id')
        req_data_json = data.get('req_data_json', {})

        if not isinstance(req_data_json, dict):
            return api_result(code=400, message="req_data_json 错误")

        check_bool, check_msg = RequestParamKeysCheck(req_data_json, p).ck()
        if not check_bool:
            return api_result(code=400, message=check_msg)

        query_test_case_data = TestCaseData.query.get(req_data_id)

        if not query_test_case_data:
            return api_result(code=400, message='用例req数据id:{}数据不存在'.format(req_data_id))

        var_list = req_data_json.get('var_list')
        _var_list_bool, _var_list_msg = check_var(var_list=var_list)

        if not _var_list_bool:
            return api_result(code=400, message=_var_list_msg)

        # TODO
        # update_var_list = req_data_json.get('update_var_list')
        # _update_var_list_bool, _update_var_list_msg = check_update_var(update_var_list=update_var_list)
        #
        # if not _update_var_list_bool:
        #     return api_result(code=400, message=_update_var_list_msg)

        data_name = req_data_json.get('data_name')

        if query_test_case_data.data_name != data_name:
            if TestCaseData.query.filter_by(data_name=data_name).all():
                return api_result(code=400, message='测试数据名称:{} 已经存在'.format(data_name))

        is_public = req_data_json.get('is_public')

        query_test_case_data.data_name = data_name
        query_test_case_data.request_headers = req_data_json.get('request_headers')
        query_test_case_data.request_params = req_data_json.get('request_params')
        query_test_case_data.request_body = req_data_json.get('request_body')
        query_test_case_data.request_body_type = req_data_json.get('request_body_type')
        query_test_case_data.var_list = var_list
        query_test_case_data.update_var_list = update_var_list
        query_test_case_data.is_public = is_public if isinstance(is_public, bool) else True,
        query_test_case_data.modifier = g.app_user.username
        query_test_case_data.modifier_id = g.app_user.id
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
        query_req_case_data.modifier = g.app_user.username
        query_req_case_data.modifier_id = g.app_user.id
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
        page = data.get('page')
        size = data.get('size')

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
