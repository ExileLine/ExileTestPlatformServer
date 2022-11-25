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
        """

        :param loop: 事件循环
        :param pool: 连接池
        :param conf_dict: 连接配置
        :param debug: 调试
        """

        self.loop = loop
        self.pool = pool
        self.conf_dict = conf_dict
        self.debug = debug

    async def get_loop(self):
        """1"""

        return

    async def init_pool(self):
        """
        初始化连接池
        当 loop 接收一个来自应用的 `loop` 即 `app.loop` 用于 aioHttp,fastApi,tornado 等异步web框架
        例如: app['aio_mysql_engine'] = await aiomysql.create_pool(**aio_mysql_conf, charset='utf8', loop=app.loop)

        当 loop 为 None 时获取当前的 `loop` 即 asyncio.run() 注意:如果接收一个新的 `loop` 会出现 attached to a different loop 事件循环不一致的问题
        例如: asyncio.run(fun(*args,**kwargs))
        :return:
        """

        try:
            if self.loop:
                new_pool = await aiomysql.create_pool(**self.conf_dict, charset='utf8', loop=self.loop)
                self.pool = new_pool
                print('=== new_pool ===')
                return self.pool
            else:
                new_pool = await aiomysql.create_pool(**self.conf_dict, charset='utf8', loop=asyncio.get_event_loop())
                print('=== get_event_loop ===')
                return new_pool
        except BaseException as e:
            print(f'创建连接池异常:{e}')
            return None

    async def __query(self, only=None, size=None, cur=None):
        """
        sql查询语句
        :param only:
        :param size:
        :param cur: cursor游标
        :return:
        """

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

    async def __execute(self, sql, conn=None, cur=None):
        """
        sql执行语句
        :param conn: connector连接
        :param cur: cursor游标
        :return:
        """

        print(f"sql: {sql}")

        try:
            await cur.execute(sql)
            return True
        except BaseException as e:
            message = str(e) if self.debug else ''
            print(f"{sql.split(' ')[0]}执行出现错误:{message}")
            await conn.rollback()
            return False
        # else:
        #     affected = cur.rowcount
        #     return affected

    async def query(self, sql, only=None, size=None):
        """
        直连select
        :param sql:
        :param only:
        :param size:
        :return:
        """

        async with aiomysql.connect(loop=asyncio.get_event_loop(), **self.conf_dict) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql)
                result = await self.__query(only=only, size=size, cur=cur)
        return result

    async def execute(self, sql):
        """
        直连update, instr, delete ...
        :param sql:
        :return:
        """

        async with aiomysql.connect(loop=asyncio.get_event_loop(), **self.conf_dict) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                result = await self.__execute(sql=sql, conn=conn, cur=cur)
        return result

    async def pool_query(self, sql, only=None, size=None):
        """
        连接池select
        :param sql:
        :param only:
        :param size:
        :return:
        """

        pool = await self.init_pool()

        print(f"sql: {sql}")

        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(sql)
                    result = await self.__query(only=only, size=size, cur=cur)
            return result
        except BaseException as e:
            message = str(e) if self.debug else ''
            return f'select出现错误:{message}'
        # finally:
        # 释放掉conn,将连接放回到连接池中
        # await self.pool.release(conn)

    async def pool_execute(self, sql):
        """
        连接池update, instr, delete ...
        :param sql:
        :return:
        """

        pool = await self.init_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                result = await self.__execute(sql=sql, conn=conn, cur=cur)

        return result


if __name__ == '__main__':
    db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)

    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    result = asyncio.run(db.query(sql=sql, only=True))
    print(result)

    sql = """UPDATE `ExileTestPlatform5.0`.`exile_test_case` SET `request_method` = 'GET123' WHERE `id` = '1';"""
    result = asyncio.run(db.execute(sql=sql))
    print(result)
