# -*- coding: utf-8 -*-
# @Time    : 2022/4/29 17:12
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : download_file_api.py
# @Software: PyCharm

from pathlib import Path

from flask import send_file, current_app

from all_reference import *
from app.models.test_logs.models import TestExecuteLogs


class DownloadFileApi(MethodView):
    """
    文件下载Api
    POST: 文件下载
    """

    def post(self):
        """文件下载"""

        data = request.get_json()
        execute_logs_id = data.get('id')

        query_execute_logs = TestExecuteLogs.query.get(execute_logs_id)
        if not query_execute_logs:
            return api_result(code=400, message=f'日志:{execute_logs_id}不存在')

        file_name = query_execute_logs.file_name
        root_path = current_app.static_folder + '/report'
        file = Path(root_path) / file_name
        print(file)
        if not file.exists():
            return api_result(code=400, message=f'文件:{file_name}不存在')

        return send_file(str(file.absolute()))
