# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 15:05
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_result.py
# @Software: PyCharm

from decimal import Decimal


class AsyncTestResult:
    """异步测试结果数据统计"""

    def __init__(self):
        self.req_count = 0
        self.req_success = 0
        self.req_error = 0
        self.req_success_rate = 0
        self.req_error_rate = 0

        self.resp_ass_count = 0
        self.resp_ass_success = 0
        self.resp_ass_fail = 0
        self.resp_ass_success_rate = 0
        self.resp_ass_fail_rate = 0

        self.field_ass_count = 0
        self.field_ass_success = 0
        self.field_ass_fail = 0
        self.field_ass_success_rate = 0
        self.field_ass_fail_rate = 0

        self.all_ass_count = 0
        self.all_ass_success_count = 0
        self.all_ass_fail_count = 0

        self.pass_count = 0
        self.pass_rate = 0
        self.fail_count = 0
        self.fail_rate = 0
        self.all_test_count = 0
        self.all_test_rate = 0

    async def add_resp_ass(self, d: dict):
        """响应断言计数"""

        self.resp_ass_success += d.get('success')
        self.resp_ass_fail += d.get('fail')

    async def add_field_ass(self, d: dict):
        """字段断言计数"""

        self.field_ass_success += d.get('success')
        self.field_ass_fail += d.get('fail')

    @classmethod
    async def gen_rate(cls, first, last):
        """生成%,保留两位"""

        return f"{Decimal(first / last * 100).quantize(Decimal('1.00'))}%"

    async def get_test_result(self):
        """
        获取测试结果
        :return:
        """

        self.req_count = self.req_success + self.req_error
        if self.req_count != 0:
            self.req_success_rate = self.gen_rate(self.req_success, self.req_count)
            self.req_error_rate = self.gen_rate(self.req_error, self.req_count)

            self.resp_ass_count = self.resp_ass_success + self.resp_ass_fail
            if self.resp_ass_count != 0:
                self.resp_ass_success_rate = self.gen_rate(self.resp_ass_success, self.resp_ass_count)
                self.resp_ass_fail_rate = self.gen_rate(self.resp_ass_fail, self.resp_ass_count)

            self.field_ass_count = self.field_ass_success + self.field_ass_fail

            if self.field_ass_count != 0:
                self.field_ass_success_rate = self.gen_rate(self.field_ass_success, self.field_ass_count)
                self.field_ass_fail_rate = self.gen_rate(self.field_ass_fail, self.field_ass_count)

            self.all_ass_count = self.resp_ass_count + self.field_ass_count

            self.all_test_count = self.pass_count + self.fail_count

            if self.all_test_count != 0:
                self.pass_rate = self.gen_rate(self.pass_count, self.all_test_count)
                self.fail_rate = self.gen_rate(self.fail_count, self.all_test_count)

        d = {
            "req_count": self.req_count,
            "req_success": self.req_success,
            "req_error": self.req_error,
            "req_success_rate": self.req_success_rate,
            "req_error_rate": self.req_error_rate,

            "resp_ass_count": self.resp_ass_count,
            "resp_ass_success": self.resp_ass_success,
            "resp_ass_fail": self.resp_ass_fail,
            "resp_ass_success_rate": self.resp_ass_success_rate,
            "resp_ass_fail_rate": self.resp_ass_fail_rate,

            "field_ass_count": self.field_ass_count,
            "field_ass_success": self.field_ass_success,
            "field_ass_fail": self.field_ass_fail,
            "field_ass_success_rate": self.field_ass_success_rate,
            "field_ass_fail_rate": self.field_ass_fail_rate,

            "all_ass_count": self.all_ass_count,

            "all_test_count": self.all_test_count,
            "pass_count": self.pass_count,
            "pass_rate": self.pass_rate,
            "fail_count": self.fail_count,
            "fail_rate": self.fail_rate
        }
        return d
