# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : index.py
# @Software: PyCharm

from app.all_reference import *


class IndexApi(MethodView):
    """
    index
    """

    def get(self):
        return api_result(code=200, message='test platform index')
