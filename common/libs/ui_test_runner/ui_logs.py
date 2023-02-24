# -*- coding: utf-8 -*-
# @Time    : 2023/2/24 10:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_logs.py
# @Software: PyCharm


class UiCaseLogs:
    """UI执行日志"""

    def __init__(self):
        self.logs_list = []

    def logs_add(self, logs_obj: any):
        self.logs_list.append(logs_obj)
