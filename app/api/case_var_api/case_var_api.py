# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 1:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_var_api.py
# @Software: PyCharm


from app.all_reference import *
from app.models.test_variable.models import TestVariable

var_type_dict = {
    "str": 1,
    "int": 2,
    "json": 3,
    "jsonstr": 4,
    "list": 5,
    "liststr": 6
}
var_source_dict = {
    "resp_data": 1,
    "resp_header": 2
}


def check_req_var(data):
    """检查变量参数"""
    var_type = data.get('var_type')
    var_source = data.get('var_source')

    if var_type_dict.get(var_type.lower()) and var_source_dict.get(var_source):
        return True
    else:
        return False


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
        var_value = data.get('var_value')
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        remark = data.get('remark')

        query_var = TestVariable.query.filter_by(var_name=var_name).first()

        if query_var:
            return api_result(code=200, message='变量:【{}】已存在'.format(var_name))
        else:
            new_var = TestVariable(
                var_name=var_name,
                var_value=var_value,
                var_type=var_type_dict.get(var_type.lower()),
                var_source=var_source_dict.get(var_source),
                var_get_key=var_get_key,
                remark=remark,
                creator='调试',
                creator_id=1
            )
            db.session.add(new_var)
            db.session.commit()
            return api_result(code=201, message='创建成功')

    def put(self):
        """用例变量编辑"""

        data = request.get_json()

        if not check_req_var(data):
            return ab_code(400)

        var_id = data.get('var_id')
        var_name = data.get('var_name')
        var_value = data.get('var_value')
        var_type = data.get('var_type')
        var_source = data.get('var_source')
        var_get_key = data.get('var_get_key')
        remark = data.get('remark')

        query_var_filter = TestVariable.query.filter_by(var_name=var_name).first()
        query_var = TestVariable.query.get(var_id)

        if query_var_filter and query_var.to_json().get('var_name') != var_name:
            return api_result(code=400, message='用例名称:{} 已存在'.format(var_name))

        if query_var:
            query_var.var_name = var_name
            query_var.var_value = var_value
            query_var.var_type = var_type_dict.get(var_type.lower())
            query_var.var_source = var_source_dict.get(var_source)
            query_var.var_get_key = var_get_key
            query_var.remark = remark
            query_var.modifier = "调试"
            query_var.modifier_id = 1
            db.session.commit()
            return api_result(code=203, message='编辑成功')
        else:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(var_id))

    def delete(self):
        """用例变量删除"""

        data = request.get_json()
        var_id = data.get('var_id')

        query_var = TestVariable.query.get(var_id)

        if not query_var:
            return api_result(code=400, message='用例变量id:{}数据不存在'.format(var_id))

        query_var.is_deleted = query_var.id
        query_var.modifier = "调试"
        query_var.modifier_id = 1
        db.session.commit()
        return api_result(code=204, message='删除成功')
