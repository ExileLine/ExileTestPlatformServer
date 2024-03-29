# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:19 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : CaseDrivenResult.py
# @Software: PyCharm


"""
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
该函数已经无法在新的数据结构中使用,保留仅用于重构过程中作为参考!
"""

import os
import sys
import re
import json
import time
import datetime
import traceback
from decimal import Decimal

import requests
import shortuuid
from loguru import logger

from common.libs.db import project_db, R
from common.libs.data_dict import GlobalsDict
from common.libs.assert_related import AssertResponseMain, AssertFieldMain
from common.libs.StringIOLog import StringIOLog
from common.libs.report_template import RepostTemplate
from common.libs.execute_code import execute_code
from common.libs.data_dict import F, execute_label_tuple
from common.tools.send_mail import SendEmail
from common.tools.message_push import MessagePush
from config.config import config_obj

# 变量转换函数字典
var_func_dict = {
    "7": F.gen_uuid_long,  # uuid
    "8": F.gen_uuid_short,  # short_uuid
    "9": F.gen_date,  # date(年月日-2022-01-01)
    "10": F.gen_time,  # time(时分秒-09:30:00.123456)
    "11": F.gen_datetime,  # datetime(年月日时分秒-2022-01-01 09:30:00.123456)
    "12": F.gen_timestamp  # timestamp(时间戳)
}


class TestResult:
    """测试结果数据统计"""

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

    @classmethod
    def gen_rate(cls, first, last):
        """生成%,保留两位"""

        return f"{Decimal(first / last * 100).quantize(Decimal('1.00'))}%"

    def get_test_result(self):
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

    4.resp断言执行:
        MainTest.resp_check_ass_execute() √
        MainTest.execute_resp_ass() -> AssertMain.assert_resp_main() √

    5.更新变量:
        MainTest.field_check_ass_execute() √
            MainTest.update_var() √

    6.field断言前置检查:
        MainTest.field_check_ass_execute() √

    7.field断言执行:
        MainTest.field_check_ass_execute() √
            MainTest.execute_field_ass() -> AssertMain.assert_field_main() √

    8.日志记录:
        MainTest.main()

    9.生成报告:
        MainTest.save_test_repost()
    """

    # TODO field 前置查询 {"before_query":"select xxx from xxx....","before_field":"username"}
    # TODO sio优化
    # TODO yield 优化 list 消费

    def __init__(self, test_obj=None):

        if not test_obj:
            test_obj = {}

        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.data_driven = test_obj.get('data_driven')

        self.execute_id = test_obj.get('execute_id')
        self.execute_name = test_obj.get('execute_name')
        self.execute_type = test_obj.get('execute_type')
        self.execute_label = test_obj.get('execute_label', '')

        self.execute_user_id = test_obj.get('execute_user_id')
        self.execute_username = test_obj.get('execute_username')
        self.sio = test_obj.get('sio', StringIOLog())

        self.is_execute_all = test_obj.get('is_execute_all', False)
        self.execute_dict = test_obj.get('execute_dict', {})
        self.case_list = test_obj.get('case_list', [])

        self.is_dd_push = test_obj.get('is_dd_push', False)
        self.dd_push_id = test_obj.get('dd_push_id')
        self.ding_talk_url = test_obj.get('ding_talk_url')

        self.is_send_mail = test_obj.get('is_send_mail', False)
        self.mail_list = test_obj.get('mail_list')

        self.is_safe_scan = test_obj.get('is_safe_scan', False)
        self.safe_scan_proxies_url = test_obj.get('safe_scan_proxies_url', False)
        self.call_safe_scan_data = test_obj.get('call_safe_scan_data')
        self.safe_scan_report_url = test_obj.get('safe_scan_report_url')
        self.proxies = {}

        self.trigger_type = test_obj.get('trigger_type', 'user_execute')

        self.request_timeout = test_obj.get('request_timeout', 3)

        if not isinstance(self.case_list, list):
            raise TypeError('MainTest.__init__.case_list 类型错误')

        if test_obj and self.execute_label not in execute_label_tuple:
            raise TypeError('MainTest.__init__.execute_label 类型错误')

        self.func_name = self.execute_label + "_execute"

        if self.is_execute_all:
            case_list = self.execute_dict.get('case_list', [])
            self.case_generator = (case for case in case_list)
            scenario_list = self.execute_dict.get('scenario_list', [])
            self.scenario_generator = (scenario for scenario in scenario_list)
        else:
            self.case_generator = (case for case in self.case_list)

        self.id_after_execution = []  # 已经执行的用例id,用于在最后更新用例的执行次数

        self.var_conversion_active_list = []
        self.current_var_value = ""

        self.current_assert_description = None

        self.full_pass = True  # 本次是否完全通过
        self.current_case_resp_ass_error = 0  # 当次用例响应断言错误数
        self.current_logs_error_switch = False  # 日志错误标识(多场景中使用)
        self.logs_error_switch = False  # 日志错误标识(都会用到)

        self.test_result = TestResult()  # 测试结果
        self.case_result_list = []  # 测试结果日志集

        self.create_time = str(datetime.datetime.now()).split(".")[0]
        self.start_time = time.time()
        self.end_time = 0
        self.total_time = 0

        self.save_key = ""
        self.execute_status = True
        self.report_name = ""
        self.path = f"{config_obj['new'].STATIC_FOLDER}/api/"
        self.report_url = ""

    def safe_scan(self):
        """
        安全扫描
        :return:
        """

        if self.is_safe_scan:
            try:
                print('=== 启动安全扫描 ===')
                print(self.call_safe_scan_data)
                resp = requests.post(**self.call_safe_scan_data, timeout=5)
                print(resp.json())
                code = resp.json().get("code")
                if code == 200:
                    time.sleep(5)
                    self.proxies = {
                        # 'http': '192.168.14.214:7777',
                        # 'https': '192.168.14.214:7777',
                        'http': self.safe_scan_proxies_url,
                        'https': self.safe_scan_proxies_url
                    }
                    print("=== 设置安全扫码代理 ===")
                    print(self.proxies)
                else:
                    self.sio.log(f'=== 启动安全扫描失败:{code} ===')
            except BaseException as e:
                self.sio.log(f'=== 启动安全扫描失败:{str(e)} ===')

    def reset_current_data(self):
        """重置"""

        self.full_pass = True
        self.current_logs_error_switch = False
        self.logs_error_switch = False
        self.current_case_resp_ass_error = 0

    def set_case_count(self):
        """设置用例统计"""

        if self.full_pass:
            self.test_result.pass_count += 1
        else:
            self.test_result.fail_count += 1

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
        self.sio.log(f'=== url ===\n{url}')
        self.json_format(headers, msg='=== headers ===')
        self.json_format(req_json, msg='=== request json ===')
        self.json_format(resp_headers, msg='=== response headers ===')
        self.json_format(resp_json, msg='=== response json ===')

    def gen_case_data_ready(self, data_ready):
        """
        {
            "db_id": 12,
            "query_list": [
                {
                    "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                    "field_list": [
                        {
                            "var_id": 3,
                            "field_name": "id",
                            "field_type": "1",
                            "is_expression": 0,
                            "python_val_exp": "obj.get(\"id\")"
                        },
                        {
                            "var_id": 3,
                            "field_name": "case_name",
                            "field_type": "2",
                            "is_expression": 0,
                            "python_val_exp": "obj.get(\"case_name\")"
                        }
                    ]
                }
            ]
        }
        :param data_ready:
        :return:
        """
        db_id = data_ready.get("db_id")
        query_list = data_ready.get("query_list")
        ass = AssertFieldMain(sio=self.sio, db_id=db_id)
        ass.query_db_connection()
        ass.ping_db_connection(from_data_ready=True)
        db_obj = ass.db_obj.get('db')
        print(db_obj)
        for q in query_list:
            print("=== q ===")
            print(q)
            sql = q.get('query')
            print(sql)
            field_list = q.get('field_list')
            result = db_obj.select(sql=sql, only=True)
            print(result)
            if not result:
                self.sio.log(f"=== 获取数据为空:{sql} ===", status="error")
                continue
            for field in field_list:
                print("=== field ===")
                print(field)
                field_name = field.get('field_name')
                print(field_name)
                if field.get('field_type') in (1, '1'):  # TODO 因为从最开始定义的字典不一致,这里只能手动增加逻辑
                    field_type = 2
                elif field.get('field_type') in (2, '2'):
                    field_type = 1
                else:
                    print("=== else ===")
                    field_type = field.get('field_type')

                print("=== field_type ===")
                print(field_type)

                is_expression = field.get('is_expression')
                python_val_exp = field.get('python_val_exp')
                if is_expression:
                    result_json = execute_code(code=python_val_exp, data=result)
                    field_value = result_json.get('result_data')
                    self.sio.log(f"=== 公式取值结果: {field_value} ===")
                else:
                    field_value = result.get(field_name)

                field_value = json.dumps(field_value, ensure_ascii=False)
                var_id = field.get('var_id')

                query_var = f"""SELECT * FROM `ExileTestPlatform`.`exile_test_variable` WHERE id={var_id};"""
                print(query_var)
                var_obj = project_db.select(sql=query_var, only=True)
                print(var_obj)

                if not var_obj:
                    self.sio.log(f"=== 变量id: {var_id} 不存在 ===")
                    continue

                var_name = var_obj.get('var_name')
                update_var = f"""UPDATE `ExileTestPlatform`.`exile_test_variable` SET var_value='{field_value}', var_type={field_type} WHERE id={var_id};"""
                print(update_var)
                project_db.update(sql=update_var)
                self.sio.log(f"=== 更新变量: {var_name} 成功 ===")

    def case_data_before(self, case_data_info):
        """参数前置准备"""

        print("=== 参数前置准备 ===")
        print(case_data_info)
        is_before = case_data_info.get('is_before')
        data_before = case_data_info.get('data_before')

        try:
            if is_before:
                data_before = self.var_conversion(data_before)
                print('=== data_before ===')
                print(data_before)
                list(map(self.gen_case_data_ready, data_before))
        except BaseException as e:
            self.sio.log(f"=== 参数前置准备失败:{str(e)} ===", status="error")

    def case_data_after(self, case_data_info):
        """参数后置准备"""

        print("=== 参数后置准备 ===")
        print(case_data_info)
        is_after = case_data_info.get('is_after')
        data_after = case_data_info.get('data_after')

        try:
            if is_after:
                data_after = self.var_conversion(data_after)
                print('=== data_after ===')
                print(data_after)
                list(map(self.gen_case_data_ready, data_after))
        except BaseException as e:
            self.sio.log(f"=== 参数后置准备失败:{str(e)} ===", status="error")

    @staticmethod
    def update_case_total_execution(case_id_list, n=1):
        """更新用例执行数"""

        sql = f"""
        UPDATE exile_test_case 
        SET total_execution = total_execution + {n} 
        WHERE 
        {f'id={case_id_list[-1]}' if len(case_id_list) == 1 else f'id in {tuple(case_id_list)}'}
        """
        project_db.update(sql)
        print(f'共 {len(case_id_list)} 条, 更新用例执行数成功:{case_id_list}')

    def var_conversion_main(self, json_str, d):
        """
        变量转换参数
        :param json_str: json字符串
        :param d: 数据字典
        :return:
        """
        matchList = re.findall(r'("?\$\{.*?\}.*?")', json_str)
        for match in matchList:
            varList = re.findall(r'\$\{.*?\}', match)
            if len(varList) > 1:
                _match = match
                for var in varList:
                    key = var[2:-1]
                    val = d.get(key)
                    if val:
                        if isinstance(val, int):
                            _match = _match.replace('${' + key + '}', json.dumps(val, ensure_ascii=False))
                        elif isinstance(val, str):
                            _match = _match.replace('${' + key + '}', json.dumps(val, ensure_ascii=False)[1:-1])
                        else:
                            _match = _match.replace('${' + key + '}',
                                                    re.sub(r'"', '\\"', json.dumps(val, ensure_ascii=False)))
                json_str = json_str.replace(match, _match)
            else:
                _matchList = re.findall(r'\$\{(.*?)\}(.*?")', match)
                key = _matchList[0][0]
                val = d.get(key)
                if val:
                    if _matchList[0][1] == '"':
                        if isinstance(val, str):
                            json_str = json_str.replace(match, match.replace('${' + key + '}', val))
                        else:
                            json_str = json_str.replace(match, match.replace('${' + key + '}',
                                                                             json.dumps(val, ensure_ascii=False))[1:-1])
                    else:
                        if isinstance(val, str):
                            json_str = json_str.replace(match, match.replace('${' + key + '}', val))
                        else:
                            res = match.replace('${' + key + '}',
                                                re.sub(r'"', '\\"', json.dumps(val, ensure_ascii=False)))
                            json_str = json_str.replace(match, res)

        result_data = json.loads(json_str)
        print(">>>", json_str)
        print(">>>", result_data)
        return result_data

    def var_conversion(self, before_value):
        """
        变量转换参数
        :param before_value:
        :return:
        """
        if isinstance(before_value, int):
            return before_value

        json_str = json.dumps(before_value, ensure_ascii=False)
        var_name_list = re.findall('\\$\\{([^}]*)', json_str)  # 找出参数中带 ${} 的字符串
        print(var_name_list)

        if not var_name_list:
            return before_value

        sql = f"""
        select id, var_name, var_value, var_type, is_active 
        from exile_test_variable 
        where {f"var_name in {tuple(var_name_list)}" if len(var_name_list) > 1 else f"var_name='{var_name_list[-1]}'"} 
        and is_deleted=0;
        """
        query_result = project_db.select(sql=sql)

        d = {}
        for obj in query_result:  # 生成: {"var_name":"var_value"}
            var_id = obj.get('id')
            var_name = obj.get('var_name')
            var_value = obj.get('var_value')
            var_type = obj.get('var_type')
            is_active = obj.get('is_active')
            print('===var_type===', var_type)
            print('===var_name===', var_name)
            if str(var_type) in var_func_dict.keys():  # 函数
                if var_id not in self.var_conversion_active_list:
                    new_val = var_func_dict.get(str(var_type))()  # 首次触函数
                    d[var_name] = new_val
                    self.current_var_value = new_val
                    self.var_conversion_active_list.append(var_id)
                else:
                    if is_active == 1:
                        new_val = var_func_dict.get(str(var_type))()
                        d[var_name] = new_val
                    else:
                        d[var_name] = self.current_var_value
            else:
                if var_type in (1, 2):
                    d[var_name] = json.loads(var_value)
                else:
                    d[var_name] = var_value
        print(d)
        return self.var_conversion_main(json_str=json_str, d=d)

    def execute_resp_ass(self, ass_json):
        """
        执行Resp断言
        resp_ass_list demo
            [
                {
                    "assert_key": "code",
                    "expect_val": "200",
                    "expect_val_type": "1",
                    "response_source": "response_body"
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                },
                {
                    "assert_key": "token",
                    "expect_val": "12345678",
                    "expect_val_type": "1",
                    "response_source": "response_headers"
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                }
            ]
        """

        ass_json = self.var_conversion(ass_json)
        print('=== 转换后的resp_ass ===')
        print(ass_json)
        response_ass_result = AssertResponseMain(
            sio=self.sio,
            resp_json=self.resp_json,
            resp_headers=self.resp_headers,
            assert_description=self.current_assert_description,
            **ass_json
        ).main()

        if response_ass_result:
            self.test_result.resp_ass_success += 1
        else:
            self.test_result.resp_ass_fail += 1
            self.current_case_resp_ass_error += 1
            self.full_pass = False
            self.current_logs_error_switch = True
            self.logs_error_switch = True
            self.execute_status = False

    def execute_field_ass(self, ass_json):
        """
        执行Field断言
        """

        ass_json = self.var_conversion(ass_json)
        print('=== 转换后的field_ass ===')
        print(ass_json)
        field_ass_result = AssertFieldMain(
            sio=self.sio,
            assert_description=self.current_assert_description,
            **ass_json
        ).main()

        self.test_result.field_ass_success += field_ass_result.get('success')
        self.test_result.field_ass_fail += field_ass_result.get('fail')

        if self.test_result.field_ass_fail != 0:
            self.full_pass = False
            self.current_logs_error_switch = True
            self.logs_error_switch = True
            self.execute_status = False

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
        :param case_data_info: 参数转换后的组装的参数对象
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
        self.sio.log(f'=== method: {method} ===')

        if method == 'get':
            if "?" in self.request_url:
                self.request_url = self.request_url.split("?")[0]

        url = self.base_url + self.request_url if self.use_base_url else self.request_base_url + self.request_url

        before_send = {
            "url": url,
            "headers": request_headers,
        }
        req_json_data = req_type_dict.get(request_body_type)

        if method == 'get':
            before_send['params'] = request_params
            __key = "params"
        else:
            before_send.update(req_json_data)
            if "json" in before_send:
                __key = "json"
            else:
                __key = "data"
                for k, v in before_send.get(__key).items():
                    if not isinstance(v, str):
                        before_send.get(__key)[k] = str(v)

        send = self.var_conversion(before_send)
        print(send)

        if self.is_safe_scan:
            send['proxies'] = self.proxies

        self.sio.log('=== send ===')
        print(json.dumps(send, ensure_ascii=False))
        resp = self.current_request(method=method, timeout=(50, 60), **send)
        self.resp_json = resp.json()
        self.resp_headers = resp.headers

    def resp_check_ass_execute(self, case_resp_ass_info):
        """
        检查 resp 断言规则并执行断言
        :param case_resp_ass_info: resp检验规则对象
        :return:
        """

        if not case_resp_ass_info:
            self.sio.log('=== 断言规则为空 ===')
            return False

        for resp_ass in case_resp_ass_info:  # 遍历断言规则逐一校验
            self.current_assert_description = resp_ass.get('assert_description')
            ass_json_list = resp_ass.get('ass_json')

            list(map(self.execute_resp_ass, ass_json_list))

    def field_check_ass_execute(self, case_field_ass_info):
        """
        检查 field 断言规则并执行断言
        :return:
        """
        if self.current_case_resp_ass_error == 0:  # 所有resp断言规则通过
            self.update_var()  # 更新变量

            for index, field_ass_obj in enumerate(case_field_ass_info, 1):
                self.current_assert_description = field_ass_obj.get('assert_description')
                ass_json_list = field_ass_obj.get('ass_json')

                list(map(self.execute_field_ass, ass_json_list))
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

            sql = f"""UPDATE exile_test_variable SET var_value='{new_var}' WHERE id='{id}';"""
            print(sql)
            # self.sio.log(f'=== update sql === 【 {sql} 】', status='success')
            project_db.update(sql)

            sql2 = """INSERT INTO exile_test_variable_history ( `create_timestamp`, `is_deleted`, `var_id`, `update_type`, `creator`, `creator_id`, `before_var`, `after_var`) VALUES ('{}',  '0',  '{}', '执行用例更新', '{}', '{}', '{}', '{}');""".format(
                int(self.start_time), id, self.execute_username, self.execute_user_id, old_var, new_var
            )
            print(sql2)
            # self.sio.log(f'=== update history sql === 【 {sql2} 】', status='success')
            project_db.insert(sql2)

    def save_logs(self, redis_key, report_url, file_name):
        """

        :param redis_key: 日志key
        :param report_url: 报告地址
        :param file_name: 文件名称
        :return:
        """

        sql = """INSERT INTO exile_test_execute_logs (`is_deleted`, `create_time`, `create_timestamp`,  `execute_id`, `execute_name`, `execute_type`, `redis_key`, `report_url`, `execute_status`, `creator`, `creator_id`, `trigger_type`, `file_name`) VALUES (0,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');""".format(
            self.create_time,
            int(self.start_time),
            self.execute_id,
            self.execute_name,
            self.execute_type,
            redis_key,
            report_url,
            int(self.execute_status),
            self.execute_username,
            self.execute_user_id,
            self.trigger_type,
            file_name
        )
        project_db.insert(sql)
        logger.success('=== save_logs ok ===')

    def gen_logs(self):
        """组装日志并保存"""

        case_summary = self.test_result.get_test_result()
        self.end_time = str(datetime.datetime.now()).split(".")[0]
        self.total_time = Decimal(time.time() - self.start_time).quantize(Decimal('0.00'))

        self.save_key = "test_log_{}_{}".format(str(int(time.time())), shortuuid.uuid())
        return_case_result = {
            "uuid": self.save_key,
            "execute_user_id": self.execute_user_id,
            "execute_username": self.execute_username,
            "execute_type": self.execute_type,
            "execute_name": self.execute_name,
            "case_result_list": self.case_result_list,
            "result_summary": case_summary,
            "create_time": self.create_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": str(self.total_time)
        }
        R.set(self.save_key, json.dumps(return_case_result))
        current_save_dict = GlobalsDict.redis_first_logs_dict(execute_id=self.execute_id)
        save_obj_first = current_save_dict.get(self.execute_type, "未知执行类型")
        R.set(save_obj_first, json.dumps(return_case_result))
        logger.success('=== save redis ok ===')

        try:
            MainTest.update_case_total_execution(self.id_after_execution)
        except BaseException as e:
            print(f"更新执行次数失败:{str(e)}")
            print(f"id_after_execution:{self.id_after_execution}")

        logger.success('=== update case total ok ===')

    def only_execute(self):
        """
        执行一个用例 -> list[obj] 如: [{}]
        执行一批用例,一个用例场景 -> list[obj,obj,obj...] 如: [{},{},{}...]
        :return:
        """
        print('=== only_execute ===')

        for case_index, case in enumerate(self.case_generator, 1):
            self.sio.log(f'=== start case: {case_index} ===')

            self.reset_current_data()

            case_info = case.get('case_info', {})
            bind_info = case.get('bind_info', [])
            case_expand = case.get('case_expand', {})
            case_sleep = case_expand.get('sleep')

            self.case_id = case_info.get('id')
            self.case_name = case_info.get('case_name')
            self.creator = case_info.get('creator')
            self.creator_id = case_info.get('creator_id')

            self.sio.log(f'=== case_id: {self.case_id} ===')
            self.sio.log(f'=== case_name: {self.case_name} ===')

            self.request_base_url = case_info.get('request_base_url')
            self.request_url = case_info.get('request_url')
            self.request_method = case_info.get('request_method')
            self.update_var_list = []

            self.resp_json = {}
            self.resp_headers = {}

            if not bind_info:
                self.sio.log('=== 未配置请求参数 ===')
                continue

            for index, bind in enumerate(bind_info, 1):

                self.sio.log(f"=== 数据驱动:{index} ===")
                case_data_info = bind.get('case_data_info', {})
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                self.case_data_before(case_data_info)

                try:
                    self.assemble_data_send(case_data_info=case_data_info)  # 转换变量并发起请求
                    self.test_result.req_success += 1
                    self.id_after_execution.append(self.case_id)
                except BaseException as e:
                    self.sio.log(f"=== 请求失败:{str(e)} ===", status="error")
                    self.test_result.req_error += 1
                    self.full_pass = False
                    self.logs_error_switch = True
                    self.execute_status = False
                    self.sio.log("=== 跳过断言 ===")
                    continue

                self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

                if isinstance(case_sleep, int) and abs(case_sleep) != 0:
                    print('等待前:', time.time())
                    time.sleep(abs(case_sleep))
                    self.sio.log(f"=== 用例 {self.case_name} 执行后等待: {case_sleep}s ===")
                    print('等待后:', time.time())

                self.case_data_after(case_data_info)

                if not self.data_driven:
                    self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                    break

            self.set_case_count()

            self.sio.log(f'=== end case: {case_index} ===\n')

            add_case = {
                "report_tab": 1,
                "case_id": self.case_id,
                "case_name": f"{self.case_name}（ID:{self.creator_id}-创建人:{self.creator}）",
                "case_log": self.sio.get_stringio().split('\n'),
                "error": self.logs_error_switch
            }

            self.case_result_list.append(add_case)

        if not self.is_execute_all:
            self.gen_logs()

    def many_execute(self):
        """
        执行多个组用例
        list[list[obj,obj,obj], list[obj,obj,obj], list[obj,obj,obj]] 如: [[{},{},{}...], [{},{},{}...], [{},{},{}...] ...]
        :return:
        """
        print('=== many_execute ===')

        if self.is_execute_all:
            new_scenario_generator = self.scenario_generator
        else:
            new_scenario_generator = self.case_generator

        for group_index, group in enumerate(new_scenario_generator, 1):
            scenario_id = group.get('scenario_id')
            scenario_title = group.get('scenario_title')
            case_list = group.get('case_list')
            self.sio.log(f'=== start {scenario_id}: scenario: {scenario_title} ===')

            self.reset_current_data()

            scenario_log = []

            for case_index, case in enumerate(case_list, 1):
                self.sio.log(f'=== start case: {case_index} ===')

                self.logs_error_switch = False

                case_info = case.get('case_info', {})
                bind_info = case.get('bind_info', [])
                case_expand = case.get('case_expand', {})
                case_sleep = case_expand.get('sleep')

                self.case_id = case_info.get('id')
                self.case_name = case_info.get('case_name')
                self.creator = case_info.get('creator')
                self.creator_id = case_info.get('creator_id')

                self.sio.log(f'=== case_id: {self.case_id} ===')
                self.sio.log(f'=== case_name: {self.case_name} ===')

                self.request_base_url = case_info.get('request_base_url')
                self.request_url = case_info.get('request_url')
                self.request_method = case_info.get('request_method')
                self.update_var_list = []

                self.resp_json = {}
                self.resp_headers = {}

                if not bind_info:
                    self.sio.log('=== 未配置请求参数 ===')
                    continue

                for index, bind in enumerate(bind_info, 1):
                    self.sio.log(f"=== 数据驱动:{index} ===")
                    case_data_info = bind.get('case_data_info', {})
                    case_resp_ass_info = bind.get('case_resp_ass_info', [])
                    case_field_ass_info = bind.get('case_field_ass_info', [])

                    self.case_data_before(case_data_info)

                    try:
                        self.assemble_data_send(case_data_info=case_data_info)
                        self.test_result.req_success += 1
                        self.id_after_execution.append(self.case_id)
                    except BaseException as e:
                        self.sio.log(f"=== 请求失败:{str(e)} ===", status="error")
                        self.test_result.req_error += 1
                        self.full_pass = False
                        self.current_logs_error_switch = True
                        self.logs_error_switch = True
                        self.execute_status = False
                        self.sio.log("=== 跳过断言 ===")
                        continue

                    self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                    self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

                    if isinstance(case_sleep, int) and abs(case_sleep) != 0:
                        print('等待前:', time.time())
                        time.sleep(abs(case_sleep))
                        self.sio.log(f"=== 用例 {self.case_name} 执行后等待: {case_sleep}s ===")
                        print('等待后:', time.time())

                    self.case_data_after(case_data_info)

                    if not self.data_driven:
                        self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                        break

                add_case = {
                    "case_id": self.case_id,
                    "case_name": f"{self.case_name}（ID:{self.creator_id}-创建人:{self.creator}）",
                    "case_log": self.sio.get_stringio().split('\n'),
                    "error": self.logs_error_switch
                }

                scenario_log.append(add_case)

                self.sio.log(f'=== end {scenario_id}: scenario: {scenario_title} case: {case_index}===\n')

            add_group = {
                "report_tab": 2,
                "scenario_id": scenario_id,
                "scenario_title": scenario_title,
                "scenario_log": scenario_log,
                "error": self.current_logs_error_switch
            }
            self.case_result_list.append(add_group)
            self.set_case_count()

        if not self.is_execute_all:
            self.gen_logs()

    def all_execute(self):
        """执行用例与场景"""

        print('=== all_execute -> only_execute ===')
        self.only_execute()

        print('=== all_execute -> many_execute ===')
        self.many_execute()

        print('=== all_execute -> gen_logs ===')
        self.gen_logs()

    def save_test_repost(self, report_str):
        """
        生成 html 测试报告
        :param report_str: html字符
        :return:
        """

        self.report_name = f"Test_Report_{time.strftime('%Y-%m-%d_%H_%M_%S')}_{self.execute_name}.html"

        # self.path = f"{os.getcwd().split('ExileTestPlatformServer')[0]}ExileTestPlatformServer/app/static/report/{self.report_name}"

        with open(self.path + self.report_name, "w", encoding="utf-8") as f:
            f.writelines(report_str)
            # f.write(report_str)
            # f.flush()
            # os.fsync(report_str)

    def gen_report_url(self):
        """
        生成测试报告链接
        :return:
        """
        query = project_db.select(
            'SELECT server_url, safe_scan_report_path, safe_scan_report_name FROM exile_platform_conf WHERE weights = (SELECT max(weights) FROM exile_platform_conf);',
            only=True)
        def_url = 'http://0.0.0.0:5000'
        self.report_url = f"{query.get('server_url', def_url)}/{self.report_name}"

    def main(self):
        """main"""

        self.safe_scan()

        getattr(self, self.func_name)()

        get_data = R.get(self.save_key)  # 日志结果集
        test_repost = RepostTemplate(data=get_data).generate_html_report()  # 测试报告渲染
        test_repost_sizeof = sys.getsizeof(test_repost)

        try:
            self.save_test_repost(report_str=test_repost)  # 创建html测试报告
        except BaseException as e:
            t = datetime.datetime.now()
            error_info = {
                "time": t,
                "test_repost": test_repost_sizeof,
                "test_repost_kb": f"{int(test_repost_sizeof / 1024)}KB",
                "traceback": traceback.print_exc(),
                "e": str(e)
            }
            R.set(f'gen_repost_error_{t}', json.dumps(error_info))

        self.gen_report_url()  # 生成测试报告链接
        self.save_logs(redis_key=self.save_key, report_url=self.report_url, file_name=self.report_name)

        if self.is_dd_push:
            try:
                mt = f"#### 测试报告:{self.execute_name}  \n  > 测试人员:{self.execute_username}  \n  > 开始时间:{self.create_time}  \n  > 结束时间:{self.end_time}  \n  > 合计耗时:{self.total_time}s  \n  > 用例总数:{self.test_result.all_test_count}  \n  > 成功数:{self.test_result.pass_count}  \n  > 失败数:{self.test_result.fail_count}  \n  > 通过率:{self.test_result.pass_rate}  \n "
                print(mt)
                print(self.ding_talk_url)
                MessagePush.dd_push(
                    ding_talk_url=self.ding_talk_url,
                    report_url=self.report_url,
                    is_safe_scan=self.is_safe_scan,
                    safe_scan_report_path=self.safe_scan_report_url,
                    markdown_text=mt
                )
            except BaseException as e:
                print(str(e))
                t = datetime.datetime.now()
                error_info = {
                    "time": t,
                    "traceback": traceback.print_exc(),
                    "e": str(e)
                }
                R.set(f'gen_dd_push_error_{t}', json.dumps(error_info))

        if self.is_send_mail:
            SendEmail(to_list=self.mail_list, ac_list=self.mail_list).send_attach(
                report_title=self.execute_name,
                html_file_path=self.path + self.report_name,
                mail_content="详情查看附件"
            )

    def __str__(self):
        return '\n'.join([f"{k}:{v}" for k, v in self.__dict__.items()])
