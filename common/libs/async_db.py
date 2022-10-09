# -*- coding: utf-8 -*-
# @Time    : 2022/9/23 17:43
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_db.py
# @Software: PyCharm

import asyncio
import decimal

import aiomysql

from common.libs.db import result_format


class AsyncMySQL:
    """1"""


class MyAioMySQL:

    def __init__(self, loop=None, pool=None, conf_dict=None):
        self.loop = loop
        self.pool = pool
        self.conf_dict = conf_dict

    async def init_pool(self):
        if self.pool:
            pass
        else:
            try:
                if self.conf_dict:
                    new_pool = await aiomysql.create_pool(**self.conf_dict, charset='utf8', loop=self.loop)
                    self.pool = new_pool
                else:
                    print('conf_dict 为空')
            except BaseException as e:
                print('创建连接池异常:{}'.format(e))

    async def query(self, sql, only=None, size=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:

                async def __func(r):
                    if isinstance(r, list):
                        new_list = []
                        for i in r:
                            new_r = {}
                            for k, v in i.items():
                                if isinstance(v, decimal.Decimal):
                                    # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                                    v = str(v)
                                    v = float(v)
                                    new_r[k] = v
                                else:
                                    new_r[k] = v
                            new_list.append(new_r)
                        return new_list
                    elif isinstance(r, dict):
                        new_r = {}
                        for k, v in r.items():
                            if isinstance(v, decimal.Decimal):
                                # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                                v = str(v)
                                v = float(v)
                                new_r[k] = v
                            else:
                                new_r[k] = v
                        return new_r
                    else:
                        pass

                try:
                    await cur.execute(sql)
                    if only and not size:  # 唯一结果返回 json/dict
                        rs = await cur.fetchone()
                        result = await __func(rs)
                        return result
                    if size and not only:  # 按照需要的长度返回
                        rs = await cur.fetchmany(size)
                        result = await __func(rs)
                        return result
                    else:  # 返回结果集返回 list
                        rs = await cur.fetchall()
                        result = await __func(rs)
                        return result

                except BaseException as e:
                    print('查询异常:{}'.format(e))
                # finally:
                # 释放掉conn,将连接放回到连接池中
                # await self.pool.release(conn)

    async def execute(self, sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql)
                except BaseException as e:
                    print(str(e))
                    await conn.rollback()
                # else:
                #     affected = cur.rowcount
                #     return affected


if __name__ == '__main__':
    async def main():
        loop = asyncio.get_event_loop()
        conf_dict = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '12345678',
            'db': 'ExileTestPlatform5.0',
            'autocommit': 'true'
        }
        db = MyAioMySQL(loop=loop, conf_dict=conf_dict)
        await db.init_pool()

        sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"

        r = await db.query(sql=sql)
        print(r)
        r = await db.query(sql=sql, size=1)
        print(r)
        r = await db.query(sql=sql, only=True)
        print(r)


    asyncio.run(main())
