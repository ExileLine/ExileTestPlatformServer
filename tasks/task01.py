# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:42 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : task01.py
# @Software: PyCharm

import time
import datetime

from celery_app import cel


@cel.task
def send_email(res):
    time.sleep(2)
    return {
        "message": "完成向%s发送邮件任务" % res,
        "datetime": datetime.datetime.now(),
        "time": time.time()
    }
