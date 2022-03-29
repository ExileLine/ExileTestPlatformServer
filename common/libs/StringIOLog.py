# -*- coding: utf-8 -*-
# @Time    : 2021/9/21 11:00 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : StringIOLog.py
# @Software: PyCharm

import io

from loguru import logger


class StringIOLog:
    """日志收集缓存"""

    def __init__(self):
        self.output = io.StringIO()
        self.output_value = None

    def log(self, msg, status='info'):
        getattr(logger, status)(str(msg))
        self.output.write(str(msg) + '\n')

    def get_stringio(self):
        """获取 stringio 值"""
        self.output_value = self.output.getvalue()
        # print(self.output_value)
        # self.output = io.StringIO()
        self.output.truncate(0)
        self.output.seek(0)
        return self.output_value
