# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index_api.py
# @Software: PyCharm

from all_reference import *


class IndexApi(MethodView):
    """
    index_api
    """

    def get(self):
        return api_result(code=200, message='index', data=[time.time(), g.app_user.id, g.app_user.username])

    def post(self):
        data = request.get_json()
        d = data
        return api_result(code=200, message='index', data=d)
