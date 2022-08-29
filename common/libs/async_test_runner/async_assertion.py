# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 15:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_assertion.py
# @Software: PyCharm

import operator

from common.libs.data_dict import GlobalsDict
from common.libs.execute_code import execute_code

resp_source_tuple = GlobalsDict.resp_source_tuple()
rule_dict_op = GlobalsDict.rule_dict_op()
value_type_dict = GlobalsDict.value_type_dict()


class AsyncAssertionResponse:
    """异步响应断言"""

    def __init__(self, http_code, resp_headers, resp_json, case_resp_ass_info, data_logs, desc=None, sio=None):
        """

        :param http_code: HTTP状态码
        :param resp_headers: 响应头
        :param resp_json: 响应体
        :param case_resp_ass_info: 断言规则
        :param data_logs: 日志对象
        :param desc: 描述
        :param sio: 日志缓存
        """
        self.http_code = http_code
        self.resp_headers = resp_headers
        self.resp_json = resp_json
        self.case_resp_ass_info = case_resp_ass_info
        self.data_logs = data_logs
        self.desc = desc
        self.sio = sio
        self.response_source_dict = {
            "response_body": self.resp_json,
            "response_headers": self.resp_headers
        }
        self.count = {
            "success": 0,
            "fail": 0,
            "flag": None
        }

    async def result(self, rule, response_source, assert_key, expect_val, expect_val_type, is_expression,
                     python_val_exp, **kwargs):
        """

        :param rule: 规则
        :param response_source: 响应来源
        :param assert_key: 取值的key
        :param expect_val:  期望值
        :param expect_val_type:  期望值类型
        :param is_expression: 是否启用表达式
        :param python_val_exp:  表达式
        :return:
        """

        if response_source not in resp_source_tuple:
            self.sio.log(f"响应来源:{response_source}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"响应来源:{response_source}不存在，无法断言"
            )
            return False
        if rule not in rule_dict_op:
            self.sio.log(f"规则:{rule}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"规则:{rule}不存在，无法断言"
            )
            return False
        if expect_val_type not in value_type_dict:
            self.sio.log(f"期望值类型:{expect_val_type}不存在，无法断言", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"期望值类型:{expect_val_type}不存在，无法断言"
            )
            return False

        # 取值
        source_data = self.response_source_dict.get(response_source)
        try:
            if is_expression:
                expression_result = execute_code(code=python_val_exp, data=source_data)
                assert_val = expression_result.get('result_data')
                self.sio.log(f"=== 公式取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="response_assert",
                    val=f"=== 公式取值结果: {assert_val} ==="
                )
            else:
                assert_val = source_data.get(assert_key)
                self.sio.log(f"=== 取值结果: {assert_val} ===")
                await self.data_logs.add_logs(
                    key="response_assert",
                    val=f"=== 取值结果: {assert_val} ==="
                )
        except BaseException as e:
            self.sio.log(f"数据异常->取值失败:{source_data},键:{assert_key},表达式:{python_val_exp}", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"数据异常->取值失败:{source_data},键:{assert_key},表达式:{python_val_exp}\n异常描述->{e}"
            )
            return False

        # 获取内置函数如:int,str...
        # 将需要断言的值进行转换
        # 如果出现异常很大几率是手动修改了数据库的数据(因为case_assertion_api.py中的CheckAssertion新增断言时会进行校验)
        native_function = value_type_dict.get(expect_val_type)
        try:
            assert_val = native_function(assert_val)
            expect_val = native_function(expect_val)
        except BaseException as e:
            self.sio.log(f"数据异常->内置函数:{native_function}转换值:{assert_val} 时失败", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"数据异常->内置函数:{native_function}转换值:{assert_val} 时失败\n异常描述->{e}"
            )
            return False

        # 日志
        self.sio.log(f'=== 断言:{self.desc} ===')
        kv = '=== 键值:{} ==='.format({assert_key: assert_val})
        self.sio.log(kv)
        message = f'{assert_val}:{type(assert_val)} [{rule}] {expect_val}:{expect_val_type}'
        self.sio.log(f'function: {native_function}')
        self.sio.log(message)
        await self.data_logs.add_logs(
            key="response_assert",
            val=f"=== 断言:{self.desc} ==="
        )
        await self.data_logs.add_logs(
            key="response_assert",
            val=f"{kv}"
        )
        await self.data_logs.add_logs(
            key="response_assert",
            val=f"function: {native_function}"
        )
        await self.data_logs.add_logs(
            key="response_assert",
            val=f"{message}"
        )

        op_function = rule_dict_op.get(rule)
        try:
            if op_function != 'contains':
                assert_result = getattr(operator, op_function)(assert_val, expect_val)
            else:
                assert_result = getattr(operator, op_function)(str(assert_val), str(expect_val))
            return assert_result
        except BaseException as e:
            self.sio.log(f"数据异常->规则:{op_function}错误", status="error")
            self.sio.log(f"异常描述->{e}", status="error")
            await self.data_logs.add_logs(
                key="response_assert",
                val=f"数据异常->规则:{op_function}错误\n异常描述->{e}"
            )
            return False

    async def main(self):
        """main"""

        print('=== AsyncAssertionResponse ===')
        print(self.case_resp_ass_info)
        for index, ass in enumerate(self.case_resp_ass_info, 1):
            ass_result = await self.result(**ass)
            if ass_result:
                self.sio.log('=== Response 断言通过 ===', status='success')
                self.count['success'] += 1
                await self.data_logs.add_logs(
                    key="response_assert",
                    val="=== Response 断言通过 ===",
                    flag=True
                )
            else:
                self.sio.log('=== Response 断言失败 ===', status="error")
                self.count['fail'] += 1
                await self.data_logs.add_logs(
                    key="response_assert",
                    val="=== Response 断言失败 ===",
                    flag=False
                )
        self.count['flag'] = False if self.count.get('fail') > 0 else True
        return self.count


class AsyncAssertionField:
    """异步字段断言"""

    def __init__(self, case_field_ass_info, data_logs, desc=None, sio=None):
        """

        :param case_field_ass_info:
        :param data_logs: 日志对象
        :param desc: 描述
        :param sio: 日志缓存
        """
        self.case_field_ass_info = case_field_ass_info
        self.data_logs = data_logs
        self.desc = desc
        self.sio = sio
        self.count = {
            "success": 0,
            "fail": 0,
        }

    async def main(self):
        """main"""

        print('=== AsyncAssertionField ===')
        self.sio.log(f'=== case_resp_ass_info ===\n{self.case_field_ass_info}\n{self.desc}')

        await self.data_logs.add_logs(
            key="field_assert",
            val=f'=== case_resp_ass_info ===\n{self.case_field_ass_info}\n{self.desc}'
        )
        return self.count
