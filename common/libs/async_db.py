# -*- coding: utf-8 -*-
# @Time    : 2022/9/23 17:43
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_db.py
# @Software: PyCharm

import asyncio
import aiomysql

from common.libs.db import result_format, DB

MYSQL_CONF = DB
MYSQL_CONF['autocommit'] = 'true'


class MyAioMySQL:

    def __init__(self, loop=None, pool=None, conf_dict=None, debug=None):

        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()

        self.pool = pool
        self.conf_dict = conf_dict
        self.debug = debug

    async def init_pool(self):
        """初始化连接池"""
        try:
            new_pool = await aiomysql.create_pool(**self.conf_dict, charset='utf8', loop=self.loop)
            self.pool = new_pool
            return True
        except BaseException as e:
            print(f'创建连接池异常:{e}')
            return False

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


async def aio_mysql_query(sql, only=None, size=None):
    """aio sql查询"""
    db = MyAioMySQL(conf_dict=MYSQL_CONF)
    await db.init_pool()
    query_result = await db.query(sql, only=only, size=size)
    return query_result


async def aio_mysql_execute(sql):
    """aio sql执行"""
    db = MyAioMySQL(conf_dict=MYSQL_CONF)
    await db.init_pool()
    await db.execute(sql)


if __name__ == '__main__':
    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    result = asyncio.run(aio_mysql_query(sql=sql, only=True))
    print(result)
