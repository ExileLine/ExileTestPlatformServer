# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:19 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CaseDrivenResult.py
# @Software: PyCharm

import re
import json
import requests

from loguru import logger

from common.libs.db import project_db
from common.libs.public_func import check_keys
from common.libs.public_func import json_format
from common.libs.assert_related import AssertMain


class CaseDrivenResult:
    """
    main
    1.组装用例:
        CaseDrivenResult.__init__ √

    2.转换参数:
        CaseDrivenResult.var_conversion √

    3.发出请求:
        CaseDrivenResult.current_request √

    4.resp断言前置检查:
        AssertMain.assert_resp_main √

    5.resp断言:
        AssertMain.assert_resp_main √

    6.更新变量:
        CaseDrivenResult.update_var √

    7.field断言前置检查:

    8.field断言:

    7.日志记录:

    8.生成报告:

    """

    def __init__(self, case):
        self.case = case
        self.case_info = self.case.get('case_info', {})
        self.bind_info = self.case.get('bind_info', [])

        self.case_name = self.case_info.get('case_name')
        self.request_url = self.case_info.get('request_url')
        self.request_method = self.case_info.get('request_method')
        self.update_var_list = []

        self.resp_json = {}
        self.resp_headers = {}

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

    @staticmethod
    def show_log(url, headers, req_json, resp_headers, resp_json):
        """测试用例日志打印"""
        logger.info('test url\n{}'.format(url))
        json_format(headers, msg='test headers')
        json_format(req_json, msg='test req_json')
        json_format(resp_headers, msg='test resp_headers')
        json_format(resp_json, msg='test resp_json')

    @staticmethod
    def var_conversion(before_var):
        """变量转换参数"""

        before_var_init = before_var
        if isinstance(before_var_init, (list, dict)):
            before_var = json.dumps(before_var, ensure_ascii=False)

        result_list = re.findall('\\$\\{([^}]*)', before_var)

        if result_list:
            err_var_list = []
            current_dict = {}
            for res in result_list:
                sql = """select var_value from exilic_test_variable where var_name='{}';""".format(res)
                query_result = project_db.select(sql=sql, only=True)
                if query_result:
                    current_dict[res] = json.loads(query_result.get('var_value'))
                else:
                    err_var_list.append(res)
            if current_dict:
                current_str = before_var
                for k, v in current_dict.items():
                    old_var = "${%s}" % (k)
                    new_var = v
                    current_str = current_str.replace(old_var, new_var)
                if isinstance(before_var_init, (list, dict)):
                    current_str = json.loads(current_str)
                # print(current_str)
                return current_str
            else:
                logger.info('===未找到变量:{}对应的参数==='.format(err_var_list))
                return before_var_init
        else:
            return before_var_init

    @staticmethod
    def check_ass_keys(assert_list, check_type):
        """
        检查断言对象参数类型是否正确
        assert_list: ->list 规则列表
        check_type: ->int 1-响应断言规则;2-数据库校验规则
        """
        keys_dict = {
            "1": ["assert_key", "expect_val", "expect_val_type", "is_expression", "python_val_exp", "rule"],
            "2": ""  # TODO 数据库校验规则

        }
        if not isinstance(assert_list, list) or not assert_list:
            logger.info("assert_list:类型错误{}".format(assert_list))
            return False

        if check_type not in [1, 2]:
            logger.info("check_type:类型错误{}".format(check_type))
            return False

        for ass in assert_list:
            if not check_keys(ass, *keys_dict.get(str(check_type))):
                logger.info("缺少需要的键值对:{}".format(ass))
                return False
        return True

    @classmethod
    def current_request(cls, method=None, **kwargs):
        """
        构造请求
        :param method: 请求方式
        :param kwargs: 请求体以及扩展参数
        :return:
        """

        if hasattr(requests, method):
            response = getattr(requests, method)(**kwargs, verify=False)
            cls.current_resp_json = response.json()
            cls.current_resp_headers = response.headers
            cls.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=cls.current_resp_json,
                resp_headers=cls.current_resp_headers
            )
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            cls.current_resp_json = response
            cls.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=cls.current_resp_json,
                resp_headers={}
            )
        return response

    def update_var(self):
        """更新变量"""
        if self.update_var_list:
            for up in self.update_var_list:
                current_list = [item for item in up.items()][0]
                id = current_list[0]
                var_value = current_list[1]
                sql = """UPDATE exilic_test_variable SET var_value='{}' WHERE id='{}';""".format(
                    json.dumps(var_value, ensure_ascii=False), id)
                logger.info('=== update sql ===\n{}'.format(sql))
                project_db.update_data(sql)
        else:
            logger.info('=== 更新变量列表为空不需要更新变量===')

    def go_test(self):
        """调试"""
        print(self.resp_ass_count)
        print(self.resp_ass_success)
        print(self.resp_ass_fail)
        print(self.update_var_list)

    def main(self):
        """main"""

        if self.bind_info:

            for bind in self.bind_info:
                case_data_info = bind.get('case_data_info', {})
                self.update_var_list = case_data_info.get('update_var_list')
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                req_type_dict = {
                    "1": {"data": case_data_info.get('request_body')},
                    "2": {"json": case_data_info.get('request_body')},
                    "3": {"data": case_data_info.get('request_body')}
                }

                send = {
                    "url": self.request_url,  # TODO 有 base url 拼接
                    "headers": case_data_info.get('request_headers'),

                }

                go = req_type_dict.get(str(case_data_info.get('request_body_type')))
                send.update(go)

                send = self.var_conversion(send)

                resp = self.current_request(method=self.request_method.lower(), **send)
                self.resp_json = resp.json()
                self.resp_headers = resp.headers
                json_format(self.resp_json, '用例:{} -> resp_json'.format(self.case_name))
                json_format(self.resp_headers, '用例:{} -> resp_headers'.format(self.case_name))

                if case_resp_ass_info:
                    for resp_ass in case_resp_ass_info:  # 遍历断言规则逐一校验
                        resp_ass_list = resp_ass.get('ass_json')
                        assert_description = resp_ass.get('assert_description')
                        # print(resp_ass_list)
                        if self.check_ass_keys(assert_list=resp_ass_list, check_type=1):
                            self.resp_ass_count = len(resp_ass_list)
                            for resp_ass_dict in resp_ass_list:
                                # print(resp_ass_dict)
                                new_ass = AssertMain(
                                    resp_json=self.resp_json,
                                    resp_headers=self.resp_headers,
                                    assert_description=assert_description,
                                    **resp_ass_dict
                                )
                                resp_ass_result = new_ass.assert_resp_main()
                                # print(resp_ass_result)
                                if resp_ass_result[0]:
                                    self.resp_ass_success += 1
                                else:
                                    self.resp_ass_fail += 1

                    if self.resp_ass_fail == 0:  # 所有断言规则通过,更新变量
                        self.update_var()
                    else:
                        logger.info('=== 断言规则没有100%通过,不更新变量以及数据库校验 ===')
        else:
            logger.info('=== 未配置请求参数 ===')


if __name__ == '__main__':
    demo = {
        "bind_info": [
            {
                "case_data_info": {
                    "create_time": "2021-09-01 20:34:39",
                    "create_timestamp": 1630499057,
                    "creator": "调试",
                    "creator_id": 1,
                    "data_name": "数据99999",
                    "id": 12,
                    "is_deleted": 0,
                    "modifier": None,
                    "modifier_id": None,
                    "remark": None,
                    "request_body": {"key": "${user_id}"},
                    "request_body_type": 1,
                    "request_headers": {"key": "${user_id}"},
                    "request_params": {"key": "${user_id}"},
                    "status": 1,
                    "update_time": "2021-09-01 20:34:40",
                    "update_timestamp": None,
                    "var_list": [
                        "user_id",
                        "username"
                    ],
                    "update_var_list": [
                        {"2": "999"},
                        {"3": "更新123"}
                    ],
                },
                "case_field_ass_info": [],
                "case_resp_ass_info": [
                    {
                        "ass_json": [
                            {"rule": "=", "assert_key": "code", "expect_val": 200, "is_expression": 0,
                             "python_val_exp": "okc.get('a').get('b').get('c')[0]", "expect_val_type": "1"},
                            {"rule": "=", "assert_key": "message", "expect_val": "index", "is_expression": 0,
                             "python_val_exp": "okc.get('a').get('b').get('c')[0]", "expect_val_type": "2"}
                        ],
                        "assert_description": "Resp通用断言",
                        "create_time": "2021-09-01 20:30:04",
                        "create_timestamp": 1630499057,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 10,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-01 20:30:05",
                        "update_timestamp": None
                    }
                ]
            }
        ],
        "case_info": {
            "case_name": "测试indexApi",
            "create_time": "2021-09-01 20:27:32",
            "create_timestamp": 1630499057,
            "creator": "调试",
            "creator_id": 1,
            "id": 14,
            "is_deleted": 0,
            "modifier": None,
            "modifier_id": None,
            "remark": "remark",
            "request_method": "GET",
            "request_url": "http://127.0.0.1:7272/api",
            "status": 1,
            "update_time": "2021-09-01 20:27:32",
            "update_timestamp": None
        }
    }
    demo2 = {
        "bind_info": [
            {
                "case_data_info": {
                    "create_time": "2021-09-01 20:34:39",
                    "create_timestamp": 1630499057,
                    "creator": "调试",
                    "creator_id": 1,
                    "data_name": "数据99999",
                    "id": 12,
                    "is_deleted": 0,
                    "modifier": None,
                    "modifier_id": None,
                    "remark": None,
                    "request_body": {"key": "${aaa}"},
                    "request_body_type": 1,
                    "request_headers": {},
                    "request_params": {},
                    "status": 1,
                    "update_time": "2021-09-01 20:34:40",
                    "update_timestamp": None,
                    "update_var_list": [
                        {
                            "3": "更新"
                        }
                    ],
                    "var_list": [
                        "user_id",
                        "username"
                    ]
                },
                "case_field_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_list": [
                                    {
                                        "assert_key": "id",
                                        "expect_val": "1",
                                        "expect_val_type": "1",
                                        "rule": "="
                                    }
                                ],
                                "db_name": "ExilicTestPlatform",
                                "query": [
                                    {
                                        "field_key": "1",
                                        "field_name": "id",
                                        "is_sql": "1",
                                        "query_rule": "=",
                                        "sql": "SELECT * FROM exilic_test_case WHERE id=1;"
                                    },
                                    {
                                        "field_key": "测试用例B1",
                                        "field_name": "case_name",
                                        "is_sql": "1",
                                        "query_rule": "=",
                                        "sql": "SELECT * FROM exilic_test_case WHERE id=1;"
                                    }
                                ],
                                "table_name": "exilic_test_case"
                            }
                        ],
                        "assert_description": "通用字段校验",
                        "create_time": "2021-09-03 14:25:53",
                        "create_timestamp": 1630649234,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 9,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-03 14:25:53",
                        "update_timestamp": None
                    }
                ],
                "case_resp_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "expect_val": "200",
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            }
                        ],
                        "assert_description": "Resp通用断言",
                        "create_time": "2021-09-01 20:30:04",
                        "create_timestamp": 1630499057,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 10,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-01 20:30:05",
                        "update_timestamp": None
                    }
                ]
            }
        ],
        "case_info": {
            "case_name": "测试indexApi",
            "create_time": "2021-09-01 20:27:32",
            "create_timestamp": 1630499057,
            "creator": "调试",
            "creator_id": 1,
            "id": 14,
            "is_deleted": 0,
            "modifier": None,
            "modifier_id": None,
            "remark": "remark",
            "request_method": "GET",
            "request_url": "http://127.0.0.1:7272/api",
            "status": 1,
            "update_time": "2021-09-01 20:27:32",
            "update_timestamp": None
        }
    }
    cdr = CaseDrivenResult(case=demo2)
    cdr.main()
    # cdr.go_test()
