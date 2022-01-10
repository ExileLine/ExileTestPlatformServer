# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 1:22 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : dingding_api.py
# @Software: PyCharm


from all_reference import *


class DingDingApi(MethodView):
    """
    钉钉 Api
    GET: 钉钉 push 详情
    POST: 钉钉 push 新增
    PUT: 钉钉 push 编辑
    DELETE: 钉钉 push 删除
    """

    def get(self):
        """钉钉 push 详情"""
        return

    def post(self):
        """钉钉 push 新增"""
        return

    def put(self):
        """钉钉 push 编辑"""
        return

    def delete(self):
        """钉钉 push 删除"""
        return


class DingDingPushPageApi(MethodView):
    """
    钉钉 push page api
    POST: 钉钉 push 分页模糊查询
    """

    def post(self):
        """钉钉 push 分页模糊查询"""
        return
