# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 10:26 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_stringIO.py
# @Software: PyCharm


import io
from shortuuid import uuid
from loguru import logger


class T:

    def __init__(self):
        self.output = io.StringIO()

    def a(self):
        self.output.write(uuid() + '\n')

    def get_output(self):
        print(self.output.getvalue())


if __name__ == '__main__':
    t = T()
    t.a()
    t.a()
    t.a()
    t.get_output()
