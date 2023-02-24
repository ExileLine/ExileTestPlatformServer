# -*- coding: utf-8 -*-
# @Time    : 2023/2/24 10:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_logs.py
# @Software: PyCharm

import json


class UiCaseLogs:
    """UI执行日志"""

    def __init__(self):
        self.logs_list = []

    def logs_add(self, logs_obj: any):
        self.logs_list.append(logs_obj)

    def get_result(self, is_json=False):
        """获取日志结果集"""

        if is_json:
            print(json.dumps(self.logs_list, ensure_ascii=False))

        return self.logs_list
