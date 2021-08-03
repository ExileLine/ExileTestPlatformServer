# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 3:15 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ApiHook.py
# @Software: PyCharm

from flask import request, g

from app import api
from common.libs.tools import print_logs


@api.before_request
def before_request_api():
    print('=== api_before_request ===')
    print_logs()
    if '/api' in request.path:
        print('访问api')
        g.app_user = None
        return
