# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_api.py
# @Software: PyCharm

from app.all_reference import *
from app.models.test_case.models import TestCase, TestCaseData, TestCaseDataAssBind
from app.models.test_variable.models import TestVariable


def check_var(var_list):
    """检查使用的变量是否存在"""
    # var_list = d.get('var_list')
    if var_list:
        query_var_list = TestVariable.query.filter(TestVariable.var_name.in_(var_list)).all()
        if not query_var_list:
            # return api_result(code=400, message='应用的变量:{}不存在,请先创建创建'.format(var_list))
            return False, '应用的变量:{}不存在,请先创建创建'.format(var_list)

        l2 = [v.var_name for v in query_var_list]
        r = [i for i in var_list if i not in l2]
        if r:
            # return api_result(code=400, message='应用的变量:{}不存在,请先创建创建'.format(r))
            return False, '应用的变量:{}不存在,请先创建创建'.format(r)

    return True, 'pass'


def check_method(current_method):
    """检查method"""
    if current_method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
        return current_method.upper()
    else:
        return False


class CaseApi(MethodView):
    """
    用例Api
    GET: 用例详情
    POST: 用例新增
    PUT: 用例编辑
    DELETE: 用例删除
    """

    def get(self, case_id):
        """用例详情"""

        # Todo 用例,数据,变量,resp断言,field断言
        return api_result(code=200, message='test case detail')

    def post(self):
        """用例新增"""

        data = request.get_json()
        case_name = data.get('case_name')
        request_method = data.get('request_method')
        request_url = data.get('request_url')
        var_list = data.get('var_list', [])
        remark = data.get('remark')

        _bool, _msg = check_var(var_list=var_list)
        request_method_result = check_method(current_method=request_method)

        if not _bool:
            return api_result(code=400, message=_msg)

        if not request_method_result:
            return api_result(code=400, message='请求方式:{} 不存在'.format(request_method))

        query_case = TestCase.query.filter_by(case_name=case_name).first()

        if query_case:
            return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        new_test_case = TestCase(
            case_name=case_name,
            request_method=request_method_result,
            request_url=request_url,
            remark=remark,
            creator='调试',
            creator_id=1,
        )
        db.session.add(new_test_case)
        db.session.commit()
        return api_result(code=201, message='创建成功')

    def put(self):
        """用例编辑"""

        data = request.get_json()
        case_id = data.get('case_id')
        case_name = data.get('case_name')
        request_method = data.get('request_method')
        request_url = data.get('request_url')
        var_list = data.get('var_list', [])
        remark = data.get('remark')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}数据不存在'.format(case_id))

        _bool, _msg = check_var(var_list=var_list)

        if not _bool:
            return api_result(code=400, message=_msg)

        if query_case.case_name != case_name:
            if TestCase.query.filter_by(case_name=case_name).all():
                return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        query_case.case_name = case_name
        query_case.request_method = request_method
        query_case.request_url = request_url
        query_case.remark = remark
        query_case.modifier = "调试"
        query_case.modifier_id = 1
        db.session.commit()
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例删除"""

        data = request.get_json()
        case_id = data.get('case_id')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}数据不存在'.format(case_id))

        query_case.is_deleted = query_case.id
        query_case.modifier = "调试"
        query_case.modifier_id = 1
        db.session.commit()
        return api_result(code=204, message='删除成功')


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
            return api_result(code=400, message='用例req数据id:{}数据不存在'.format(req_data_id))

        return api_result(code=200, message='删除成功', data=query_req_case_data.to_json())

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


class CaseBindDataApi(MethodView):
    """
    用例配置数据Api
    """

    def post(self):
        """用例配置数据"""

        data = request.get_json()
        case_id = data.get('case_id')
        var_ids = data.get('var_ids', [])

        if not isinstance(var_ids, list) or not var_ids:
            return api_result()

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id不存在:{}'.format(case_id))

        query_var_list = TestVariable.query.filter(TestVariable.id.in_(var_ids)).all()

        query_var_ids = [v.to_json().get('id') for v in query_var_list]

        set_result = list(set(var_ids).difference(set(query_var_ids)))
        if set_result:
            return api_result(code=400, message='变量不存在:{}'.format(set_result))

        # Todo 入库