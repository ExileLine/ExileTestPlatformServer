# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 13:41
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_report_api.py
# @Software: PyCharm


from all_reference import *


class CaseReportApi(MethodView):
    """
    测试报告 Api
    """

    def get(self, redis_key):
        """1"""

        query_logs_json = R.get(redis_key)
        if not query_logs_json:
            return api_result(code=NO_DATA, message="日志不存在无法生成测试报告")

        # 渲染逻辑
        h = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1 style="color:red">
        模块001的index页面
    </h1>
</body>
</html>
        """
        return h
