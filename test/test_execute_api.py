# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 17:45
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_execute_api.py
# @Software: PyCharm


import time
import unittest

from test.test_tools import current_request

url = 'http://0.0.0.0:7878/api/case_execute'


class TestExecuteApi(unittest.TestCase):

    def test_001(self):
        """创建成功"""

        json_data = {
            "execute_id": 635,
            "execute_type": "case",
            "execute_label": "only",
            "data_driven": False,
            "is_env_cover": False,
            "env_url_id": 1,
            "use_dd_push": False,
            "dd_push_id": 1,
            "use_mail": False,
            "mail_send_all": False,
            "mail_list": [],
            "request_timeout": 100
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)


if __name__ == '__main__':
    unittest.main()
