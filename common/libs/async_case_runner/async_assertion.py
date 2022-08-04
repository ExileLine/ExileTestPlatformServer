# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 15:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_assertion.py
# @Software: PyCharm


class AsyncAssertionResponse:
    """异步响应断言"""

    def __init__(self, http_code, resp_headers, resp_json, sio, case_resp_ass_info, desc=None):
        """

        :param http_code: HTTP状态码
        :param resp_headers: 响应头
        :param resp_json: 响应体
        :param sio: 日志缓存
        :param case_resp_ass_info: 断言规则
        """
        self.http_code = http_code
        self.resp_headers = resp_headers
        self.resp_json = resp_json
        self.sio = sio
        self.case_resp_ass_info = case_resp_ass_info
        self.desc = desc

    async def main(self):
        """main"""

        print('=== AsyncAssertionResponse ===')
        self.sio.log(f'=== case_resp_ass_info ===\n{self.case_resp_ass_info}\n{self.desc}')


class AsyncAssertionField:
    """异步字段断言"""

    def __init__(self, sio, case_field_ass_info, desc=None):
        self.sio = sio
        self.case_field_ass_info = case_field_ass_info
        self.desc = desc

    async def main(self):
        """main"""

        print('=== AsyncAssertionField ===')
        self.sio.log(f'=== case_resp_ass_info ===\n{self.case_field_ass_info}\n{self.desc}')
