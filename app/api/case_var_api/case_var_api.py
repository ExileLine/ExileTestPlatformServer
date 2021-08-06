# -*- coding: utf-8 -*-
# @Time    : 2021/8/6 1:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_var_api.py
# @Software: PyCharm


from app.all_reference import *
from app.models.test_variable.models import TestVariable


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
        return api_result(code=200, message='操作成功')

    def post(self):
        """用例变量新增"""
        d = {
            "var_name": "变量名称",
            "var_value": "123okc",
            "var_type": "str",
            "var_source": "resp_data",
            "var_get_key": "",
            "var_gremarket_key": "remark"
        }
        return api_result(code=201, message='创建成功', data=d)

    def put(self):
        """用例变量编辑"""
        return api_result(code=203, message='编辑成功')

    def delete(self):
        """用例变量删除"""
        return api_result(code=204, message='删除成功')
