# -*- coding: utf-8 -*-
# @Time    : 2022/10/29 21:48
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_logs_demo.py
# @Software: PyCharm

case_logs_demo = [
    {
        "case_uuid": "OKC123Ym2FuxgRmj8brEVt",
        "id": 1,
        "case_name": "yy",
        "logs": [],
        "fail": True,  # bool
        "data_dict": {
            "9": {
                "data_id": 9,
                "data_name": "xx",
                "fail": True,  # bool
                "logs": {
                    "request_before": {
                        "description": "参数前置准备",
                        "logs": []
                    },
                    "url": {
                        "description": "请求地址",
                        "logs": []
                    },
                    "request_headers": {
                        "description": "请求头",
                        "type": None,
                        "logs": []
                    },
                    "request_body": {
                        "description": "请求体",
                        "logs": []
                    },
                    "http_code": {
                        "description": "HTTP响应码",
                        "logs": []
                    },
                    "response_headers": {
                        "description": "响应头",
                        "logs": []
                    },
                    "response_body": {
                        "description": "响应体",
                        "type": None,
                        "logs": []
                    },
                    "request_after": {
                        "description": "参数后置准备",
                        "logs": []
                    },
                    "response_assert": {
                        "description": '响应断言',
                        "fail": True,  # bool
                        "logs": [
                            '=== 公式取值结果: 200 ===',
                            '=== 断言:1-123-第一个 ===',
                            "=== 键值:{'code': 200} ===",
                            "function: <class 'int'>",
                            "200:<class 'int'> [==] 200:int",
                            '=== Response 断言通过 ===',
                            '=== 取值结果: 200 ===',
                            '=== 断言:1-123-第一个 ===',
                            "=== 键值:{'code': 200} ===",
                            "function: <class 'int'>",
                            "200:<class 'int'> [==] 200:int",
                            '=== Response 断言通过 ===',
                        ],
                    },
                    "field_assert": {
                        "description": '字段断言',
                        "fail": True,  # bool
                        "logs": ["=== case_resp_ass_info ===\n[{'field_ass': '1'}]\n1-123-第一个"],
                    },
                },
                "logs_summary": ['=== 日志1 ===', '=== 日志2 ===', '=== ... ==='],
            }
        }
    }
]

scenario_logs_demo = [
    {
        "uuid": "DrxW6nYm2FuxgRmj8brEVt",
        "id": 65,
        "scenario_title": "场景1666949754",
        "case_list": [
            {
                "uuid": "2kZGYrkarcb9Aa2SK7R7NU",
                "case_info": {
                    "id": 8646,
                    "is_deleted": 0,
                    "case_name": "测试重构用例相关456",
                    "request_method": "POST",
                    "request_base_url": "http://0.0.0.0:7878",
                    "request_url": "${重构url}",
                    "is_shared": 1,
                    "is_public": 1,
                    "total_execution": 0,
                    "creator": "admin",
                    "creator_id": 1,
                    "create_time": "2022-08-15 22:33:28",
                    "create_timestamp": 1660557652,
                    "modifier": "admin",
                    "modifier_id": 1,
                    "update_time": "2022-09-22 16:16:46",
                    "update_timestamp": 1663834584,
                    "remark": "123"
                },
                "bind_info": [
                    {
                        "data_info": {
                            "id": 19345,
                            "data_name": "5.0新的参数",
                            "request_params": {},
                            "request_headers": {
                                "token": "123"
                            },
                            "request_body": {
                                "a": "123"
                            },
                            "request_body_type": "json",
                            "var_list": "",
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
                                    "expression": "okc.a",
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
                                },
                                {
                                    "id": 102,
                                    "remark": None,
                                    "status": 1,
                                    "creator": "admin",
                                    "modifier": None,
                                    "var_args": {},
                                    "var_name": "zxc",
                                    "var_type": "int",
                                    "is_active": False,
                                    "is_public": False,
                                    "is_source": False,
                                    "last_func": None,
                                    "var_value": "1",
                                    "creator_id": 1,
                                    "expression": None,
                                    "is_deleted": 0,
                                    "project_id": 30,
                                    "var_source": "response_body",
                                    "create_time": "2022-09-26 17:10:26",
                                    "modifier_id": None,
                                    "update_time": "2022-09-26 17:10:26",
                                    "var_get_key": "123",
                                    "is_expression": True,
                                    "last_func_var": None,
                                    "var_init_value": "1",
                                    "create_timestamp": 1664179672,
                                    "update_timestamp": None
                                }
                            ],
                            "is_deleted": 0,
                            "is_public": 0,
                            "creator": "admin",
                            "creator_id": 1,
                            "create_time": "2022-08-16 20:25:50",
                            "create_timestamp": 1660652718,
                            "modifier": "admin",
                            "modifier_id": 1,
                            "update_time": "2022-09-26 17:38:58",
                            "update_timestamp": 1664185124,
                            "remark": None,
                            "is_before": 0,
                            "data_before": [],
                            "is_after": 0,
                            "data_after": []
                        },
                        "case_resp_ass_info": [
                            {
                                "id": 1,
                                "create_timestamp": 1660190869,
                                "update_time": "2022-09-23 10:46:45",
                                "is_deleted": 0,
                                "project_id": 30,
                                "ass_json": [
                                    {
                                        "rule": "==",
                                        "uuid": "TpDMbUm9dEMXZw2wdNvSVF-1663901205",
                                        "assert_key": "code",
                                        "expect_val": "200",
                                        "is_expression": False,
                                        "python_val_exp": "obj.get('code')",
                                        "expect_val_type": "str",
                                        "response_source": "response_body"
                                    },
                                    {
                                        "rule": "==",
                                        "uuid": "YRhwmQA9MbdYG3YQnxv3CC-1663901205",
                                        "assert_key": "code",
                                        "expect_val": "400",
                                        "is_expression": True,
                                        "python_val_exp": "obj.get('code')",
                                        "expect_val_type": "int",
                                        "response_source": "response_body"
                                    }
                                ],
                                "creator": "admin",
                                "modifier": "admin",
                                "remark": "调试用例执行专用resp断言",
                                "create_time": "2022-08-11 12:07:55",
                                "update_timestamp": 1663901103,
                                "status": 1,
                                "assert_description": "调试用例执行专用resp断言",
                                "assertion_type": "response",
                                "creator_id": 1,
                                "modifier_id": 1,
                                "is_public": False
                            }
                        ],
                        "case_field_ass_info": [
                            {
                                "id": 3,
                                "create_timestamp": 1660191877,
                                "update_time": "2022-08-11 12:25:11",
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
                                "remark": "",
                                "create_time": "2022-08-11 12:25:10",
                                "update_timestamp": None,
                                "status": 1,
                                "assert_description": "okclol",
                                "assertion_type": "field",
                                "creator_id": 1,
                                "modifier_id": None,
                                "is_public": True
                            }
                        ]
                    }
                ],
                "case_expand": {
                    "index": 1,
                    "sleep": 10,
                    "case_id": 8646
                }
            }
        ]
    }
]
