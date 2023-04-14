# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:49 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_data_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case.models import TestCaseData
from app.models.test_variable.models import TestVariable

params_key = [
    ("data_name", "数据名称"),
    # ("request_headers", "headers"),
    # ("request_params", "params"),
    # ("request_body", "body"),
    ("request_body_type", "请求参数类型"),
    ("update_var_list", "关系变量")
]


def check_variable(before_var):
    """检查数据可以中是否存在变量"""

    before_var_init = before_var
    if isinstance(before_var_init, (list, dict)):
        before_var = json.dumps(before_var, ensure_ascii=False)

    result_list = re.findall('\\$\\{([^}]*)', before_var)

    query_done_list = []
    query_none_list = []

    result = {
        "status": True,
        "query_done_list": query_done_list,
        "query_none_list": query_none_list
    }

    if not result_list:
        return result

    for res in result_list:
        sql = """select var_value from exile5_test_variable where var_name='{}';""".format(res)
        query_result = project_db.select(sql=sql, only=True)
        if query_result:
            query_done_list.append(res)
        else:
            query_none_list.append(res)

    if query_none_list:
        result['status'] = False
        return result

    return result


def check_update_var(update_var_list):
    """
    检查需要更新的变量是否存在
    [
        {
            "id": 1,
            "var_source": "response_body",
            "expression": "obj.get('code')",
            "is_expression":0,
            "var_get_key": "code"
        },
        {
            "id": 2,
            "var_source": "response_headers",
            "expression": "obj.get('token')",
            "is_expression":0,
            "var_get_key": "token"
        }
        ...
    ]
    """
    if update_var_list:
        update_var_id_list = set()
        for var in update_var_list:
            if not isinstance(var, dict):
                return False, f'数据异常:{var}-{type(var)}'
            _id = var.get('id')
            var_source = var.get('var_source')
            var_get_key = var.get('var_get_key')
            var_name = var.get('var_name')
            if var_source not in GlobalsDict.var_source_tuple():
                return False, f'变量: {var_name} 更新值来源为空'
            if not var_get_key:
                return False, f'变量: {var_name} 取值的key为空'
            update_var_id_list.add(_id)
        update_var_id_list = list(update_var_id_list)

        query_variable = TestVariable.query.filter(
            TestVariable.is_deleted == 0,
            TestVariable.id.in_(update_var_id_list)
        ).all()
        if not query_variable:
            return False, '变量均不存在'

        query_variable_id_list = [variable.id for variable in query_variable]
        variable_diff = ActionSet.gen_difference(update_var_id_list, query_variable_id_list)
        if variable_diff:
            return False, f'变量: {variable_diff} 不存在'
    return True, 'pass'


def data_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        check_bool, check_msg = RequestParamKeysCheck(data, params_key).result()
        if not check_bool:
            return api_result(code=NO_DATA, message=check_msg)

        update_var_list = data.get('update_var_list', [])
        _update_var_list_bool, _update_var_list_msg = check_update_var(update_var_list=update_var_list)
        if not _update_var_list_bool:
            return api_result(code=NO_DATA, message=_update_var_list_msg)

        # check_result = check_variable(data)
        # if not check_result.get('status'):
        #     return api_result(code=NO_DATA, message="参数不存在:{}".format(check_result.get('query_none_list')))

        return func(*args, **kwargs)

    return wrapper


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
            return api_result(code=NO_DATA, message=f'参数不存在:{req_data_id}')

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_req_case_data.to_json())

    @data_decorator
    def post(self):
        """用例req数据新增"""

        data = request.get_json()
        data_name = data.get('data_name')
        remark = data.get('remark')
        request_params_hash = data.get('request_params_hash', [])
        request_params = gen_request_dict(request_params_hash)
        request_headers_hash = data.get('request_headers_hash', [])
        request_headers = gen_request_dict(request_headers_hash)
        request_body_type = data.get('request_body_type')
        _func = GlobalsDict.request_body_type_func().get(request_body_type)
        request_body_hash = data.get('request_body_hash')
        request_body = _func(request_body_hash)
        is_public = data.get('is_public', True)
        update_var_list = data.get('update_var_list', [])
        data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(
            json.dumps(request_body))

        new_data = TestCaseData(
            data_name=data_name,
            request_params_hash=request_params_hash,
            request_params=request_params,
            request_headers_hash=request_headers_hash,
            request_headers=request_headers,
            request_body_hash=request_body_hash,
            request_body=request_body,
            request_body_type=request_body_type,
            update_var_list=update_var_list,
            is_public=is_public,
            data_size=data_size,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_data.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_data.to_json())

    @data_decorator
    def put(self):
        """用例req数据编辑"""

        data = request.get_json()
        req_data_id = data.get('id')
        remark = data.get('remark')
        is_public = data.get('is_public', True)
        update_var_list = data.get('update_var_list', [])

        query_test_case_data = TestCaseData.query.get(req_data_id)
        if not query_test_case_data:
            return api_result(code=NO_DATA, message=f'参数不存在:{req_data_id}')

        if not bool(is_public) and query_test_case_data.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not bool(query_test_case_data.is_public):
            if query_test_case_data.creator_id != g.app_user.id:
                return api_result(code=BUSINESS_ERROR, message='该参数未开放,只能被创建人修改!')

        data_name = data.get('data_name')
        if query_test_case_data.data_name != data_name:
            if TestCaseData.query.filter_by(data_name=data_name).all():
                return api_result(code=UNIQUE_ERROR, message=f'参数名称: {data_name} 已经存在')

        request_params_hash = data.get('request_params_hash', [])
        request_params = gen_request_dict(request_params_hash)
        request_headers_hash = data.get('request_headers_hash', [])
        request_headers = gen_request_dict(request_headers_hash)
        request_body_type = data.get('request_body_type')
        _func = GlobalsDict.request_body_type_func().get(request_body_type)
        request_body_hash = data.get('request_body_hash')
        request_body = _func(request_body_hash)
        data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(json.dumps(request_body))

        query_test_case_data.data_name = data_name
        query_test_case_data.request_params_hash = request_params_hash
        query_test_case_data.request_params = request_params
        query_test_case_data.request_headers_hash = request_headers_hash
        query_test_case_data.request_headers = request_headers
        query_test_case_data.request_body_hash = request_body_hash
        query_test_case_data.request_body = request_body
        query_test_case_data.request_body_type = request_body_type
        query_test_case_data.update_var_list = update_var_list
        query_test_case_data.is_public = is_public
        query_test_case_data.data_size = data_size
        query_test_case_data.modifier = g.app_user.username
        query_test_case_data.modifier_id = g.app_user.id
        query_test_case_data.remark = remark
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE, data=query_test_case_data.to_json())

    def delete(self):
        """用例req数据删除"""

        data = request.get_json()
        req_data_id = data.get('id')

        query_req_case_data = TestCaseData.query.get(req_data_id)
        if not query_req_case_data:
            return api_result(code=NO_DATA, message=f'req参数不存在:{req_data_id}')

        if query_req_case_data.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的参数！')

        query_req_case_data.modifier_id = g.app_user.id
        query_req_case_data.modifier = g.app_user.username
        query_req_case_data.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class CaseReqDataPageApi(MethodView):
    """
    用例请求参数分页模糊查询 Api
    POST: 用例请求参数分页模糊查询
    """

    def post(self):
        """用例请求参数分页模糊查询"""

        data = request.get_json()
        data_id = data.get('data_id')
        project_id = data.get('project_id')
        version_id = data.get('version_id', 0)
        data_name = data.get('data_name')
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')
        limit = page_size(page=page, size=size)

        sql = f"""
        SELECT
            *
        FROM
            exile5_test_case_data
        WHERE
            is_deleted = 0
            {f'AND data_name LIKE "%{data_name}%"' if data_name else ''}
            {f'AND creator_id={creator_id}' if creator_id else ''}
        ORDER BY
            update_time desc 
        LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            exile5_test_case_data
        WHERE
            is_deleted = 0
            {f'AND data_name LIKE "%{data_name}%"' if data_name else ''}
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
