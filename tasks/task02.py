# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:42 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : task02.py
# @Software: PyCharm
import datetime
import time
from tasks.celery import cel


@cel.task
def send_msg(name):
    time.sleep(5)
    return {
        "message": "完成向%s发送短信任务" % name,
        "time": datetime.datetime.now()
    }
