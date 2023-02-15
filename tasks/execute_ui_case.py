# -*- coding: utf-8 -*-
# @Time    : 2023/2/15 15:44
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : execute_ui_case.py
# @Software: PyCharm


from tasks.celery import cel
from common.libs.BaseWebDriver import BaseWebDriver
from common.libs.ui_test_runner.ui_runner import ui_case_runner


@cel.task
def execute_ui_case(meta_data_list):
    result = ui_case_runner(meta_data_list=meta_data_list, web_driver=BaseWebDriver)
    return "执行完成", result
