# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 1:17 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : mail_api.py
# @Software: PyCharm

from all_reference import *


class MailApi(MethodView):
    """
    邮箱Api
    GET: 邮箱详情
    POST: 邮件新增
    PUT: 邮件编辑
    DELETE: 邮件删除
    """

    def get(self):
        """邮箱详情"""
        return

    def post(self):
        """邮箱新增"""
        return

    def put(self):
        """邮箱编辑"""
        return

    def delete(self):
        """邮箱删除"""
        return


class MailPageApi(MethodView):
    """
    mail page api
    POST: 邮箱分页模糊查询
    """

    def post(self):
        """邮箱分页模糊查询"""
        return
