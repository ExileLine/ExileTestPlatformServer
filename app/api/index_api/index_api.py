# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : index_api.py
# @Software: PyCharm

from all_reference import *


class IndexApi(MethodView):
    """
    index Api
    """

    async def get(self):
        """index GET"""
        return api_result(code=SUCCESS, message='index GET', data=[])

    async def post(self):
        """index POST"""
        return api_result(code=POST_SUCCESS, message='index POST', data=[])

    async def put(self):
        """index PUT"""
        return api_result(code=PUT_SUCCESS, message='index PUT', data=[])

    async def delete(self):
        """index DELETE"""
        return api_result(code=DEL_SUCCESS, message='index DELETE', data=[])
