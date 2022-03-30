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
import psycopg2
from psycopg2.extras import DictCursor, RealDictCursor

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
    def __init__(self, host=None, port=None, user=None, password=None, db=None, debug=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
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
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)  # 执行sql语句
                if only and not size:  # 唯一结果返回 json/dict
                    query_result = cur.fetchone()
                    result = result_format(query_result)
                elif size and not only:  # 按照需要的长度返回
                    query_result = cur.fetchmany(size)
                    result = [result_format(data) for data in query_result]
                else:  # 返回结果集返回 list
                    query_result = cur.fetchall()
                    result = [result_format(data) for data in query_result]
                return result
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')

    def execute_sql(self, sql=None):
        """execute_sql"""
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                result = cur.execute(sql)
                return result
        except BaseException as e:
            print(str(e))

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
            with db.cursor() as cur:
                result = cur.execute(sql)
                return result
        except BaseException as e:
            print(str(e))

    def ping(self):
        """ping"""
        return self.db_obj().cursor()


project_db = MyPyMysql(**DB, debug=CONFIG_OBJ.DEBUG)  # MySql实例

if __name__ == '__main__':
    # 测试 MySql
    print('\n===test MySql===')
    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    print('ping:', project_db.db_obj().open)
    result1 = project_db.select(sql, only=True)
    result2 = project_db.select(sql, size=3)
    result3 = project_db.select(sql)
    print(result1, type(result1), len(result1))
    print(result2, type(result2), len(result2))
    print(result3, type(result3), len(result3))

    # 测试 Redis
    print('\n===test Redis===')
    print('ping:', R.ping())
    print(R)
    print(R.get('yangyuexiong'))
    print(R.execute_command("get 127.0.0.1"))
    print(type(R.execute_command("get 127.0.0.1")))
