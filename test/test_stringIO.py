# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 10:26 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_stringIO.py
# @Software: PyCharm


import io
import sys
from shortuuid import uuid
from loguru import logger


class T:

    def __init__(self):
        self.output = io.StringIO()

    def log(self, msg, status='info'):
        getattr(logger, status)(str(msg))
        self.output.write(str(msg) + '\n')

    def get_output(self):
        print(self.output.getvalue())


if __name__ == '__main__':
    # t = T()
    # t.log(123)
    # t.log(456)
    # t.log(789, status='success')
    # t.get_output()

    out_put1 = io.StringIO()

    out_put1.write('123')
    print(out_put1.getvalue())

