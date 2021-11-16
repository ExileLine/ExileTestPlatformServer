# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_assert.models import TestCaseDataAssBind


def check_method(current_method):
    """检查method"""
    if current_method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
        return current_method.upper()
    else:
        return False


p = [
    ("case_name", "用例名称"),
    ("request_method", "请求方式"),
    ("request_base_url", "base url"),
    ("request_url", "url")
]


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
        request_base_url = data.get('request_base_url')
        request_url = data.get('request_url')
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        check_bool, check_msg = RequestParamKeysCheck(data, p).ck()
        if not check_bool:
            return api_result(code=400, message=check_msg)

        request_method_result = check_method(current_method=request_method)

        if not request_method_result:
            return api_result(code=400, message='请求方式:{} 不存在'.format(request_method))

        query_case = TestCase.query.filter_by(case_name=case_name).first()

        if query_case:
            return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        new_test_case = TestCase(
            case_name=case_name,
            request_method=request_method_result,
            request_base_url=request_base_url,
            request_url=request_url,
            is_shared=is_shared,
            is_public=is_public if isinstance(is_public, bool) else True,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_test_case.save()
        data['id'] = new_test_case.id
        return api_result(code=201, message='创建成功', data=data)

    def put(self):
        """用例编辑"""

        data = request.get_json()
        case_id = data.get('id')
        case_name = data.get('case_name')
        request_method = data.get('request_method')
        request_base_url = data.get('request_base_url')
        request_url = data.get('request_url')
        is_shared = data.get('is_shared', 0)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        check_bool, check_msg = RequestParamKeysCheck(data, p).ck()
        if not check_bool:
            return api_result(code=400, message=check_msg)

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}数据不存在'.format(case_id))

        if not bool(query_case.is_public):
            if query_case.creator_id != g.app_user.id:
                return api_result(code=400, message='该用例未开放,只能被创建人修改!')

        if query_case.case_name != case_name:
            if TestCase.query.filter_by(case_name=case_name).all():
                return api_result(code=400, message='用例名称:{} 已经存在'.format(case_name))

        query_case.case_name = case_name
        query_case.request_method = request_method
        query_case.request_base_url = request_base_url
        query_case.request_url = request_url
        query_case.is_shared = is_shared
        query_case.is_public = is_public if isinstance(is_public, bool) else True
        query_case.remark = remark
        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id
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
        query_case.modifier = g.app_user.username
        query_case.modifier_id = g.app_user.id
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
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_case  
        WHERE 
        id LIKE"%%" 
        and case_name LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestCase,
            field_list=['id', 'case_name', 'creator_id'],
            query_list=[case_id, case_name, creator_id],
            is_deleted=is_deleted,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)


class CaseCopyApi(MethodView):
    """
    用例复制Api
    POST: 用例复制
    """

    def post(self):
        """用例复制"""

        data = request.get_json()
        case_id = data.get('case_id')

        query_case = TestCase.query.get(case_id)

        if not query_case:
            return api_result(code=400, message='用例id:{}不存在'.format(case_id))

        new_test_case = TestCase(
            case_name=query_case.case_name,
            request_method=query_case.request_method,
            request_base_url=query_case.request_base_url,
            request_url=query_case.request_url,
            is_shared=query_case.is_shared,
            is_public=query_case.is_public,
            remark="用例: {}-{} 的复制".format(query_case.id, query_case.case_name),
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_test_case.save()
        new_test_case_id = new_test_case.id

        query_bind = TestCaseDataAssBind.query.filter_by(case_id=case_id).all()

        if query_bind:
            for index, d in enumerate(query_bind, 1):
                new_bind = TestCaseDataAssBind(
                    case_id=new_test_case_id,
                    data_id=d.data_id,
                    ass_resp_id_list=d.ass_resp_id_list,  # TODO 检查 ass_resp_id_list 中的 id 是否存在
                    ass_field_id_list=d.ass_field_id_list,  # TODO 检查 ass_field_id_list 中的 id 是否存在
                    creator=g.app_user.username,
                    creator_id=g.app_user.id,
                    remark="用例复制生成"
                )
                db.session.add(new_bind)
            db.session.commit()

        return api_result(code=200, message='操作成功')
