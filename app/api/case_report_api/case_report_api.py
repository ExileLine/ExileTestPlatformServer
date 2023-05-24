# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 13:41
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_report_api.py
# @Software: PyCharm

from all_reference import *

demo_html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试报告</title>
</head>
<body>
    <h1 style="color:red">
        测试报告页面
    </h1>
</body>
</html>
"""


class CaseReportApi(MethodView):
    """
    测试报告 Api
    """

    def get(self, redis_key):
        """生成测试报告"""

        query_logs_json = R.get(redis_key)
        if not query_logs_json:
            return api_result(code=NO_DATA, message="日志不存在无法生成测试报告")

        return render_template('test_report.html', **{"logs_json": query_logs_json})
