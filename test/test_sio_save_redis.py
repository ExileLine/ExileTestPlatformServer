# -*- coding: utf-8 -*-
# @Time    : 2021/9/23 9:45 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_sio_save_redis.py
# @Software: PyCharm


import json
from common.libs.db import R

if __name__ == '__main__':
    r = R.get("test_log_1632405375")
    x = json.loads(r)
    for i in x.get('case_result_list'):
        print(i.get('case_log'))
