# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 2:14 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : apscheduler_register.py
# @Software: PyCharm


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
