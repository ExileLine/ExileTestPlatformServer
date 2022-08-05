# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:58
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_scenario_loader.py
# @Software: PyCharm


import asyncio
import json

from common.libs.async_case_runner import AsyncCaseRunner

test_obj = {}

if __name__ == '__main__':
    acr = AsyncCaseRunner(test_obj=test_obj)
    asyncio.run(acr.scenario_loader())
