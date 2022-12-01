# -*- coding: utf-8 -*-
# @Time    : 2022/12/1 10:28
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_aio_redis.py
# @Software: PyCharm

import json
import asyncio

from common.libs.db import AIO_REDIS_CONF
from common.libs.async_db import MyAioRedis


async def test_001():
    """测试直接连接:字符串set/get"""

    db = MyAioRedis(conf_dict=AIO_REDIS_CONF, debug=True)
    await db.redis.set('test_set_str', 'test_001')
    result = await db.redis.get('test_redis')
    return result


async def test_002():
    """测试直接连接:json字符串set/get"""

    db = MyAioRedis(conf_dict=AIO_REDIS_CONF, debug=True)
    await db.redis.set('test_set_json_str', json.dumps({"test_001": "test_set_json_str"}))
    result = await db.redis.get('test_set_json_str')
    result_to_dict = json.loads(result)
    return result_to_dict


async def test_003():
    """测试直接连接:语句执行"""

    db = MyAioRedis(conf_dict=AIO_REDIS_CONF, debug=True)
    command = 'set test_003_key 123456'
    print(command)
    await db.execute(command)
    result = await db.execute('get test_003_key')
    return result


async def test_004():
    """测试连接连接池:字符串set/get"""

    db = MyAioRedis(is_pool=True, conf_dict=AIO_REDIS_CONF, debug=True)
    await db.redis.set('test_set_str', 'test_001')
    result = await db.redis.get('test_redis')
    return result


async def test_005():
    """测试连接连接池:json字符串set/get"""

    db = MyAioRedis(is_pool=True, conf_dict=AIO_REDIS_CONF, debug=True)
    await db.redis.set('test_set_json_str', json.dumps({"test_001": "test_set_json_str"}))
    result = await db.redis.get('test_set_json_str')
    result_to_dict = json.loads(result)
    return result_to_dict


async def test_006():
    """测试连接连接池:语句执行"""

    db = MyAioRedis(is_pool=True, conf_dict=AIO_REDIS_CONF, debug=True)
    command = 'set test_003_key 123456'
    print(command)
    await db.execute(command)
    result = await db.execute('get test_003_key')
    return result


if __name__ == '__main__':
    res1 = asyncio.run(test_001())
    print(res1, type(res1), '\n')

    res2 = asyncio.run(test_002())
    print(res2, type(res2), '\n')

    res3 = asyncio.run(test_003())
    print(res3, type(res3), '\n')

    res4 = asyncio.run(test_004())
    print(res4, type(res4), '\n')

    res5 = asyncio.run(test_005())
    print(res5, type(res5), '\n')

    res6 = asyncio.run(test_006())
    print(res6, type(res6), '\n')
