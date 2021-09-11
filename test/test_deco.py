# -*- coding: utf-8 -*-
# @Time    : 2021/9/11 12:30 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_deco.py
# @Software: PyCharm


from functools import wraps


# 无参数装饰器
def deco_1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('func name:{}'.format(func.__name__))
        print('func doc:{}'.format(func.__doc__))
        print('func param:{}'.format(args))
        print('func param:{}'.format(kwargs))
        return func(*args, **kwargs)

    return wrapper


# 带参数装饰器
def deco_2(deco_param):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('func name:{}'.format(func.__name__))
            print('func doc:{}'.format(func.__doc__))
            print('func param:{}'.format(args))
            print('func param:{}'.format(kwargs))
            print('deco deco_param:{}'.format(deco_param))
            return func(*args, **kwargs)

        return wrapper

    return decorator


@deco_1
def main_1():
    """第一个main"""
    print('main_1 done')


@deco_2('test')
def main_2(*args, **kwargs):
    """第二个main"""
    print('main_2 done')


if __name__ == '__main__':
    main_1()
    print('-' * 33)
    main_2(*['yyx', 'okc'], **{"yang": "123", "yue": "456", "x": "789"})
