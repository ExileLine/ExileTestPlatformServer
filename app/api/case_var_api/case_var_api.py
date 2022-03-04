# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 1:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_var_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_variable.models import TestVariable, TestVariableHistory


def check_req_var(data):
    """检查变量参数"""
    var_type = data.get('var_type')
    var_source = data.get('var_source')
    var_type_list = list(range(1, 20))

    if var_type not in var_type_list:
        return False
    if var_source and var_source not in var_source_tuple:
        return False
    return True


class CaseVarApi(MethodView):
    """
    用例变量
    GET: 用例变量详情
    POST: 用例变量新增
    PUT: 用例变量编辑
    DELETE: 用例变量删除
    """

    def get(self, var_id):
        """用例变量详情"""

        query_var = TestVariable.query.get(var_id)

        if not query_var:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(var_id))

        return api_result(code=200, message='操作成功', data=query_var.to_json())

    def post(self):
        """用例变量新增"""

        data = request.get_json()
        if not check_req_var(data):
            return ab_code(400)

        var_name = data.get('var_name')
        var_value = data.get('var_value', "")
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        expression = data.get('expression')
        is_expression = data.get('is_expression', 0)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        query_var = TestVariable.query.filter_by(var_name=var_name).first()

        if query_var:
            return api_result(code=200, message='变量:【{}】已存在'.format(var_name))
        else:
            new_var = TestVariable(
                var_name=var_name,
                var_value=var_value,
                var_type=var_type,
                var_source=var_source,
                var_get_key=var_get_key,
                expression=expression,
                is_expression=is_expression,
                is_public=is_public if isinstance(is_public, bool) else True,
                remark=remark,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            new_var.save()
            return api_result(code=201, message='创建成功')

    def put(self):
        """用例变量编辑"""

        data = request.get_json()

        if not check_req_var(data):
            return ab_code(400)

        var_id = data.get('id')
        var_name = data.get('var_name')
        var_value = data.get('var_value', "")
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        expression = data.get('expression')
        is_expression = data.get('is_expression', 0)
        is_public = data.get('is_public', True)
        remark = data.get('remark')

        query_var = TestVariable.query.get(var_id)
        after_var = query_var.var_value

        if not query_var:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(var_id))

        if not bool(is_public) and query_var.creator_id != g.app_user.id:
            return api_result(code=400, message='非创建人，无法修改使用状态')

        if not bool(query_var.is_public):
            if query_var.creator_id != g.app_user.id:
                return api_result(code=400, message='该变量未开放,只能被创建人修改!')

        query_var_filter = TestVariable.query.filter_by(var_name=var_name).first()

        if query_var_filter and query_var.to_json().get('var_name') != var_name:
            return api_result(code=400, message='变量名称:{} 已存在'.format(var_name))

        query_var.var_name = var_name
        query_var.var_value = var_value
        query_var.var_type = var_type
        query_var.var_source = var_source
        query_var.var_get_key = var_get_key
        query_var.expression = expression
        query_var.is_expression = is_expression
        query_var.is_public = is_public if isinstance(is_public, bool) else True
        query_var.remark = remark
        query_var.modifier = g.app_user.username
        query_var.modifier_id = g.app_user.id
        db.session.commit()

        var_history = TestVariableHistory(
            var_id=var_id,
            update_type="用户操作更新",
            before_var=query_var.var_value,
            after_var=after_var,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        db.session.add(var_history)
        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例变量删除"""

        data = request.get_json()
        var_id = data.get('id')

        query_var = TestVariable.query.get(var_id)

        if not query_var:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(var_id))

        if query_var.creator_id != g.app_user.id:
            return api_result(code=400, message='非管理员不能删除其他人的变量！')

        query_var.modifier_id = g.app_user.id
        query_var.modifier = g.app_user.username
        query_var.delete()
        return api_result(code=204, message='删除成功')


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
        return api_result(code=200, message='操作成功', data=result_data)


class CaseVarPageApi(MethodView):
    """
    case var page api
    POST: 用例变量分页模糊查询
    """

    def post(self):
        """用例变量分页模糊查询"""

        data = request.get_json()
        var_id = data.get('var_id')
        var_name = data.get('var_name')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_variable  
        WHERE 
        id LIKE"%%" 
        and var_name LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=TestVariable,
            field_list=['id', 'var_name'],
            query_list=[var_id, var_name],
            is_deleted=is_deleted,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)
