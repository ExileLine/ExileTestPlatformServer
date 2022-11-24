# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 16:30
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_aio_db.py
# @Software: PyCharm

import asyncio

from common.libs.async_db import MyAioMySQL, MYSQL_CONF


async def test_aio_mysql(*args, **kwargs):
    """测试"""
    db = MyAioMySQL(conf_dict=MYSQL_CONF)
    await db.init_pool()

    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"

    result1 = await db.query(sql, only=True)
    print(result1, type(result1))

    result2 = await db.query(sql, size=3)
    print(result2, type(result2), len(result2))

    result3 = await db.query(sql)
    print(result3, type(result3), len(result3))
    return result1, result2, result3


class A:

    def __init__(self):
        self.db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)

    async def correct_demo(self):
        """正确例子"""

        sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
        db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)
        await db.init_pool()
        result1 = await db.query(sql, only=True)
        print(result1, type(result1))

    async def error_demo(self):
        """错误例子"""

        sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
        self.db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)
        await self.db.init_pool()
        result1 = await self.db.query(sql, only=True)
        print(result1, type(result1))


if __name__ == '__main__':
    pass
    result = asyncio.run(test_aio_mysql())
    print(result)

    a = A()
    asyncio.run(a.correct_demo())
    asyncio.run(a.error_demo())
