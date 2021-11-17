# -*- coding: utf-8 -*-
# @Time    : 2021/9/24 1:50 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_clear_redis_execute_log.py
# @Software: PyCharm


from common.libs.db import R

if __name__ == '__main__':
    r1 = R.keys(pattern="test_log_*")
    r2 = R.keys(pattern="case_first_log:*")
    r3 = R.keys(pattern="scenario_first_log:*")
    list(map(lambda x: R.delete(x), r1))
    list(map(lambda x: R.delete(x), r2))
    list(map(lambda x: R.delete(x), r3))
