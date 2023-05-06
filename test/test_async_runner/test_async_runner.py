# -*- coding: utf-8 -*-
# @Time    : 2022/10/29 17:13
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_async_runner.py
# @Software: PyCharm

import json
import asyncio

from common.libs.async_test_runner import AsyncLogs, AsyncCaseRunner

case_list = [
    {
        "case_uuid": "OKC123Ym2FuxgRmj8brEVt",
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
            "case_name": "测试重构用例相关123",
            "creator": "admin",
            "creator_id": 1,
            "is_public": True,
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
                                "db_id": 8899,
                                "assert_list": []
                            },  # 测试-数据库不存在或禁用
                            {
                                "db_id": 4,
                                "assert_list": []
                            },  # 测试-数据库数据类型暂不支持
                            {
                                "db_id": 18,
                                "assert_list": []
                            },  # 测试-数据库连接失败
                            {
                                "db_id": 12,
                                "assert_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "id",
                                                "expect_val": 1,
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"id\")",
                                                "expect_val_type": "int"
                                            },
                                            {
                                                "rule": "==",
                                                "assert_key": "case_name",
                                                "expect_val": "yyx",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试mysql-有查询结果
                            {
                                "db_id": 12,
                                "assert_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=0;",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "id",
                                                "expect_val": 1,
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"id\")",
                                                "expect_val_type": "int"
                                            },
                                            {
                                                "rule": "==",
                                                "assert_key": "case_name",
                                                "expect_val": "yyx",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试mysql-无查询结果
                            {
                                "db_id": 9,
                                "assert_list": [
                                    {
                                        "query": "get 127.0.0.1111111",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "username",
                                                "expect_val": "user_00007",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get('username')",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试redis-无查询结果
                            {
                                "db_id": 9,
                                "assert_list": [
                                    {
                                        "query": "get 127.0.0.1",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "username",
                                                "expect_val": "yyx_999",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get('username')",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试redis-查询结果为dict以及用表达式取值
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
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            }  # 测试redis-查询结果为str
                        ],
                        "creator": "admin",
                        "modifier": None,
                        "is_public": True
                    }
                ]
            }
        ]
    },
    {
        "case_uuid": "YYX123Ym2FuxgRmj8br999",
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
            "case_name": "测试重构用例相关123",
            "creator": "admin",
            "creator_id": 1,
            "is_public": True,
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
                                        "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "id",
                                                "expect_val": 1,
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"id\")",
                                                "expect_val_type": "int"
                                            },
                                            {
                                                "rule": "==",
                                                "assert_key": "case_name",
                                                "expect_val": "yyx",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试mysql-有查询结果
                            {
                                "db_id": 9,
                                "assert_list": [
                                    {
                                        "query": "get 127.0.0.1",
                                        "assert_field_list": [
                                            {
                                                "rule": "==",
                                                "assert_key": "username",
                                                "expect_val": "yyx_999",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get('username')",
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            },  # 测试redis-查询结果为dict以及用表达式取值
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
                                                "expect_val_type": "str"
                                            }
                                        ]
                                    }
                                ]
                            }  # 测试redis-查询结果为str
                        ],
                        "creator": "admin",
                        "modifier": None,
                        "is_public": True
                    }
                ]
            }
        ]
    }
]

scenario_list = [
    {
        "scenario_uuid": "DrxW6nYm2FuxgRmj8brEVt",
        "id": 65,
        "scenario_title": "场景1666949754",
        "case_list": [
            {
                "case_uuid": "hYru8UsE9uDZKrxPSmU3oS",
                "case_info": {
                    "id": 8649,
                    "is_deleted": 0,
                    "case_name": "新的123123",
                    "request_method": "POST",
                    "request_base_url": "/api/123",
                    "request_url": "/api/123",
                    "is_public": 1,
                    "total_execution": 0,
                    "creator": "admin",
                    "creator_id": 1,
                    "create_time": "2022-08-16 15:46:03",
                    "create_timestamp": 1660635931,
                    "modifier": None,
                    "modifier_id": None,
                    "update_time": "2022-08-16 15:46:04",
                    "update_timestamp": None,
                    "remark": "123"
                },
                "bind_info": [
                    {
                        "data_info": {
                            "id": 19331,
                            "data_name": "p1",
                            "request_params": {
                                "a": "123",
                                "b": "456"
                            },
                            "request_headers": {
                                "c": "123",
                                "d": "456"
                            },
                            "request_body": None,
                            "request_body_type": "none",
                            "var_list": "",
                            "update_var_list": [],
                            "is_deleted": 0,
                            "is_public": 1,
                            "creator": "admin",
                            "creator_id": 1,
                            "create_time": "2022-08-16 15:46:03",
                            "create_timestamp": 1660635931,
                            "modifier": None,
                            "modifier_id": None,
                            "update_time": "2022-08-16 15:46:04",
                            "update_timestamp": None,
                            "remark": None,
                            "is_before": None,
                            "data_before": [],
                            "is_after": None,
                            "data_after": []
                        },
                        "case_resp_ass_info": [],
                        "case_field_ass_info": []
                    },
                    {
                        "data_info": {
                            "id": 19332,
                            "data_name": "p2",
                            "request_params": {},
                            "request_headers": {},
                            "request_body": {
                                "a": "b"
                            },
                            "request_body_type": "form-data",
                            "var_list": "",
                            "update_var_list": [],
                            "is_deleted": 0,
                            "is_public": 1,
                            "creator": "admin",
                            "creator_id": 1,
                            "create_time": "2022-08-16 15:46:03",
                            "create_timestamp": 1660635931,
                            "modifier": None,
                            "modifier_id": None,
                            "update_time": "2022-08-16 15:46:04",
                            "update_timestamp": None,
                            "remark": None,
                            "is_before": None,
                            "data_before": [],
                            "is_after": None,
                            "data_after": []
                        },
                        "case_resp_ass_info": [],
                        "case_field_ass_info": []
                    },
                    {
                        "data_info": {
                            "id": 19333,
                            "data_name": "p3",
                            "request_params": {},
                            "request_headers": {},
                            "request_body": {
                                "b": "2"
                            },
                            "request_body_type": "json",
                            "var_list": "",
                            "update_var_list": [],
                            "is_deleted": 0,
                            "is_public": 1,
                            "creator": "admin",
                            "creator_id": 1,
                            "create_time": "2022-08-16 15:46:03",
                            "create_timestamp": 1660635931,
                            "modifier": None,
                            "modifier_id": None,
                            "update_time": "2022-08-16 15:46:04",
                            "update_timestamp": None,
                            "remark": None,
                            "is_before": None,
                            "data_before": [],
                            "is_after": None,
                            "data_after": []
                        },
                        "case_resp_ass_info": [],
                        "case_field_ass_info": []
                    },
                    {
                        "data_info": {
                            "id": 19334,
                            "data_name": "p4",
                            "request_params": {},
                            "request_headers": {},
                            "request_body": "\"<div>123</div>\"",
                            "request_body_type": "html",
                            "var_list": "",
                            "update_var_list": [],
                            "is_deleted": 0,
                            "is_public": 1,
                            "creator": "admin",
                            "creator_id": 1,
                            "create_time": "2022-08-16 15:46:03",
                            "create_timestamp": 1660635931,
                            "modifier": None,
                            "modifier_id": None,
                            "update_time": "2022-08-16 15:46:04",
                            "update_timestamp": None,
                            "remark": None,
                            "is_before": None,
                            "data_before": [],
                            "is_after": None,
                            "data_after": []
                        },
                        "case_resp_ass_info": [],
                        "case_field_ass_info": []
                    }
                ],
                "case_expand": {
                    "index": 8649,
                    "sleep": 29,
                    "case_id": 8649
                }
            },
            {
                "case_uuid": "7B5UDGtbZfemm5Xf857zgT",
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
                    "case_name": "测试重构用例相关123",
                    "creator": "admin",
                    "creator_id": 1,
                    "is_public": True,
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
                                        "db_id": 8899,
                                        "assert_list": []
                                    },  # 测试-数据库不存在或禁用
                                    {
                                        "db_id": 4,
                                        "assert_list": []
                                    },  # 测试-数据库数据类型暂不支持
                                    {
                                        "db_id": 18,
                                        "assert_list": []
                                    },  # 测试-数据库连接失败
                                    {
                                        "db_id": 12,
                                        "assert_list": [
                                            {
                                                "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "id",
                                                        "expect_val": 1,
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"id\")",
                                                        "expect_val_type": "int"
                                                    },
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "case_name",
                                                        "expect_val": "yyx",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"case_name\")",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试mysql-有查询结果
                                    {
                                        "db_id": 12,
                                        "assert_list": [
                                            {
                                                "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=0;",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "id",
                                                        "expect_val": 1,
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"id\")",
                                                        "expect_val_type": "int"
                                                    },
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "case_name",
                                                        "expect_val": "yyx",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"case_name\")",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试mysql-无查询结果
                                    {
                                        "db_id": 9,
                                        "assert_list": [
                                            {
                                                "query": "get 127.0.0.1111111",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "username",
                                                        "expect_val": "user_00007",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get('username')",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试redis-无查询结果
                                    {
                                        "db_id": 9,
                                        "assert_list": [
                                            {
                                                "query": "get 127.0.0.1",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "username",
                                                        "expect_val": "yyx_999",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get('username')",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试redis-查询结果为dict以及用表达式取值
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
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    }  # 测试redis-查询结果为str
                                ],
                                "creator": "admin",
                                "modifier": None,
                                "is_public": True
                            }
                        ]
                    }
                ],
                "case_expand": {
                    "index": 2,
                    "sleep": 10,
                    "case_id": 8646
                }
            },
            {
                "case_uuid": "2kZGYrkarcb9Aa2SK7R7NU",
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
                    "case_name": "测试重构用例相关123",
                    "creator": "admin",
                    "creator_id": 1,
                    "is_public": True,
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
                                                "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "id",
                                                        "expect_val": 1,
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"id\")",
                                                        "expect_val_type": "int"
                                                    },
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "case_name",
                                                        "expect_val": "yyx",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get(\"case_name\")",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试mysql-有查询结果
                                    {
                                        "db_id": 9,
                                        "assert_list": [
                                            {
                                                "query": "get 127.0.0.1",
                                                "assert_field_list": [
                                                    {
                                                        "rule": "==",
                                                        "assert_key": "username",
                                                        "expect_val": "yyx_999",
                                                        "is_expression": 1,
                                                        "python_val_exp": "obj.get('username')",
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    },  # 测试redis-查询结果为dict以及用表达式取值
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
                                                        "expect_val_type": "str"
                                                    }
                                                ]
                                            }
                                        ]
                                    }  # 测试redis-查询结果为str
                                ],
                                "creator": "admin",
                                "modifier": None,
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

# 单用例/多用例
test_obj = {
    "project_id": 30,
    "execute_id": 8646,
    "execute_name": "测试重构用例相关",
    "execute_key": "case",
    "execute_type": "case",
    "execute_label": "execute_label",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
    "case_list": case_list,
    "scenario_list": [],
    "use_dd_push": False,
    "dd_push_id": "",
    "ding_talk_url": "",
    "use_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 5
}

# 单场景/多场景
test_obj2 = {
    "project_id": 30,
    "execute_id": 65,
    "execute_name": "测试编辑场景",
    "execute_type": "scenario",
    "execute_label": "execute_label",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
    "case_list": [],
    "scenario_list": [
        {
            "scenario_uuid": "GNwvyXy6qYsmedCdYuwUwp",
            "id": 65,
            "scenario_title": "场景1666949754",
            "case_list": [
                {
                    "case_info": {
                        "id": 8649,
                        "is_deleted": 0,
                        "case_name": "新的123123",
                        "request_method": "POST",
                        "request_base_url": "/api/123",
                        "request_url": "/api/123",
                        "is_public": 1,
                        "total_execution": 0,
                        "creator": "admin",
                        "creator_id": 1,
                        "create_time": "2022-08-16 15:46:03",
                        "create_timestamp": 1660635931,
                        "modifier": None,
                        "modifier_id": None,
                        "update_time": "2022-08-16 15:46:04",
                        "update_timestamp": None,
                        "remark": "123"
                    },
                    "bind_info": [
                        {
                            "data_info": {
                                "id": 19331,
                                "data_name": "p1",
                                "request_params": {
                                    "a": "123",
                                    "b": "456"
                                },
                                "request_headers": {
                                    "c": "123",
                                    "d": "456"
                                },
                                "request_body": None,
                                "request_body_type": "none",
                                "var_list": "",
                                "update_var_list": [],
                                "is_deleted": 0,
                                "is_public": 1,
                                "creator": "admin",
                                "creator_id": 1,
                                "create_time": "2022-08-16 15:46:03",
                                "create_timestamp": 1660635931,
                                "modifier": None,
                                "modifier_id": None,
                                "update_time": "2022-08-16 15:46:04",
                                "update_timestamp": None,
                                "remark": None,
                                "is_before": None,
                                "data_before": [],
                                "is_after": None,
                                "data_after": []
                            },
                            "case_resp_ass_info": [],
                            "case_field_ass_info": []
                        },
                        {
                            "data_info": {
                                "id": 19332,
                                "data_name": "p2",
                                "request_params": {},
                                "request_headers": {},
                                "request_body": {
                                    "a": "b"
                                },
                                "request_body_type": "form-data",
                                "var_list": "",
                                "update_var_list": [],
                                "is_deleted": 0,
                                "is_public": 1,
                                "creator": "admin",
                                "creator_id": 1,
                                "create_time": "2022-08-16 15:46:03",
                                "create_timestamp": 1660635931,
                                "modifier": None,
                                "modifier_id": None,
                                "update_time": "2022-08-16 15:46:04",
                                "update_timestamp": None,
                                "remark": None,
                                "is_before": None,
                                "data_before": [],
                                "is_after": None,
                                "data_after": []
                            },
                            "case_resp_ass_info": [],
                            "case_field_ass_info": []
                        },
                        {
                            "data_info": {
                                "id": 19333,
                                "data_name": "p3",
                                "request_params": {},
                                "request_headers": {},
                                "request_body": {
                                    "b": "2"
                                },
                                "request_body_type": "json",
                                "var_list": "",
                                "update_var_list": [],
                                "is_deleted": 0,
                                "is_public": 1,
                                "creator": "admin",
                                "creator_id": 1,
                                "create_time": "2022-08-16 15:46:03",
                                "create_timestamp": 1660635931,
                                "modifier": None,
                                "modifier_id": None,
                                "update_time": "2022-08-16 15:46:04",
                                "update_timestamp": None,
                                "remark": None,
                                "is_before": None,
                                "data_before": [],
                                "is_after": None,
                                "data_after": []
                            },
                            "case_resp_ass_info": [],
                            "case_field_ass_info": []
                        },
                        {
                            "data_info": {
                                "id": 19334,
                                "data_name": "p4",
                                "request_params": {},
                                "request_headers": {},
                                "request_body": "\"<div>123</div>\"",
                                "request_body_type": "html",
                                "var_list": "",
                                "update_var_list": [],
                                "is_deleted": 0,
                                "is_public": 1,
                                "creator": "admin",
                                "creator_id": 1,
                                "create_time": "2022-08-16 15:46:03",
                                "create_timestamp": 1660635931,
                                "modifier": None,
                                "modifier_id": None,
                                "update_time": "2022-08-16 15:46:04",
                                "update_timestamp": None,
                                "remark": None,
                                "is_before": None,
                                "data_before": [],
                                "is_after": None,
                                "data_after": []
                            },
                            "case_resp_ass_info": [],
                            "case_field_ass_info": []
                        }
                    ],
                    "case_uuid": "Vcm94g5G847HQ9hrASx48o",
                    "case_expand": {
                        "index": 8649,
                        "sleep": 29,
                        "case_id": 8649
                    }
                },
                {
                    "case_info": {
                        "id": 8646,
                        "is_deleted": 0,
                        "case_name": "测试重构用例相关",
                        "request_method": "POST",
                        "request_base_url": "http://0.0.0.0:7878",
                        "request_url": "${重构url}",
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
                                                    "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                                    "assert_field_list": [
                                                        {
                                                            "rule": "==",
                                                            "assert_key": "id",
                                                            "expect_val": 1,
                                                            "is_expression": 1,
                                                            "python_val_exp": "obj.get(\"id\")",
                                                            "expect_val_type": "int"
                                                        },
                                                        {
                                                            "rule": "==",
                                                            "assert_key": "case_name",
                                                            "expect_val": "yyx",
                                                            "is_expression": 1,
                                                            "python_val_exp": "obj.get(\"case_name\")",
                                                            "expect_val_type": "str"
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
                                                            "expect_val_type": "str"
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
                                                            "expect_val_type": "str"
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
                    "case_uuid": "b7m8kgJbhNBgrnwSzMjPsb",
                    "case_expand": {
                        "index": 2,
                        "sleep": 10,
                        "case_id": 8646
                    }
                },
                {
                    "case_info": {
                        "id": 8646,
                        "is_deleted": 0,
                        "case_name": "测试重构用例相关",
                        "request_method": "POST",
                        "request_base_url": "http://0.0.0.0:7878",
                        "request_url": "${重构url}",
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
                                                    "query": "select id, case_name FROM ExileTestPlatform.exile5_test_case WHERE id=1;",
                                                    "assert_field_list": [
                                                        {
                                                            "rule": "==",
                                                            "assert_key": "id",
                                                            "expect_val": 1,
                                                            "is_expression": 1,
                                                            "python_val_exp": "obj.get(\"id\")",
                                                            "expect_val_type": "int"
                                                        },
                                                        {
                                                            "rule": "==",
                                                            "assert_key": "case_name",
                                                            "expect_val": "yyx",
                                                            "is_expression": 1,
                                                            "python_val_exp": "obj.get(\"case_name\")",
                                                            "expect_val_type": "str"
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
                                                            "expect_val_type": "str"
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
                                                            "expect_val_type": "str"
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
                    "case_uuid": "MiEYzbeMfirdWVQjDAN983",
                    "case_expand": {
                        "index": 1,
                        "sleep": 10,
                        "case_id": 8646
                    }
                }
            ]
        }
    ],
    "use_dd_push": False,
    "dd_push_id": "",
    "ding_talk_url": "",
    "use_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 5
}

# 混合
test_obj3 = {
    "project_id": 30,
    "execute_id": 30,
    "execute_name": "测试编辑场景",
    "execute_type": "project",
    "execute_label": "execute_label",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
    "case_list": [],
    "scenario_list": [],
    "use_dd_push": False,
    "dd_push_id": "",
    "ding_talk_url": "",
    "use_mail": False,
    "mail_list": [],
    "trigger_type": "user_execute",
    "request_timeout": 5
}


async def test_ael():
    """测试生成异步执行日志模型"""

    ael = AsyncLogs()
    await ael.gen_case_logs_dict(case_list=test_obj.get('case_list'))
    await ael.gen_scenario_logs_dict(scenario_list=test_obj.get('scenario_list'))

    print(json.dumps(ael.case_logs_dict, ensure_ascii=False))
    print('=' * 100)
    print(json.dumps(ael.scenario_logs_dict, ensure_ascii=False))


async def test_execute():
    """测试执行用例与场景"""

    acr = AsyncCaseRunner(test_obj=test_obj, is_debug=True)
    # acr = AsyncCaseRunner(test_obj=test_obj2, is_debug=True)
    # acr = AsyncCaseRunner(test_obj=test_obj3, is_debug=True)
    await acr.main()


if __name__ == '__main__':
    """单元测试"""

    asyncio.run(test_execute())
