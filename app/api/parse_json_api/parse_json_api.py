# -*- coding: utf-8 -*-
# @Time    : 2022/7/18 14:06
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : parse_json_api.py
# @Software: PyCharm


from all_reference import *
from tasks.parse_json import execute_pjs_main


class ParseJsonApi(MethodView):
    """
    解析json_schema
    """

    def post(self):
        """解析json_schema"""

        data = request.get_json()
        app_name = data.get('app_name')
        base_url = data.get('base_url')
        query_id = data.get('query_id')
        query_all = data.get('query_all')

        if not app_name or not base_url:
            return api_result(code=400, message='缺少必传参数:app_name, base_url')

        if not query_all and not query_id:
            return api_result(code=400, message='query_all 为false时需要传递query_id')

        execute_pjs_main.delay(**data)

        return api_result(code=200, message='操作成功')
