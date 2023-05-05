# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:42 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : task02.py
# @Software: PyCharm


from celery_app import cel
from app.models.admin.models import Admin


@cel.task
def test_context():
    """测试flask中celery上下文"""

    admin = Admin.query.get(1)
    print('=== 测试flask中celery上下文 ===')
    print(admin.to_json())
