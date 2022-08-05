# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 15:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_assertion.py
# @Software: PyCharm


class AsyncAssertionResponse:
    """异步响应断言"""

    def __init__(self, http_code, resp_headers, resp_json, sio, case_resp_ass_info, data_logs, desc=None):
        """

        :param http_code: HTTP状态码
        :param resp_headers: 响应头
        :param resp_json: 响应体
        :param sio: 日志缓存
        :param case_resp_ass_info: 断言规则
        :param data_logs: 日志对象
        :param desc: 描述
        """
        self.http_code = http_code
        self.resp_headers = resp_headers
        self.resp_json = resp_json
        self.sio = sio
        self.case_resp_ass_info = case_resp_ass_info
        self.data_logs = data_logs
        self.desc = desc

    async def main(self):
        """main"""

        print('=== AsyncAssertionResponse ===')
        self.sio.log(f'=== case_resp_ass_info ===\n{self.case_resp_ass_info}\n{self.desc}')

        await self.data_logs.add_logs(
            key="response_assert",
            val=f'=== case_resp_ass_info ===\n{self.case_resp_ass_info}\n{self.desc}'
        )


class AsyncAssertionField:
    """异步字段断言"""

    def __init__(self, sio, case_field_ass_info, data_logs, desc=None):
        """

        :param sio:
        :param case_field_ass_info:
        :param data_logs: 日志对象
        :param desc:
        """
        self.sio = sio
        self.case_field_ass_info = case_field_ass_info
        self.data_logs = data_logs
        self.desc = desc

    async def main(self):
        """main"""

        print('=== AsyncAssertionField ===')
        self.sio.log(f'=== case_resp_ass_info ===\n{self.case_field_ass_info}\n{self.desc}')

        await self.data_logs.add_logs(
            key="field_assert",
            val=f'=== case_resp_ass_info ===\n{self.case_field_ass_info}\n{self.desc}'
        )
