# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : hook_register.py
# @Software: PyCharm

from app.api import api
from app.api import crm
from common.interceptors.ApiHook import api_before_request, api_after_request
from common.interceptors.CrmHook import crm_before_request, crm_after_request
from common.interceptors.AppHook import app_before_request, app_after_request


def register_hook(app):
    """拦截器(钩子函数)注册"""

    api.before_request(api_before_request)
    api.after_request(api_after_request)

    crm.before_request(crm_before_request)
    crm.after_request(crm_after_request)

    # app.before_request(app_before_request)
    # app.after_request(app_after_request)