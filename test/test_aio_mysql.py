# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 16:30
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_aio_mysql.py
# @Software: PyCharm

import asyncio
from common.libs.db import MYSQL_CONF
from common.libs.async_db import MyAioMySQL


async def test_query():
    """测试直连查询"""

    db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)
    sql = "SELECT id, case_name FROM exile5_test_case limit 0,6;"

    result1 = await db.query(sql, only=True)
    print(result1, type(result1))

    result2 = await db.query(sql, size=3)
    print(result2, type(result2), len(result2))

    result3 = await db.query(sql)
    print(result3, type(result3), len(result3))
    return result1, result2, result3


async def test_pool_query():
    """测试连接池查询"""

    db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)
    sql = "SELECT id, case_name FROM exile5_test_case limit 0,6;"

    result1 = await db.pool_query(sql, only=True)
    print(result1, type(result1))

    result2 = await db.pool_query(sql, size=3)
    print(result2, type(result2), len(result2))

    result3 = await db.pool_query(sql)
    print(result3, type(result3), len(result3))
    return result1, result2, result3


if __name__ == '__main__':
    db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)
    print(db.conf_dict)
    sql = "SELECT id, case_name FROM exile5_test_case limit 0,6;"
    update_sql = """UPDATE exile5_test_case SET request_method = 'GET123' WHERE id = '1';"""

    print('\n=== 直接调用 ===')
    result1 = asyncio.run(db.query(sql, only=True))
    print(result1, type(result1))

    result2 = asyncio.run(db.query(sql, size=3))
    print(result2, type(result2), len(result2))

    result3 = asyncio.run(db.query(sql))
    print(result3, type(result3), len(result3))

    update_result = asyncio.run(db.execute(sql=update_sql))
    print(update_result)

    print('\n=== 连接池查询测试 ===')
    result1 = asyncio.run(db.pool_query(sql, only=True))
    print(result1, type(result1))

    result2 = asyncio.run(db.pool_query(sql, size=3))
    print(result2, type(result2), len(result2))

    result3 = asyncio.run(db.pool_query(sql))
    print(result3, type(result3), len(result3))

    update_result = asyncio.run(db.pool_execute(sql=update_sql))
    print(update_result)

    print('\n=== test_query ===')
    test_query_result = asyncio.run(test_query())
    print(test_query_result)

    print('\n=== test_pool_query ===')
    test_pool_query_result = asyncio.run(test_pool_query())
    print(test_pool_query_result)
