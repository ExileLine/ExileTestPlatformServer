# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:57 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : task03.py
# @Software: PyCharm


from tasks.celery import cel
from common.libs.CaseDrivenResult import MainTest


@cel.task
def execute_main(test_obj):
    MainTest(test_obj).main()
    return "执行完成"
