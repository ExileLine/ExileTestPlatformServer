# -*- coding: utf-8 -*-
# @Time    : 2022/7/19 10:51
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : celeryconfig.py
# @Software: PyCharm

from config.config import config_obj

broker_url = config_obj['new'].broker_url
result_backend = config_obj['new'].result_backend

# 时区
timezone = 'Asia/Shanghai'

# 是否使用UTC
enable_utc = False

# include_list = [
#     'tasks.celery_tasks.task01',
#     'tasks.celery_tasks.task02'
# ]

imports = (
    'tasks.task01',
    'tasks.task02',
    'tasks.task03',
    'tasks.parse_json',
    'tasks.postman_import'
)