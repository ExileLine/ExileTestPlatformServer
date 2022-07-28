# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test.py
# @Software: PyCharm

import asyncio

from common.libs.async_case_runner import AsyncCaseRunner

acr = AsyncCaseRunner()
if __name__ == '__main__':
    asyncio.run(acr.main())
    rl = list(sorted(acr.test_list, key=lambda x: x.get("t")))
    print([(r.get('n'), r.get('t')) for r in rl if 'y' in r.get('n')])
    print([(r.get('n'), r.get('t')) for r in rl if 'x' in r.get('n')])
    print([(r.get('n'), r.get('t')) for r in rl if 'z' in r.get('n')])
