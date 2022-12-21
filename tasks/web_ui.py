# -*- coding: utf-8 -*-
# @Time    : 2022/12/21 16:59
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : web_ui.py
# @Software: PyCharm


import time
import datetime

from tasks.celery import cel
from common.libs.BaseWebDriver import BaseWebDriver


@cel.task
def web_ui():
    bwd = BaseWebDriver(headless=True)
    bwd.test()
    return {
        "message": "完成 web_ui 任务",
        "datetime": datetime.datetime.now(),
        "time": time.time()
    }
