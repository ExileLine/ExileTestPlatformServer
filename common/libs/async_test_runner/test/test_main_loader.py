# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_case_loader.py
# @Software: PyCharm

import asyncio

from common.libs.async_test_runner import AsyncCaseRunner, case_list, scenario_list

test_obj = {
    "project_id": 30,
    "execute_id": 8646,
    "execute_name": "执行用例8646:[登录成功okc2]",
    "execute_type": "case",
    "execute_label": "only",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
    "is_execute_all": False,
    "case_list": case_list,
    "scenario_list": scenario_list,
    "execute_dict": {},
    "is_dd_push": False,
    "dd_push_id": None,
    "ding_talk_url": "",
    "is_send_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 3,
    "is_safe_scan": False,
    "safe_scan_proxies_url": "",
    "call_safe_scan_data": {},
    "safe_scan_report_url": ""
}

test_obj2 = {
    "project_id": 30,
    "execute_id": 8646,
    "execute_name": "测试重构用例相关",
    "execute_type": "case",
    "execute_label": "execute_label",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": False,
    "case_list": [
        {
            "case_info": {
                "id": 8646,
                "request_method": "POST",
                "modifier": "admin",
                "create_timestamp": 1660557652,
                "request_base_url": "http://0.0.0.0:7878",
                "modifier_id": 1,
                "update_time": "2022-09-22 16:16:46",
                "request_url": "${重构url}",
                "remark": "123",
                "update_timestamp": 1663834584,
                "case_status": "active",
                "create_time": "2022-08-15 22:33:28",
                "is_deleted": 0,
                "is_pass": 0,
                "status": 1,
                "total_execution": 0,
                "case_name": "测试重构用例相关",
                "creator": "admin",
                "creator_id": 1,
                "is_public": True,
                "is_shared": True
            },
            "bind_info": [
                {
                    "data_info": {
                        "id": 19345,
                        "status": 1,
                        "request_body_hash": "{\n  \"a\":\"123\"\n}",
                        "creator": "admin",
                        "data_name": "5.0新的参数",
                        "request_body_type": "json",
                        "request_params": {},
                        "use_var_list": None,
                        "creator_id": 1,
                        "create_time": "2022-08-16 20:25:50",
                        "request_params_hash": [],
                        "update_var_list": [
                            {
                                "id": 28,
                                "remark": "123",
                                "status": 1,
                                "creator": "user_00001",
                                "modifier": "admin",
                                "var_name": "okc",
                                "var_type": 6,
                                "is_public": 1,
                                "last_func": None,
                                "var_value": None,
                                "creator_id": 1,
                                "expression": "okc.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                "is_deleted": 0,
                                "var_source": "response_body",
                                "create_time": "2021-12-11 17:13:07",
                                "modifier_id": 1,
                                "update_time": "2021-12-17 16:49:48",
                                "var_get_key": "123",
                                "is_expression": 1,
                                "last_func_var": None,
                                "create_timestamp": 1639213949,
                                "update_timestamp": 1639730968
                            }
                        ],
                        "modifier": "admin",
                        "create_timestamp": 1660652718,
                        "request_headers": {
                            "token": "123"
                        },
                        "data_before": [],
                        "modifier_id": 1,
                        "update_time": "2022-09-19 14:04:18",
                        "request_headers_hash": [
                            {
                                "cid": 1,
                                "key": "token",
                                "desc": "",
                                "value": "123",
                                "active": True
                            }
                        ],
                        "data_after": [],
                        "remark": None,
                        "update_timestamp": 1663234923,
                        "request_body": {
                            "a": "123"
                        },
                        "md5": None,
                        "is_deleted": 0,
                        "data_size": 30,
                        "is_public": False,
                        "is_before": False,
                        "is_after": False
                    },
                    "case_resp_ass_info": [
                        {
                            "id": 1,
                            "create_timestamp": 1660190869,
                            "update_timestamp": 1663837753,
                            "status": 1,
                            "assert_description": "调试用例执行专用resp断言",
                            "assertion_type": "response",
                            "creator_id": 1,
                            "modifier_id": 1,
                            "remark": "调试用例执行专用resp断言",
                            "update_time": "2022-09-22 17:12:28",
                            "create_time": "2022-08-11 12:07:55",
                            "is_deleted": 0,
                            "project_id": 30,
                            "ass_json": [
                                {
                                    "rule": "==",
                                    "uuid": "fypU7LmFya7zfcfUtf54uX-1663837947",
                                    "assert_key": "data",
                                    "expect_val": "200",
                                    "is_expression": False,
                                    "python_val_exp": "obj.get('data')",
                                    "expect_val_type": "str",
                                    "response_source": "response_body"
                                },
                                {
                                    "rule": "==",
                                    "uuid": "HTtKYnE5Yoxr8hTqd2Eaty-1663837947",
                                    "assert_key": "data",
                                    "expect_val": "200",
                                    "is_expression": True,
                                    "python_val_exp": "obj.get('data')",
                                    "expect_val_type": "int",
                                    "response_source": "response_body"
                                }
                            ],
                            "creator": "admin",
                            "modifier": "admin",
                            "is_public": False
                        }
                    ],
                    "case_field_ass_info": [
                        {
                            "id": 3,
                            "create_timestamp": 1660191877,
                            "update_timestamp": None,
                            "status": 1,
                            "assert_description": "okclol",
                            "assertion_type": "field",
                            "creator_id": 1,
                            "modifier_id": None,
                            "remark": "",
                            "update_time": "2022-08-11 12:25:11",
                            "create_time": "2022-08-11 12:25:10",
                            "is_deleted": 0,
                            "project_id": 30,
                            "ass_json": [
                                {
                                    "db_id": 12,
                                    "assert_list": [
                                        {
                                            "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1;",
                                            "assert_field_list": [
                                                {
                                                    "rule": "==",
                                                    "assert_key": "id",
                                                    "expect_val": 1,
                                                    "is_expression": 1,
                                                    "python_val_exp": "obj.get(\"id\")",
                                                    "expect_val_type": "1"
                                                },
                                                {
                                                    "rule": "==",
                                                    "assert_key": "case_name",
                                                    "expect_val": "yyx",
                                                    "is_expression": 1,
                                                    "python_val_exp": "obj.get(\"case_name\")",
                                                    "expect_val_type": "2"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "db_id": 9,
                                    "assert_list": [
                                        {
                                            "query": "get 127.0.0.1",
                                            "assert_field_list": [
                                                {
                                                    "rule": "==",
                                                    "assert_key": "username",
                                                    "expect_val": "user_00007",
                                                    "is_expression": 1,
                                                    "python_val_exp": "obj.get('username')",
                                                    "expect_val_type": "2"
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "db_id": 9,
                                    "assert_list": [
                                        {
                                            "query": "get user_00007",
                                            "assert_field_list": [
                                                {
                                                    "rule": "==",
                                                    "assert_key": "7",
                                                    "expect_val": "7",
                                                    "python_val_exp": "",
                                                    "expect_val_type": "2"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "creator": "admin",
                            "modifier": None,
                            "is_public": True
                        }
                    ]
                }
            ]
        }
    ],
    "scenario_list": [],
    "use_dd_push": False,
    "dd_push_id": "",
    "ding_talk_url": "",
    "use_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 5
}
if __name__ == '__main__':
    """单元测试"""

    acr = AsyncCaseRunner(test_obj=test_obj2, is_debug=True)
    asyncio.run(acr.main())
