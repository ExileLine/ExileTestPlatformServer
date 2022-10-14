# -*- coding: utf-8 -*-
# @Time    : 2022/9/23 17:43
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_db.py
# @Software: PyCharm

import asyncio
import aiomysql

from common.libs.db import result_format


class MyAioMySQL:

    def __init__(self, loop=None, pool=None, conf_dict=None, debug=None):
        self.loop = loop
        self.pool = pool
        self.conf_dict = conf_dict
        self.debug = debug

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
        """
        select
        :param sql:
        :param only:
        :param size:
        :return:
        """

        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql)
                    if only and not size:  # 唯一结果返回 json/dict
                        query_result = await cur.fetchone()
                        result = result_format(query_result)
                    elif size and not only:  # 按照需要的长度返回
                        query_result = await cur.fetchmany(size)
                        result = [result_format(q) for q in query_result]
                    else:
                        query_result = await cur.fetchall()
                        result = [result_format(q) for q in query_result]
            return result
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')
        # finally:
        # 释放掉conn,将连接放回到连接池中
        # await self.pool.release(conn)

    async def execute(self, sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql)
                except BaseException as e:
                    print('sql执行出现错误:{}'.format(str(e) if self.debug else ''))
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
        result1 = await db.query(sql, only=True)
        result2 = await db.query(sql, size=3)
        result3 = await db.query(sql)
        print(result1, type(result1), len(result1))
        print(result2, type(result2), len(result2))
        print(result3, type(result3), len(result3))


    asyncio.run(main())
