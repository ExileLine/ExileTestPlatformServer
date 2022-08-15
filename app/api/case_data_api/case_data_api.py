# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:49 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_data_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_case.models import TestCaseData

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
        sql = """select var_value from exile_test_variable where var_name='{}';""".format(res)
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
            "id": 3,
            "var_source": "resp_data",
            "expression": "obj.get('code')",
            "is_expression":0,
            "var_get_key": "code"
        },
        ...
    ]
    """
    if update_var_list:
        update_var_id_list = list(set(map(lambda x: x.get('id') if isinstance(x, dict) else 0, update_var_list)))
        if 0 in update_var_id_list:
            update_var_id_list.remove(0)

        if len(update_var_list) == 1:
            sql = f"""SELECT id FROM exile_test_variable WHERE id = {update_var_list[-1].get('id')} and var_source is not null;"""
            logger.success(sql)
        else:
            sql = f"""SELECT id FROM exile_test_variable WHERE id in {tuple(update_var_id_list)} and var_source is not null;"""
            logger.success(sql)

        query_result = project_db.select(sql)
        if not query_result:
            return False, '静态变量缺少来源,不能作为关系变量使用'

        query_result_id = list(map(lambda x: x.get('id'), query_result))
        cj = ActionSet.gen_difference(update_var_id_list, query_result_id)
        if cj:
            logger.error("cj:{}".format(cj))
            return False, f'更新的变量不存在:{cj}'
    return True, 'pass'


def data_decorator(deco_param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            request_data = data.get('request_data', {})

            if not isinstance(request_data, dict) or not request_data:
                return api_result(code=DATA_ERROR, message='请求参数错误')

            check_bool, check_msg = RequestParamKeysCheck(request_data, params_key).result()
            if not check_bool:
                return api_result(code=NO_DATA, message=check_msg)

            is_public = request_data.get('is_public')
            if is_public and not isinstance(is_public, bool):
                return api_result(code=TYPE_ERROR, message=f'标识错误: {is_public}')

            update_var_list = request_data.get('update_var_list', [])
            _update_var_list_bool, _update_var_list_msg = check_update_var(update_var_list=update_var_list)
            if not _update_var_list_bool:
                return api_result(code=NO_DATA, message=_update_var_list_msg)

            # check_result = check_variable(data)
            # if not check_result.get('status'):
            #     return api_result(code=400, message="参数不存在:{}".format(check_result.get('query_none_list')))

            return func(*args, **kwargs)

        return wrapper

    return decorator


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

        return api_result(code=SUCCESS, message='操作成功', data=query_req_case_data.to_json())

    @data_decorator("post")
    def post(self):
        """用例req数据新增"""

        data = request.get_json()
        request_data = data.get('request_data', {})
        data_name = request_data.get('data_name')
        request_params_hash = request_data.get('request_params_hash', []) or []
        request_headers_hash = request_data.get('request_headers_hash', []) or []
        request_body_hash = request_data.get('request_body_hash', []) or []
        request_params = gen_request_dict(request_params_hash)
        request_headers = gen_request_dict(request_headers_hash)
        request_body = gen_request_dict(request_body_hash)
        request_body_type = request_data.get('request_body_type')
        is_public = request_data.get('is_public', True)
        update_var_list = request_data.get('update_var_list', [])
        data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(
            json.dumps(request_body))

        new_data = TestCaseData(
            data_name=data_name,
            request_params=request_params,
            request_params_hash=request_params_hash,
            request_headers=request_headers,
            request_headers_hash=request_headers_hash,
            request_body=request_body,
            request_body_hash=request_body_hash,
            request_body_type=request_body_type,
            update_var_list=update_var_list,
            is_public=is_public,
            data_size=data_size,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_data.save()
        return api_result(code=POST_SUCCESS, message='创建成功', data=new_data.to_json())

        """
        data_list = data.get('data_list', [])
        new_data_list = []

        if not isinstance(data_list, list) or not data_list:
            return api_result(code=DATA_ERROR, message='请求参数错误')

        for index, d in enumerate(data_list):
            is_public = d.get('is_public', True)

            # check_result = check_variable(d)
            # if not check_result.get('status'):
            #     return api_result(code=400, message="参数不存在:{}".format(check_result.get('query_none_list')))

            check_bool, check_msg = RequestParamKeysCheck(d, params_key).result()
            if not check_bool:
                return api_result(code=NO_DATA, message=check_msg)

            update_var_list = d.get('update_var_list', [])
            _update_var_list_bool, _update_var_list_msg = check_update_var(update_var_list=update_var_list)
            if not _update_var_list_bool:
                return api_result(code=NO_DATA, message=_update_var_list_msg)

            data_name = d.get('data_name')
            request_params_hash = d.get('request_params_hash', {}) or {}
            request_headers_hash = d.get('request_headers_hash', {}) or {}
            request_body_hash = d.get('request_body_hash', {}) or {}
            request_params = gen_request_dict(request_params_hash)
            request_headers = gen_request_dict(request_headers_hash)
            request_body = gen_request_dict(request_body_hash)
            request_body_type = d.get('request_body_type')
            data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(
                json.dumps(request_body))

            new_data = TestCaseData(
                data_name=data_name,
                request_params=request_params,
                request_params_hash=request_params_hash,
                request_headers=request_headers,
                request_headers_hash=request_headers_hash,
                request_body=request_body,
                request_body_hash=request_body_hash,
                request_body_type=request_body_type,
                update_var_list=update_var_list,
                is_public=is_public,
                data_size=data_size,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_data)
            new_data_list.append(new_data)
        db.session.commit()
        # TODO 后面将入参的list改为dict
        result = []
        for new_data in new_data_list:
            new_data.to_json()['id'] = new_data.id
            result.append(new_data.to_json())
        return api_result(code=POST_SUCCESS, message='创建成功', data=result)
        """

    @data_decorator("put")
    def put(self):
        """用例req数据编辑"""

        data = request.get_json()
        req_data_id = data.get('id')
        request_data = data.get('request_data', {})
        is_public = request_data.get('is_public', True)
        update_var_list = request_data.get('update_var_list', [])

        query_test_case_data = TestCaseData.query.get(req_data_id)
        if not query_test_case_data:
            return api_result(code=NO_DATA, message=f'参数不存在:{req_data_id}')

        if not bool(is_public) and query_test_case_data.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not bool(query_test_case_data.is_public):
            if query_test_case_data.creator_id != g.app_user.id:
                return api_result(code=BUSINESS_ERROR, message='该参数未开放,只能被创建人修改!')

        data_name = request_data.get('data_name')
        if query_test_case_data.data_name != data_name:
            if TestCaseData.query.filter_by(data_name=data_name).all():
                return api_result(code=UNIQUE_ERROR, message=f'参数名称: {data_name} 已经存在')

        request_params_hash = request_data.get('request_params_hash', {}) or {}
        request_headers_hash = request_data.get('request_headers_hash', {}) or {}
        request_body_hash = request_data.get('request_body_hash', {}) or {}
        request_params = gen_request_dict(request_params_hash)
        request_headers = gen_request_dict(request_headers_hash)
        request_body = gen_request_dict(request_body_hash)
        request_body_type = request_data.get('request_body_type')
        data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(json.dumps(request_body))

        query_test_case_data.data_name = data_name
        query_test_case_data.request_params = request_params
        query_test_case_data.request_params_hash = request_params_hash
        query_test_case_data.request_headers = request_headers
        query_test_case_data.request_headers_hash = request_headers_hash
        query_test_case_data.request_body = request_body
        query_test_case_data.request_body_hash = request_body_hash
        query_test_case_data.request_body_type = request_body_type
        query_test_case_data.update_var_list = update_var_list
        query_test_case_data.is_public = is_public
        query_test_case_data.data_size = data_size
        query_test_case_data.modifier = g.app_user.username
        query_test_case_data.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message='编辑成功')

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
        return api_result(code=DEL_SUCCESS, message='删除成功')


class CaseReqDataPageApi(MethodView):
    """
    case req data page api
    POST: 用例req数据分页模糊查询
    """

    def post(self):
        """用例req数据分页模糊查询"""

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
            exile_test_case_data
        WHERE
            is_deleted = 0
            {f'AND data_name LIKE "%{data_name}%"' if data_name else ''}
            {f'AND creator_id={creator_id}' if creator_id else ''}
        ORDER BY
            data_size 
        LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            exile_test_case_data
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

        return api_result(code=SUCCESS, message='操作成功', data=result_data)
