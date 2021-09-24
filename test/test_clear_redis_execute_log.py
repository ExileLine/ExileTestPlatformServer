# -*- coding: utf-8 -*-
# @Time    : 2021/9/24 1:50 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_clear_redis_execute_log.py
# @Software: PyCharm


from common.libs.db import R

if __name__ == '__main__':
    r = R.keys(pattern="test_log_*")
    for c in r:
        R.delete(c)
