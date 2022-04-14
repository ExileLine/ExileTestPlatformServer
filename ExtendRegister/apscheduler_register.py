# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 2:14 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : apscheduler_register.py
# @Software: PyCharm


import atexit
import platform
from flask_apscheduler import APScheduler

scheduler = APScheduler()


def register_apscheduler(app):
    """定时任务注册"""
    scheduler.init_app(app)
    scheduler.start()


def __register_apscheduler(app):
    """
    定时任务注册
    """

    if platform.system() != 'Windows':
        # Linux 环境下
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            print('dev1 scheduler start.....')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        # Window 环境下
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            scheduler.start()
            print('dev2 scheduler start.......')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)
