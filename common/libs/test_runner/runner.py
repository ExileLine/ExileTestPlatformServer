# -*- coding: utf-8 -*-
# @Time    : 2022/8/6 19:52
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : runner.py
# @Software: PyCharm

import json
import requests

from common.libs.StringIOLog import StringIOLog


class CaseRunner:
    """
    同步用例执行
    """

    def __init__(self, test_obj=None):

        self.test_obj = test_obj
        self.sio = test_obj.get('sio', StringIOLog())
        self.end_time = 0

    def json_format(self, d, msg=None):
        """
        json格式打印
        :param d:
        :param msg:
        :return:
        """
        try:
            output = '{}\n'.format(msg) + json.dumps(
                d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False
            )
            self.sio.log(output)
        except BaseException as e:
            self.sio.log('{}\n{}'.format(msg, d))

    def send_logs(self, url, headers, req_json, http_code, resp_headers, resp_json):
        """
        测试用例日志打印
        :param url:
        :param headers:
        :param req_json:
        :param http_code:
        :param resp_headers:
        :param resp_json:
        :return:
        """
        self.sio.log(f'=== url ===\n{url}')
        self.json_format(headers, msg='=== headers ===')
        self.json_format(req_json, msg='=== request json ===')
        self.sio.log(f'=== http_code ===\n{http_code}')
        self.json_format(resp_headers, msg='=== response headers ===')
        self.json_format(resp_json, msg='=== response json ===')

    def request_before(self, a):
        """请求前置"""
        print('request_before', a)

    def request_after(self, a):
        """请求后置"""
        print('request_after', a)

    @classmethod
    def check_method(cls, session, method):
        """检查请求方式"""

        if not hasattr(session, method):
            print(f'错误的请求方式:{method}')
            return False
        return True

    @classmethod
    def check_headers(cls, headers):
        """检查headers"""

        for k, v in headers.items():
            if isinstance(v, (dict, list)):
                headers[k] = json.dumps(v)
        return headers

    def current_request(self, method, **kwargs):
        """同步请求"""

        method = method.lower()
        if not self.check_method:
            response = {
                "error": f"错误的请求方式:{method}"
            }
            return response
        kwargs['headers'] = self.check_headers(kwargs.get('headers'))
        response = getattr(requests, method)(**kwargs, verify=False)
        http_code = response.status_code
        try:
            resp_headers = response.headers
            resp_json = response.json()
            result = {
                "http_code": http_code,
                "resp_json": resp_json,
                "resp_headers": resp_headers
            }
            return result
        except BaseException as e:
            result = {
                "http_code": http_code,
                "resp_error": f"{e}"
            }
            return result
