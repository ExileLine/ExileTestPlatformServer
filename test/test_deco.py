# -*- coding: utf-8 -*-
# @Time    : 2021/9/11 12:30 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_deco.py
# @Software: PyCharm

import types
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


class ClassDeco:

    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs):
        print("call")
        print('func name:{}'.format(self.func.__name__))
        print('func doc:{}'.format(self.func.__doc__))
        return self.func(*args, **kwargs)


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@deco_1
def main_1():
    """第一个main"""
    print('main_1 done')


@deco_2('test')
def main_2(*args, **kwargs):
    """第二个main"""
    print('main_2 done')


@Profiled
def main_3(*args, **kwargs):
    """第三个main"""
    print('main_3 done')


def set_child_column(is_child=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_child:
                setattr(func, 'a', 123456)
                setattr(func, 'b', 123456)
                setattr(func, 'c', 123456)
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


@set_child_column(True)
class OKC:
    a = 1
    b = 2

    def hello(self):
        print(self.a)
        print(self.b)
        print(getattr(self, 'c'))
        print('hello')


if __name__ == '__main__':
    print('-' * 33)
    main_1()
    print('-' * 33)
    main_2(*['yyx', 'okc'], **{"yang": "123", "yue": "456", "x": "789"})
    print('-' * 33)
    main_3()
    print('-' * 33)
    okc = OKC()
    okc.hello()
    print(OKC.a)
