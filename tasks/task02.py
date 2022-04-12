# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:42 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : task02.py
# @Software: PyCharm

import time
from tasks.celery import cel


@cel.task
def send_msg(name):
    time.sleep(5)
    return "完成向%s发送短信任务" % name
