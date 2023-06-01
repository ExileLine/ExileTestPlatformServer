# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 13:41
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_report_api.py
# @Software: PyCharm


from all_reference import *
from config.config import config_obj

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


def save_html(ctn):
    """保存html文件,用于测试"""

    import shortuuid

    fn = f'/Users/yangyuexiong/Desktop/ExileTestPlatformServer/app/templates/xxx_{shortuuid.uuid()}.html'
    with open(fn, "w") as f:
        f.write(ctn)


class CaseReportApi(MethodView):
    """
    测试报告 Api
    """

    def get(self, redis_key):
        """生成测试报告"""

        query_logs_json = R.get(redis_key)
        if not query_logs_json:
            return api_result(code=NO_DATA, message="日志不存在无法生成测试报告")

        debug = config_obj['new'].DEBUG
        run_host = config_obj['new'].RUN_HOST
        run_port = config_obj['new'].RUN_PORT
        title = f"Exile测试报告{'Dev' if debug else ''}"
        static_path = f"http://{run_host}:{run_port}/{'static' if debug else 'report_static'}"
        ctx = {
            "title": title,
            "static_path": static_path,
            "logs_json": query_logs_json
        }
        html_str = render_template('test_report.html', **ctx)
        return html_str
