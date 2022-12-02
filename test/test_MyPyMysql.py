# -*- coding: utf-8 -*-
# @Time    : 2022/12/2 15:38
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_MyPyMysql.py
# @Software: PyCharm

from common.libs.db import MyPyMysql, MYSQL_CONF, MYSQL_POOL


def test_mysql():
    """测试MySql"""
    print('\n===test MySql===')
    project_db = MyPyMysql(**MYSQL_CONF, debug=True)  # MySql实例

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
    project_db_pool = MyPyMysql(pool=MYSQL_POOL, is_pool=True, debug=True)  # MySql连接池实例

    sql = "SELECT id, case_name FROM exile_test_case limit 0,6;"
    result1 = project_db_pool.select(sql, only=True)
    result2 = project_db_pool.select(sql, size=3)
    result3 = project_db_pool.select(sql)
    print(result1, type(result1), len(result1))
    print(result2, type(result2), len(result2))
    print(result3, type(result3), len(result3))


if __name__ == '__main__':
    test_mysql()
    test_mysql_pool()
