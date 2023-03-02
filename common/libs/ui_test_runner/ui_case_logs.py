# -*- coding: utf-8 -*-
# @Time    : 2023/2/24 10:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_logs.py
# @Software: PyCharm


import json
import time
from time import gmtime
from time import strftime
from decimal import Decimal


class UiCaseLogs:
    """UI执行日志"""

    def __init__(self):
        self.logs_list = []

        self.start_time = 0
        self.end_time = 0
        self.total_time = 0

        self.execute_count = 0
        self.execute_success = 0
        self.execute_fail = 0
        self.execute_success_rate = 0
        self.execute_fail_rate = 0

    def logs_add(self, logs_obj: any):
        self.logs_list.append(logs_obj)

    def get_logs(self, is_json=False):
        """
        获取日志结果集
        :param is_json:
        :return:
        """

        if is_json:
            print(json.dumps(self.logs_list, ensure_ascii=False))

        return self.logs_list

    @classmethod
    def gen_rate(cls, first, last):
        """生成%,保留两位"""

        return f"{Decimal(first / last * 100).quantize(Decimal('1.00'))}%"

    def get_test_result(self):
        """
        获取测试结果
        :return:
        """

        self.execute_success_rate = self.gen_rate(self.execute_success, self.execute_count)
        self.execute_fail_rate = self.gen_rate(self.execute_fail, self.execute_count)
        self.total_time = round(self.end_time - self.start_time, 2)
        total_time_str = strftime("%H小时 %M分 %S秒", gmtime(self.total_time))

        d = {
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)),
            "end_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end_time)),
            "total_time": self.total_time,
            "total_time_str": total_time_str,
            "execute_count": self.execute_count,
            "execute_success": self.execute_success,
            "execute_fail": self.execute_fail,
            "execute_success_rate": self.execute_success_rate,
            "execute_fail_rate": self.execute_fail_rate
        }
        return d
