# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 1:08 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_variable_api.py
# @Software: PyCharm

from types import MethodType, FunctionType

from all_reference import *
from app.api.project_api.project_api import qp
from app.models.test_variable.models import TestVariable, TestVariableHistory


def variable_conversion(var_type, var_value):
    """
    类型转换校验
    :param var_type: 变量类型
    :param var_value: 变量值
    :return:
    """

    d = GlobalsDict.variable_type_dict()
    func = d.get(var_type)
    if isinstance(func, (type, FunctionType)):
        try:
            func(var_value)
            msg = f"值:{var_value}-{type(var_value)} 【func-{func}】"
            print(msg)
            return True, msg
        except BaseException as e:
            msg = f'变量:{var_value} 无法转换至 类型:{var_type}'
            print(f'{msg} ERROR:{e}')
            return False, msg
    elif isinstance(func, MethodType):
        return True, '函数变量'
    else:
        return False, f'函数方法: {func.__class__} 不存在'


def variable_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        data = request.get_json()

        project_id = data.get('project_id')
        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        var_name = data.get('var_name', '').strip()
        if not var_name:
            return api_result(code=REQUIRED, message='变量名称不能为空')

        var_type = data.get('var_type')
        var_value = data.get('var_value')
        if var_type not in GlobalsDict.variable_type_dict():
            return api_result(code=NO_DATA, message=f'变量类型: {var_type} 不存在')

        var_source = data.get('var_source')
        if var_source and var_source not in GlobalsDict.var_source_tuple():
            return api_result(code=NO_DATA, message=f'变量来源: {var_source} 不存在')

        bool_result, result = variable_conversion(var_type=var_type, var_value=var_value)
        if not bool_result:
            return api_result(code=BUSINESS_ERROR, message=result)

        return func(*args, **kwargs)

    return wrapper


class CaseVarApi(MethodView):
    """
    变量
    GET: 变量详情
    POST: 变量新增
    PUT: 变量编辑
    DELETE: 变量删除
    """

    def get(self, var_id):
        """变量详情"""

        query_variable = TestVariable.query.get(var_id)
        if not query_variable:
            return api_result(code=NO_DATA, message='变量不存在')
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_variable.to_json())

    @variable_decorator
    def post(self):
        """变量新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        var_name = data.get('var_name', '').strip()
        var_init_value = data.get('var_init_value', "")
        var_value = data.get('var_value', "")
        var_args = data.get('var_args', {})
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        expression = data.get('expression')
        is_source = data.get('is_source')
        is_expression = data.get('is_expression')
        is_active = data.get('is_active')
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_variable = TestVariable.query.filter_by(project_id=project_id, var_name=var_name, is_deleted=0).first()
        if query_variable:
            return api_result(code=UNIQUE_ERROR, message=f'变量: {var_name} 已存在')

        new_variable = TestVariable(
            project_id=project_id,
            var_name=var_name,
            var_init_value=var_init_value,
            var_value=var_value,
            var_args=var_args,
            var_type=var_type,
            var_source=var_source,
            var_get_key=var_get_key,
            expression=expression,
            is_source=is_source,
            is_expression=is_expression,
            is_active=is_active,
            is_public=is_public,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_variable.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE, data=new_variable.to_json())

    @variable_decorator
    def put(self):
        """变量编辑"""

        data = request.get_json()
        project_id = data.get('project_id')
        var_id = data.get('id')
        var_name = data.get('var_name', '').strip()
        var_init_value = data.get('var_init_value', "")
        var_value = data.get('var_value', "")
        var_args = data.get('var_args', {})
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        expression = data.get('expression')
        is_source = data.get('is_source')
        is_expression = data.get('is_expression')
        is_active = data.get('is_active')
        is_public = data.get('is_public')
        remark = data.get('remark')

        query_variable = TestVariable.query.get(var_id)

        if not query_variable:
            return api_result(code=NO_DATA, message='变量不存在')

        if not bool(is_public) and query_variable.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非创建人，无法修改使用状态')

        if not bool(query_variable.is_public) and query_variable.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='该变量未开放,只能被创建人修改!')

        before_var = query_variable.var_value
        query_var_filter = TestVariable.query.filter_by(project_id=project_id, var_name=var_name, is_deleted=0).first()

        if query_var_filter and query_variable.id != query_var_filter.id:
            return api_result(code=UNIQUE_ERROR, message=f'变量名称:{var_name} 已存在')

        query_variable.var_name = var_name
        query_variable.var_init_value = var_init_value
        query_variable.var_value = var_value
        query_variable.var_args = var_args
        query_variable.var_type = var_type
        query_variable.var_source = var_source
        query_variable.var_get_key = var_get_key
        query_variable.expression = expression
        query_variable.is_source = is_source
        query_variable.is_expression = is_expression
        query_variable.is_active = is_active
        query_variable.is_public = is_public
        query_variable.remark = remark
        query_variable.modifier = g.app_user.username
        query_variable.modifier_id = g.app_user.id
        db.session.commit()

        var_history = TestVariableHistory(
            var_id=var_id,
            update_type="用户操作更新",
            before_var=before_var,
            after_var=var_value,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        db.session.add(var_history)
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE, data=query_variable.to_json())

    def delete(self):
        """变量删除"""

        data = request.get_json()
        var_id = data.get('id')

        query_var = TestVariable.query.get(var_id)
        if not query_var:
            return api_result(code=NO_DATA, message='变量不存在')

        if query_var.creator_id != g.app_user.id:
            return api_result(code=BUSINESS_ERROR, message='非管理员不能删除其他人的变量！')

        query_var.modifier_id = g.app_user.id
        query_var.modifier = g.app_user.username
        query_var.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class CaseVarHistoryApi(MethodView):
    """
    变量变更历史
    """

    def post(self):
        """变量变更记录"""

        data = request.get_json()
        var_id = data.get('var_id')
        page = data.get('page')
        size = data.get('size')

        result = TestVariableHistory.query.filter_by(var_id=var_id).order_by(
            TestVariableHistory.create_time.desc()).paginate(
            page=int(page),
            per_page=int(size),
            error_out=False
        )
        result_list = []
        total = result.total
        for res in result.items:
            result_list.append(res.to_json())
        result_data = {
            'records': result_list,
            'now_page': page,
            'total': total
        }
        return api_result(code=200, message=SUCCESS_MESSAGE, data=result_data)


class CaseVarPageApi(MethodView):
    """
    case variable page api
    POST: 变量分页模糊查询
    """

    def post(self):
        """变量分页模糊查询"""

        data = request.get_json()
        var_id = data.get('id')
        project_id = data.get('project_id')
        var_name = data.get('var_name')
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile5_test_variable  
        WHERE 
        id = "id" 
        and var_name LIKE"%B1%" 
        and is_deleted = 0
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": var_id,
            "project_id": project_id,
            "var_type": var_type,
            "var_source": var_source,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestVariable,
            field_list=['var_name'],
            query_list=[var_name],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
