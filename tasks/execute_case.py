# -*- coding: utf-8 -*-
# @Time    : 2022/8/24 16:40 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : execute_case.py
# @Software: PyCharm

import asyncio

from tasks.celery import cel
from common.libs.async_test_runner.async_runner import AsyncCaseRunner


@cel.task
def execute_case(test_obj):
    acr = AsyncCaseRunner(test_obj=test_obj)
    asyncio.run(acr.main())
    return "执行完成"
