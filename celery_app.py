# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 10:48
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : celery_app.py
# @Software: PyCharm


from celery import Celery
from ApplicationExample import create_app


def create_celery(app):
    """

    :param app: Flask应用实例
    :return:
    """

    my_celery = Celery(app.import_name)

    my_celery.config_from_object("config.celeryconfig")

    class ContextTask(my_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    my_celery.Task = ContextTask
    return my_celery


app = create_app()
cel = create_celery(app)

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
