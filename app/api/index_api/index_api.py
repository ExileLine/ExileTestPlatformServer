# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index_api.py
# @Software: PyCharm

from all_reference import *
import asyncio


class IndexApi(MethodView):
    """
    index_api
    """

    async def get(self):
        await asyncio.sleep(1)
        return api_result(code=200, message='index', data=[time.time(), g.app_user.id, g.app_user.username])

    async def post(self):
        data = request.get_json()
        d = data
        return api_result(code=200, message='index', data=d)
