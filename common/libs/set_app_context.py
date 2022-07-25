# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 7:47 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : set_app_context.py
# @Software: PyCharm

from functools import wraps


def set_app_context(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            print('=== 测试:{} ==='.format(func.__name__))
            from ApplicationExample import create_app
            app = create_app(is_context=True)
            with app.app_context():
                return func(*args, **kwargs)

    return wrapper