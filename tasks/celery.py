# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:40 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : celery.py
# @Software: PyCharm

from celery import Celery

broker_url = 'redis://:123456@127.0.0.1:6379/2'
result_backend = 'redis://:123456@127.0.0.1:6379/3'
include_list = [
    'tasks.task01',
    'tasks.task02',
    'tasks.task03'
]
cel = Celery('celery_demo', broker=broker_url, backend=result_backend, include=include_list)

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False

"""
celery --app=tasks worker -l info --detach

前台执行:
    celery --app=tasks worker -l INFO
            
后台执行:
    celery -A tasks multi start worker1 --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/%n%I.log"
    celery -A tasks multi start worker1 --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log"
    
重启并后台执行:
    celery -A tasks multi restart worker1 --pidfile="$HOME/run/celery/%n.pid" --logfile="$HOME/log/celery/%n%I.log"
    celery -A tasks multi restart worker1 --pidfile="/srv/logs/celery/%n.pid" --logfile="/srv/logs/celery/%n%I.log"

异步关闭(立即返回):
    celery multi stop worker1 --pidfile="$HOME/run/celery/%n.pid"
    celery multi stop worker1 --pidfile="/srv/logs/celery/%n.pid"

等待关闭(操作完成):
    celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"
    celery multi stopwait worker1 --pidfile="/srv/logs/celery/%n.pid"
"""
