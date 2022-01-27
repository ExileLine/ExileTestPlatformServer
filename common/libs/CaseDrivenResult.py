# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:19 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CaseDrivenResult.py
# @Software: PyCharm


import re
import json
import time
import datetime
import shortuuid

import requests
from loguru import logger

from common.libs.db import project_db, R
from common.libs.public_func import check_keys
from common.libs.assert_related import AssertResponseMain, AssertFieldMain
from common.libs.StringIOLog import StringIOLog
from common.libs.execute_code import execute_code

var_func_dict = {
    "Date": str(datetime.datetime.now().date()),
    "Time": str(datetime.datetime.now().time()),
    "DateTime": str(datetime.datetime.now()),
    "TimeStamp": str(int(time.time())),
    "UUID": shortuuid.uuid()[0:10] + str(int(time.time())) + shortuuid.uuid()[0:10]
}


class TestResult:
    """测试结果"""

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
        self.field_ass_error = 0
        self.field_ass_success_rate = 0
        self.field_ass_fail_rate = 0
        self.field_ass_error_rate = 0

    def get_test_result(self):
        """

        :return:
        """
        self.req_count = self.req_success + self.req_error
        self.req_success_rate = "{}%".format(round(self.req_success / self.req_count, 2) * 100)
        self.req_error_rate = "{}%".format(round(self.req_error / self.req_count, 2) * 100)
        self.resp_ass_count = self.resp_ass_success + self.resp_ass_fail

        self.resp_ass_success_rate = 0 if self.resp_ass_success == 0 else "{}%".format(
            round(self.resp_ass_success / self.resp_ass_count, 2) * 100)

        self.resp_ass_fail_rate = 0 if self.resp_ass_fail == 0 else "{}%".format(
            round(self.resp_ass_fail / self.resp_ass_count, 2) * 100)

        self.field_ass_count = self.field_ass_success + self.field_ass_fail + self.field_ass_error

        self.field_ass_success_rate = 0 if self.field_ass_success == 0 else "{}%".format(
            round(self.field_ass_success / self.field_ass_count, 2) * 100)

        self.field_ass_fail_rate = 0 if self.field_ass_fail == 0 else "{}%".format(
            round(self.field_ass_fail / self.field_ass_count, 2) * 100)

        self.field_ass_error_rate = 0 if self.field_ass_error == 0 else "{}%".format(
            round(self.field_ass_error / self.field_ass_count, 2) * 100)

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
            "field_ass_error": self.field_ass_error,
            "field_ass_success_rate": self.field_ass_success_rate,
            "field_ass_fail_rate": self.field_ass_fail_rate,
            "field_ass_error_rate": self.field_ass_error_rate
        }
        return d


class MainTest:
    """
    测试执行

    1.转换参数:
        MainTest.assemble_data_send()√
            MainTest.var_conversion() √

    2.发出请求:
        MainTest.assemble_data_send() √
            MainTest.current_request() √

    3.resp断言前置检查:
        MainTest.resp_check_ass_execute() √
        MainTest.check_resp_ass_keys() √

    4.resp断言执行:
        MainTest.resp_check_ass_execute() √
        MainTest.execute_resp_ass() -> AssertMain.assert_resp_main() √

    5.更新变量:
        MainTest.field_check_ass_execute() √
            MainTest.update_var() √

    6.field断言前置检查:
        MainTest.field_check_ass_execute() √
            MainTest.check_field_ass_keys() √

    7.field断言执行:
        MainTest.field_check_ass_execute() √
            MainTest.execute_field_ass() -> AssertMain.assert_field_main() √

    8.日志记录:
        MainTest.main()

    9.生成报告:

    """

    # TODO field 前置查询 {"before_query":"select xxx from xxx....","before_field":"username"}
    # TODO sio优化
    # TODO yield 优化 list 消费
    # TODO decimal.Decimal 优化统计数据
    # TODO 消息推送(邮件, 钉钉, 微信)

    def __init__(self, test_obj):
        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.case_list = test_obj.get('case_list', [])
        self.data_driven = test_obj.get('data_driven')
        self.execute_id = test_obj.get('execute_id')
        self.execute_name = test_obj.get('execute_name')
        self.execute_type = test_obj.get('execute_type')
        self.execute_user_id = test_obj.get('execute_user_id')
        self.execute_username = test_obj.get('execute_username')
        self.sio = test_obj.get('sio', StringIOLog())

        if not isinstance(self.case_list, list) or not self.case_list:
            raise TypeError('TestLoader.__init__.case_list 类型错误')

        self.case_list = self.case_list
        self.test_result = TestResult()
        self.current_case_resp_ass_error = 0
        self.case_result_list = []

        self.create_time = str(datetime.datetime.now())
        self.start_time = time.time()
        self.end_time = 0

    def json_format(self, d, msg=None):
        """json格式打印"""
        try:
            output = '{}\n'.format(msg) + json.dumps(
                d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False
            )
            self.sio.log(output)
        except BaseException as e:
            self.sio.log('{}\n{}'.format(msg, d))

    def show_log(self, url, headers, req_json, resp_headers, resp_json):
        """测试用例日志打印"""
        self.sio.log('test url\n{}'.format(url))
        self.json_format(headers, msg='test headers')
        self.json_format(req_json, msg='test req_json')
        self.json_format(resp_headers, msg='test resp_headers')
        self.json_format(resp_json, msg='test resp_json')

    def var_conversion(self, before_var):
        """变量转换参数"""

        before_var_init = before_var
        if isinstance(before_var_init, (list, dict)):
            before_var = json.dumps(before_var, ensure_ascii=False)

        result_list = re.findall('\\$\\{([^}]*)', before_var)

        if not result_list:
            return before_var_init

        err_var_list = []
        current_dict = {}
        for res in result_list:
            sql = """select var_value from exile_test_variable where var_name='{}';""".format(res)
            query_result = project_db.select(sql=sql, only=True)
            if query_result:
                current_dict[res] = json.loads(query_result.get('var_value'))
            elif var_func_dict.get(res):
                current_dict[res] = var_func_dict.get(res)
            else:
                err_var_list.append(res)

        if not current_dict:
            self.sio.log('===未找到变量:{}对应的参数==='.format(err_var_list))
            return before_var_init

        current_str = before_var
        for k, v in current_dict.items():
            old_var = "${%s}" % (k)
            new_var = v
            current_str = current_str.replace(old_var, new_var)
        if isinstance(before_var_init, (list, dict)):
            current_str = json.loads(current_str)
        # print(current_str)
        return current_str

    def check_resp_ass_keys(self, assert_list):
        """
        检查resp断言对象参数类型是否正确
        assert_list: ->list 规则列表
        """

        cl = ["assert_key", "expect_val", "expect_val_type", "is_expression", "python_val_exp", "rule"]

        if not isinstance(assert_list, list) or not assert_list:
            self.sio.log("assert_list:类型错误{}".format(assert_list))
            return False

        for ass in assert_list:
            if not check_keys(ass, *cl):
                self.sio.log("缺少需要的键值对:{}".format(ass), status='error')
                return False
        return True

    def check_field_ass_keys(self, assert_list):
        """
        检查field断言对象参数类型是否正确
        assert_list: ->list 规则列表
        """

        cl = ["assert_key", "expect_val", "expect_val_type", "rule"]

        if not isinstance(assert_list, list) or not assert_list:
            self.sio.log("assert_list:类型错误{}".format(assert_list))
            return False

        for ass in assert_list:
            child_assert_list = ass.get('assert_list')
            for ass_child in child_assert_list:
                if not check_keys(ass_child, *cl):
                    self.sio.log("缺少需要的键值对:{}".format(ass), status='error')
                    return False
        return True

    def execute_resp_ass(self, resp_ass_list, assert_description):
        """
        执行Resp断言
        resp_ass_list demo
            [
                {
                    "assert_key": "code",
                    "expect_val": "200",
                    "expect_val_type": "1",
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                },
                {
                    "assert_key": "message",
                    "expect_val": "index",
                    "expect_val_type": "1",
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                }
            ]
        """
        for resp_ass_dict in resp_ass_list:
            # print(resp_ass_dict)
            new_resp_ass = AssertResponseMain(
                sio=self.sio,
                resp_json=self.resp_json,
                resp_headers=self.resp_headers,
                assert_description=assert_description,
                **resp_ass_dict
            )
            resp_ass_result = new_resp_ass.main()
            # print(resp_ass_result)
            if resp_ass_result.get('status'):  # [bool,str]
                self.test_result.resp_ass_success += 1
            else:
                self.test_result.resp_ass_fail += 1
                self.current_case_resp_ass_error += 1

    def execute_field_ass(self, field_ass_list, assert_description):
        """
        执行Field断言
        """

        for field_ass_dict in field_ass_list:
            # print(field_ass_dict)
            new_field_ass = AssertFieldMain(
                sio=self.sio,
                assert_description=assert_description,
                **field_ass_dict
            )

            field_ass_result = new_field_ass.main()

            self.test_result.field_ass_success += field_ass_result.get('success')
            self.test_result.field_ass_fail += field_ass_result.get('fail')
            self.test_result.field_ass_error += field_ass_result.get('error')

    def current_request(self, method=None, **kwargs):
        """
        构造请求
        :param method: 请求方式
        :param kwargs: 请求体以及扩展参数
        :return:
        """

        if hasattr(requests, method):
            response = getattr(requests, method)(**kwargs, verify=False)
            self.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=response.json(),
                resp_headers=response.headers
            )
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            self.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=response,
                resp_headers={}
            )
        return response

    def assemble_data_send(self, case_data_info):
        """
        组装数据发送并且更新变量
        :return:
        """

        request_params = case_data_info.get('request_params')
        request_body = case_data_info.get('request_body')
        request_headers = case_data_info.get('request_headers')
        request_body_type = str(case_data_info.get('request_body_type'))
        self.update_var_list = case_data_info.get('update_var_list')

        req_type_dict = {
            "1": {"data": request_body},
            "2": {"json": request_body},
            "3": {"data": request_body}
        }

        method = self.request_method.lower()
        self.sio.log('=== method: {} ==='.format(method))

        url = self.base_url + self.request_url if self.use_base_url else self.request_base_url + self.request_url

        before_send = {
            "url": url,
            "headers": request_headers,
        }
        req_json_data = req_type_dict.get(request_body_type)

        if method == 'get':
            before_send['params'] = request_params
        else:
            before_send.update(req_json_data)

        send = self.var_conversion(before_send)
        self.sio.log('=== send: {} ==='.format(send))

        resp = self.current_request(method=method, **send)
        self.resp_json = resp.json()
        self.resp_headers = resp.headers
        self.json_format(self.resp_json, '用例:{} -> resp_json'.format(self.case_name))
        self.json_format(self.resp_headers, '用例:{} -> resp_headers'.format(self.case_name))

    def resp_check_ass_execute(self, case_resp_ass_info):
        """
        检查 resp 断言规则并执行断言
        :return:
        """
        if not case_resp_ass_info:
            self.sio.log('=== case_resp_ass_info is [] ===')
            return False

        for resp_ass in case_resp_ass_info:  # 遍历断言规则逐一校验
            resp_ass_list = resp_ass.get('ass_json')
            assert_description = resp_ass.get('assert_description')
            # print(resp_ass_list)
            if self.check_resp_ass_keys(assert_list=resp_ass_list):  # 响应检验
                self.execute_resp_ass(resp_ass_list=resp_ass_list, assert_description=assert_description)
            else:
                self.sio.log('=== check_ass_keys error ===', status='error')
                # return False

    def field_check_ass_execute(self, case_field_ass_info):
        """
        检查 field 断言规则并执行断言
        :return:
        """
        if self.current_case_resp_ass_error == 0:  # 所有resp断言规则通过
            self.update_var()  # 更新变量
            for field_ass in case_field_ass_info:
                field_ass_list = field_ass.get('ass_json')
                assert_description = field_ass.get('assert_description')
                # print(field_ass_list)
                if self.check_field_ass_keys(assert_list=field_ass_list):  # 数据库校验
                    for field_ass_child in field_ass_list:
                        assert_list = field_ass_child.get('assert_list')
                    self.execute_field_ass(
                        field_ass_list=field_ass_list,
                        assert_description=assert_description
                    )
                else:
                    return False

        else:
            self.sio.log('=== 断言规则没有100%通过,失败数:{} 不更新变量以及不进行数据库校验 ==='.format(self.current_case_resp_ass_error))

    def update_var(self):
        """更新变量"""

        var_source_dict = {
            "resp_data": self.resp_json,
            "resp_headers": self.resp_headers
        }

        if not self.update_var_list:
            self.sio.log('=== 更新变量列表为空不需要更新变量===')

        for up in self.update_var_list:
            """
            {
                "id": 3,
                "var_value":"123",
                "var_source": "resp_data",
                "expression": "obj.get('code')",
                "is_expression":0,
                "var_get_key": "code"
            }
            """
            id = up.get('id')
            var_value = up.get('var_value')
            var_source = up.get('var_source')
            var_get_key = up.get('var_get_key')
            expression = up.get('expression')
            is_expression = up.get('is_expression', 0)
            data = var_source_dict.get(var_source)

            if bool(is_expression):
                # 表达式取值
                result_json = execute_code(code=expression, data=data)
                update_val_result = result_json.get('result_data')
            else:
                # 直接取值
                update_val_result = data.get(var_get_key)

            old_var = json.dumps(var_value, ensure_ascii=False)
            new_var = json.dumps(update_val_result, ensure_ascii=False)

            sql = """UPDATE exile_test_variable SET var_value='{}' WHERE id='{}';""".format(new_var, id)
            self.sio.log('=== update sql === 【 {} 】'.format(sql), status='success')
            project_db.update_data(sql)

            sql2 = """INSERT INTO exile_test_variable_history ( `create_timestamp`, `is_deleted`, `var_id`, `update_type`, `creator`, `creator_id`, `before_var`, `after_var`) VALUES ('{}',  '0',  '{}', '执行用例更新', '{}', '{}', '{}', '{}');""".format(
                int(self.start_time), id, self.execute_username, self.execute_user_id, old_var, new_var
            )
            self.sio.log('=== update history sql === 【 {} 】'.format(sql2), status='success')
            project_db.create_data(sql2)

    def save_logs(self, log_id):
        """

        :param log_id: 日志id
        :return:
        """

        sql = """INSERT INTO exile_test_execute_logs (`is_deleted`, `create_time`, `create_timestamp`,  `execute_id`, `execute_name`, `execute_type`, `redis_key`, `creator`, `creator_id`) VALUES (0,'{}','{}','{}','{}','{}','{}','{}','{}');""".format(
            self.create_time.split('.')[0],
            int(self.end_time),
            self.execute_id,
            self.execute_name,
            self.execute_type,
            log_id,
            self.execute_username,
            self.execute_user_id
        )
        project_db.create_data(sql)
        logger.success('=== save_logs ok ===')

    def main(self):
        """main"""

        for case_index, case in enumerate(self.case_list, 1):
            self.sio.log('=== start case: {} ==='.format(case_index))
            self.current_case_resp_ass_error = 0
            case_info = case.get('case_info', {})
            bind_info = case.get('bind_info', [])

            self.case_id = case_info.get('id')
            self.case_name = case_info.get('case_name')

            self.request_base_url = case_info.get('request_base_url')
            self.request_url = case_info.get('request_url')
            self.request_method = case_info.get('request_method')
            self.update_var_list = []

            self.resp_json = {}
            self.resp_headers = {}

            if not bind_info:
                self.sio.log('=== 未配置请求参数 ===')

            for index, bind in enumerate(bind_info, 1):

                self.sio.log("=== 数据驱动:{} ===".format(index))
                case_data_info = bind.get('case_data_info', {})
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                try:
                    self.test_result.req_success += 1
                    self.assemble_data_send(case_data_info=case_data_info)
                except BaseException as e:
                    self.sio.log("=== 请求失败:{} ===".format(str(e)), status="error")
                    self.test_result.req_error += 1
                    self.sio.log("=== 跳过断言 ===")
                    continue

                self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

                if not self.data_driven:
                    self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                    break

            self.sio.log('=== end case: {} ===\n\n'.format(case_index))

            add_case = {
                "case_id": self.case_id,
                "case_name": self.case_name,
                "case_log": self.sio.get_stringio(),
            }
            self.case_result_list.append(add_case)

        logger.info('=== save redis start ===')

        case_summary = self.test_result.get_test_result()
        self.end_time = time.time()
        save_key = "test_log_{}_{}".format(str(int(time.time())), shortuuid.uuid())
        return_case_result = {
            "uuid": save_key,
            "case_result_list": self.case_result_list,
            "result_summary": case_summary,
            "create_time": self.create_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": self.end_time - self.start_time
        }
        R.set(save_key, json.dumps(return_case_result))

        current_save_dict = {
            "case": "case_first_log:{}".format(self.execute_id),
            "scenario": "scenario_first_log:{}".format(self.execute_id)
        }
        save_obj_first = current_save_dict.get(self.execute_type, "未知执行类型")
        R.set(save_obj_first, json.dumps(return_case_result))

        logger.success('=== save redis ok ===')

        self.save_logs(log_id=save_key)

    def __str__(self):
        return '\n'.join(["{}:{}".format(k, v) for k, v in self.__dict__.items()])
