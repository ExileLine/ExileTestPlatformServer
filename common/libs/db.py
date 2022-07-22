# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : db.py
# @Software: PyCharm

import json
import decimal
from abc import ABCMeta, abstractmethod
from datetime import datetime

import pymysql
from dbutils.pooled_db import PooledDB
import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor
import pymssql

from config.config import config_obj

CONFIG_OBJ = config_obj.get('new')

R = CONFIG_OBJ.R  # Redis实例

DB = {
    'user': CONFIG_OBJ.MYSQL_USERNAME,
    'password': CONFIG_OBJ.MYSQL_PASSWORD,
    'host': CONFIG_OBJ.MYSQL_HOSTNAME,
    'port': CONFIG_OBJ.MYSQL_PORT,
    'db': CONFIG_OBJ.MYSQL_DATABASE
}

MYSQL_POOL = PooledDB(
    creator=pymysql,
    mincached=0,  # 初始化创建闲置连接线程数
    maxcached=0,  # 最大闲置连接线程数
    maxshared=0,
    maxconnections=100,  # 允许最大连接数
    blocking=True,  # 阻塞是否等待，False则阻塞时候报错
    maxusage=None,  # 一个线程连接可以复用的次数，None表示无限制
    setsession=None,  #
    ping=0,  # 执行前是否ping通数据
    **DB
)


def result_format(data):
    """
    查询结果处理
    :param data:
    :return:
    """
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, decimal.Decimal):
                data[key] = float(decimal.Decimal(val).quantize(decimal.Decimal("0.000")))
            elif isinstance(val, datetime):
                data[key] = str(val)
            elif isinstance(val, str):
                try:
                    new_val = json.loads(val)
                    if isinstance(new_val, (dict, list, tuple)):
                        data[key] = new_val
                except BaseException as e:
                    pass
    return data


class BaseDatabase(metaclass=ABCMeta):
    """基类"""

    @abstractmethod
    def db_obj(self):
        return


class MyPyMysql(BaseDatabase):
    def __init__(self, host=None, port=None, user=None, password=None, db=None, pool=None, is_pool=None, debug=None):
        """

        :param host:
        :param port:
        :param user:
        :param password:
        :param db:
        :param pool:
        :param is_pool:
        :param debug:
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = pool
        self.is_pool = is_pool
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            if self.is_pool:
                return self.pool.connection()
            else:
                database_obj = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    db=self.db)
                return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e) if self.debug else '')

    def __send(self, sql):
        """执行语句"""

        try:
            db = self.db_obj()
            with db as db:
                with db.cursor() as cur:
                    result = cur.execute(sql)
                    db.commit()
            return result
        except BaseException as e:
            cur.rollback()
            return f"执行错误:{str(e)}"

    def insert(self, sql):
        return self.__send(sql)

    def update(self, sql):
        return self.__send(sql)

    def delete(self, sql):
        return self.__send(sql)

    def select(self, sql=None, only=None, size=None):
        """
        查询
        :param sql:
        :param only:
        :param size:
        :return:
        """

        try:
            db = self.db_obj()
            with db as db:
                with db.cursor(pymysql.cursors.DictCursor) as cur:
                    cur.execute(sql)  # 执行sql语句
                    if only and not size:  # 唯一结果返回 json/dict
                        query_result = cur.fetchone()
                        result = result_format(query_result)
                    elif size and not only:  # 按照需要的长度返回
                        query_result = cur.fetchmany(size)
                        result = list(map(result_format, query_result))
                    else:  # 返回结果集返回 list
                        query_result = cur.fetchall()
                        result = list(map(result_format, query_result))
            return result
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')

    def execute_sql(self, sql=None):
        """execute_sql"""
        try:
            db = self.db_obj()
            with db as db:
                with db.cursor() as cur:
                    result = cur.execute(sql)
            return result
        except BaseException as e:
            print(f"execute_sql error {e}")

    def ping(self):
        """ping"""
        return self.db_obj().open


class MyPostgreSql(BaseDatabase):

    def __init__(self, host=None, port=None, user=None, password=None, database=None, debug=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            database_obj = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database)
            return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e) if self.debug else '')

    def __send(self, sql):
        """执行语句"""

        try:
            db = self.db_obj()
            with db as db:
                with db.cursor() as cur:
                    result = cur.execute(sql)
                    db.commit()
            return result
        except BaseException as e:
            cur.rollback()
            return f"执行错误:{str(e)}"

    def insert(self, sql):
        return self.__send(sql)

    def update(self, sql):
        return self.__send(sql)

    def delete(self, sql):
        return self.__send(sql)

    def select(self, sql=None, only=None, size=None):
        try:
            db = self.db_obj()
            with db as db:
                with db.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql)
                    if only and not size:
                        query_result = cur.fetchone()
                        results = result_format(query_result)
                    elif size and not only:
                        query_result = cur.fetchmany(size)
                        results = [result_format(data) for data in query_result]
                    else:
                        query_result = cur.fetchall()
                        results = [result_format(data) for data in query_result]
            results_json = json.dumps(results, ensure_ascii=False)
            return json.loads(results_json)
        except Exception as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')

    def execute_sql(self, sql=None):
        """execute_sql"""
        try:
            db = self.db_obj()
            with db as db:
                with db.cursor() as cur:
                    result = cur.execute(sql)
            return result
        except BaseException as e:
            print(f"execute_sql error {e}")

    def ping(self):
        """ping"""
        return self.db_obj().cursor()


class MySqlServer(BaseDatabase):

    def __init__(self, server=None, user=None, password=None, database=None, debug=None):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            database_obj = pymssql.connect(
                server=self.server,
                user=self.user,
                password=self.password,
                database=self.database)
            return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e) if self.debug else '')

    def __send(self, sql):
        """执行语句"""

        try:
            db = self.db_obj()
            with db as db:
                with db.cursor(as_dict=True) as cur:
                    result = cur.execute(sql)
                    db.commit()
            return result
        except BaseException as e:
            cur.rollback()
            return f"执行错误:{str(e)}"

    def insert(self, sql):
        return self.__send(sql)

    def update(self, sql):
        return self.__send(sql)

    def delete(self, sql):
        return self.__send(sql)

    def select(self, sql=None, only=None, size=None):
        try:
            db = self.db_obj()
            with db as db:
                with db.cursor(as_dict=True) as cur:
                    cur.execute(sql)
                    if only and not size:
                        query_result = cur.fetchone()
                        results = result_format(query_result)
                    elif size and not only:
                        query_result = cur.fetchmany(size)
                        results = [result_format(data) for data in query_result]
                    else:
                        query_result = cur.fetchall()
                        results = [result_format(data) for data in query_result]
            return results
        except Exception as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')

    def ping(self):
        """ping"""
        return self.db_obj().cursor()


project_db = MyPyMysql(**DB, debug=CONFIG_OBJ.DEBUG)  # MySql实例
project_db_pool = MyPyMysql(pool=MYSQL_POOL, is_pool=True, debug=CONFIG_OBJ.DEBUG)  # MySql连接池实例


def test_mysql():
    """测试MySql"""
    print('\n===test MySql===')
    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    print('ping:', project_db.db_obj().open)
    result1 = project_db.select(sql, only=True)
    result2 = project_db.select(sql, size=3)
    result3 = project_db.select(sql)
    print(result1, type(result1), len(result1))
    print(result2, type(result2), len(result2))
    print(result3, type(result3), len(result3))


def test_mysql_pool():
    """测试MySql连接池"""
    print('\n===test MySql POOL===')
    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    result1 = project_db_pool.select(sql, only=True)
    result2 = project_db_pool.select(sql, size=3)
    result3 = project_db_pool.select(sql)
    print(result1, type(result1), len(result1))
    print(result2, type(result2), len(result2))
    print(result3, type(result3), len(result3))


def test_redis():
    """测试Redis"""
    print('\n===test Redis===')
    print('ping:', R.ping())
    print(R)
    print(R.get('yangyuexiong'))
    print(R.execute_command("get 127.0.0.1"))
    print(type(R.execute_command("get 127.0.0.1")))


if __name__ == '__main__':
    test_mysql()
    test_mysql_pool()
    test_redis()
