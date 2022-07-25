# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 2:14 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : apscheduler_register.py
# @Software: PyCharm

import os
import atexit
import platform

from flask_apscheduler import APScheduler

scheduler = APScheduler()


def register_apscheduler(app):
    """定时任务注册"""

    scheduler.init_app(app)
    scheduler.start()

    @scheduler.authenticate
    def authenticate(auth):
        """Check auth."""
        R = app.config.get("R")
        username = R.get('apscheduler')
        password = R.get('apscheduler_pwd')
        # return auth["username"] == 'yyx' and auth["password"] == 'yyx'
        return auth["username"] == username and auth["password"] == password

    print('APScheduler start...')


def __register_apscheduler(app):
    """定时任务注册"""

    if os.environ.get('FLASK_ENV') == 'production':
        pf = platform.system()
        if pf != 'Windows':  # Linux,MacOS
            fcntl = __import__("fcntl")
            f = open('scheduler.lock', 'wb')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                scheduler.init_app(app)
                scheduler.start()

                @scheduler.authenticate
                def authenticate(auth):
                    """Check auth."""
                    R = app.config.get("R")
                    username = R.get('apscheduler')
                    password = R.get('apscheduler_pwd')
                    # return auth["username"] == 'yyx' and auth["password"] == 'yyx'
                    return auth["username"] == username and auth["password"] == password

                print(f'{pf}-APScheduler start...')

            except BaseException as e:
                print(str(e))

            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()

            atexit.register(unlock)
        else:
            msvcrt = __import__('msvcrt')
            f = open('scheduler.lock', 'wb')
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                scheduler.init_app(app)
                scheduler.start()

                @scheduler.authenticate
                def authenticate(auth):
                    """Check auth."""
                    R = app.config.get("R")
                    username = R.get('apscheduler')
                    password = R.get('apscheduler_pwd')
                    # return auth["username"] == 'yyx' and auth["password"] == 'yyx'
                    return auth["username"] == username and auth["password"] == password

                print(f'{pf}-APScheduler start...')

            except BaseException as e:
                print(str(e))

            def _unlock_file():
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass

            atexit.register(_unlock_file)
    else:
        scheduler.init_app(app)
        scheduler.start()
        print('dev-APScheduler start...')
