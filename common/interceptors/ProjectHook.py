# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 14:21
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ProjectHook.py
# @Software: PyCharm

from flask import request, g

from common.libs.api_result import *
from app.models.test_project.models import TestProject


def check_project_auth():
    """检查项目访问权限"""

    if '/api/project_page' not in request.path:
        data = request.get_json()
        project_id = data.get('project_id')
        if project_id:
            query_project = TestProject.query.get(project_id)
            if not query_project:
                return api_result(code=NO_DATA, message=f'项目: {project_id} 不存在')

            project_auth = query_project.project_auth
            project_user = query_project.project_user
            print(f'project_auth:{project_auth}')
            print(f'project_user:{project_user}')
            if project_auth:
                user_id = g.app_user.id
                username = g.app_user.username
                print(f'user_id:{user_id}')
                print(f'username:{username}')
                if user_id not in project_user and username != "admin1":
                    print('hhhh')
                    return api_result(code=BUSINESS_ERROR, message='缺少项目访问权限')
    return