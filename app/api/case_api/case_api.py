# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
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

        result = query_case_zip(case_id=case_id)

        if not result:
            return api_result(code=400, message='用例id:{}不存在'.format(case_id))

        return api_result(code=200, message='操作成功', data=result)

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
        new_test_case.save()
        # db.session.add(new_test_case)
        # db.session.commit()
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


class CasePageApi(MethodView):
    """
    case page api
    POST: 用例分页模糊查询
    """

    def post(self):
        """用例分页模糊查询"""

        data = request.get_json()
        case_id = data.get('case_id')
        case_name = data.get('case_name')
        is_deleted = data.get('is_deleted', False)
        page, size = page_size(**data)

        sql = """
        SELECT * 
        FROM exilic_test_case  
        WHERE 
        id LIKE"%%" 
        and case_name LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCase,
            field_list=['id', 'case_name'],
            query_list=[case_id, case_name],
            is_deleted=is_deleted,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)
