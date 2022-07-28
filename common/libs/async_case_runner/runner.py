# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 13:18
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : runner.py
# @Software: PyCharm


import time
import aiohttp
import asyncio


class AsyncCaseRunner:
    """异步用例执行"""

    def __init__(self):

        self.ll = [
            ['y1', 'y2', 'y3', 'y4', 'y5', 'y6'],
            ['x1', 'x2', 'x3', 'x4', 'x5', 'x6'],
            ['z1', 'z2', 'z3', 'z4', 'z5', 'z6']
        ]
        self.logs_hash_map = {}
        self.test_list = []

    async def request_before(self):
        """请求前置"""
        print('request_before')

    async def request_after(self):
        """请求后置"""
        print('request_after')

    @classmethod
    async def check_method(cls, session, method):
        """检查请求方式"""

        if not hasattr(session, method):
            print(f'错误的请求方式:{method}')
            return False
        return True

    async def current_request(self, method, url, headers=None):
        """异步请求"""

        sem = asyncio.Semaphore(100)  # 并发数量限制
        # timeout = aiohttp.ClientTimeout(total=3)  # 超时
        async with sem:
            async with aiohttp.ClientSession(headers=headers, cookies='') as session:
                method = method.lower()
                result = await self.check_method(session, method)
                if not result:
                    return {
                        "error": f"错误的请求方式:{method}"
                    }
                async with getattr(session, method)(url) as resp:
                    if resp.status in [200, 201]:
                        data = await resp.json()
                        return data

    async def scenario_task(self, scenario_list):
        """场景"""

        for scenario in scenario_list:
            headers = {
                "token": f"{scenario}--d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122"
            }
            await self.request_before()
            result = await self.current_request("get", url='http://0.0.0.0:7878/api/auth', headers=headers)
            print(result)
            await self.request_after()
            d = {
                "n": scenario,
                "t": time.time()
            }
            self.test_list.append(d)

    async def case_task(self, i):
        """用例"""

        print('hello:{}'.format(i))
        # result = await asyncio.sleep(1)
        headers = {
            "token": f"{i}--d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122"
        }
        await self.request_before()
        result = await self.current_request("GET", url='http://0.0.0.0:7878/api/auth', headers=headers)
        await self.request_after()
        print('world:{}'.format(i))
        print(result)

    async def test_loader(self):
        """用例加载"""

        case_task = [asyncio.create_task(self.case_task(i)) for i in range(10)]
        scenario_task = [asyncio.create_task(self.scenario_task(i)) for i in self.ll]
        await asyncio.wait(case_task)
        await asyncio.wait(scenario_task)

    async def main(self):
        """main"""

        await self.test_loader()
