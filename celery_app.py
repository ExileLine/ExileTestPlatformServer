# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 10:48
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : celery_app.py
# @Software: PyCharm

from flask import Flask
from celery import Celery


def create_celery_app() -> Flask:
    """celery实例化应用实例"""

    app = Flask(__name__)  # 实例
    from ExtendRegister.conf_register import register_config
    from ExtendRegister.db_register import register_db
    register_config(app)  # 配置注册
    register_db(app)  # db注册
    return app


def create_celery(app: Flask) -> Celery:
    """

    :param app: Flask应用实例
    :return:
    """

    celery_example = Celery(app.import_name)

    celery_example.config_from_object("config.celeryconfig")

    class ContextTask(celery_example.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_example.Task = ContextTask
    return celery_example


init_app = create_celery_app()
cel = create_celery(app=init_app)

"""
前台执行:
    celery --app=celery_app.cel worker -l INFO

后台执行:
    celery -A celery_app.cel multi start worker --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/%n%I.log"
    celery -A celery_app.cel multi start worker --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log"
    
重启并后台执行:
    celery -A celery_app.cel multi restart worker --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/%n%I.log"
    celery -A celery_app.cel multi restart worker --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log"
    
异步关闭(立即返回):
    celery multi stop worker --pidfile="$HOME/run/celery/%n.pid"
    celery multi stop worker --pidfile="/srv/logs/celery/%n.pid"
    
等待关闭(操作完成):
    celery multi stopwait worker --pidfile="$HOME/run/celery/%n.pid"
    celery multi stopwait worker --pidfile="/srv/logs/celery/%n.pid"
"""
