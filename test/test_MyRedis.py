# -*- coding: utf-8 -*-
# @Time    : 2022/12/2 15:43
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_MyRedis.py
# @Software: PyCharm

from common.libs.db import R


def test_redis():
    """测试Redis"""
    print('===test Redis===')
    print('ping:', R.ping())
    print(R)
    res1 = R.get('127.0.0.1')
    print(res1, type(res1))
    res2 = R.execute_command("get 127.0.0.1")
    print(res2, type(res2))


if __name__ == '__main__':
    test_redis()
