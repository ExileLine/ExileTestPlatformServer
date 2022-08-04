# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test.py
# @Software: PyCharm

import asyncio
import json

from common.libs.async_case_runner import CaseRunner, AsyncCaseRunner

test_obj1 = {
    "execute_id": 8641,
    "execute_name": "执行用例:[登录成功okc2]",
    "execute_type": "case",
    "execute_label": "only",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": False,
    "is_execute_all": False,
    "case_list": [
        {
            "case_info": {
                "status": 1,
                "total_execution": 10,
                "case_name": "登录成功okc2",
                "is_public": True,
                "create_time": "2022-08-01 11:43:36",
                "request_method": "POST",
                "creator": "admin",
                "id": 8641,
                "request_base_url": "http://106.75.174.40:5000",
                "creator_id": 1,
                "create_timestamp": 1659325393,
                "request_url": "/api/login",
                "modifier": "admin",
                "update_time": "2022-08-01 11:44:03",
                "is_pass": 0,
                "modifier_id": 1,
                "update_timestamp": 1659325393,
                "is_shared": True,
                "remark": "用例: 635-登录成功9999999 的复制",
                "is_deleted": 0
            },
            "bind_info": [
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-04-01 17:16:34",
                        "data_name": "yyyyyyyyyyyyyyy",
                        "data_size": 56,
                        "creator_id": 1,
                        "create_timestamp": 1648804537,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:24:03",
                        "request_headers": {
                            "token": ""
                        },
                        "data_before": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 217,
                        "update_var_list": [
                            {
                                "id": 2,
                                "remark": "脚本生成:1",
                                "status": 1,
                                "creator": "脚本生成:1",
                                "modifier": None,
                                "var_name": "token",
                                "var_type": 2,
                                "is_active": None,
                                "is_public": 1,
                                "last_func": None,
                                "var_value": None,
                                "creator_id": 999999,
                                "expression": "obj.get('data').get('token')",
                                "is_deleted": 0,
                                "var_source": "resp_data",
                                "create_time": "2021-12-09 17:39:17",
                                "modifier_id": None,
                                "update_time": "2021-12-09 17:39:17",
                                "var_get_key": "code",
                                "inputVisible": False,
                                "is_expression": 1,
                                "last_func_var": None,
                                "create_timestamp": 1639042757,
                                "update_timestamp": None
                            }
                        ]
                    },
                    "case_resp_ass_info": [
                        {
                            "create_time": "2022-03-11 16:57:17",
                            "update_time": "2022-07-05 15:57:18",
                            "is_deleted": 0,
                            "assert_description": "200",
                            "is_public": 1,
                            "creator": "admin",
                            "modifier": "admin",
                            "remark": "",
                            "create_timestamp": 1646988270,
                            "id": 86,
                            "update_timestamp": 1656984261,
                            "status": 1,
                            "ass_json": [
                                {
                                    "rule": "==",
                                    "assert_key": "code",
                                    "expect_val": 200,
                                    "is_expression": 1,
                                    "python_val_exp": "obj.get(\"code\")",
                                    "expect_val_type": 1,
                                    "response_source": "response_body"
                                },
                                {
                                    "rule": "in",
                                    "assert_key": "message",
                                    "expect_val": "登录",
                                    "is_expression": 0,
                                    "python_val_exp": "",
                                    "expect_val_type": 2,
                                    "response_source": "response_body"
                                }
                            ],
                            "creator_id": 1,
                            "modifier_id": 1
                        }
                    ],
                    "case_field_ass_info": [
                        {
                            "update_time": "2022-06-16 15:44:51",
                            "id": 73,
                            "is_deleted": 0,
                            "assert_description": "测试重构1234567",
                            "is_public": 1,
                            "creator": "admin",
                            "modifier": "admin",
                            "remark": "",
                            "create_timestamp": 1651137930,
                            "update_timestamp": 1655365126,
                            "create_time": "2022-04-28 17:29:58",
                            "status": 1,
                            "ass_json": [
                                {
                                    "db_id": 12,
                                    "assert_list": [
                                        {
                                            "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                            "assert_field_list": [
                                                {
                                                    "rule": "==",
                                                    "assert_key": "id",
                                                    "expect_val": 1,
                                                    "is_expression": 0,
                                                    "python_val_exp": "",
                                                    "expect_val_type": "1"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "creator_id": 1,
                            "modifier_id": 1
                        },
                        {
                            "update_time": "2022-04-28 17:40:01",
                            "id": 74,
                            "is_deleted": 0,
                            "assert_description": "测试重构7654321",
                            "is_public": 1,
                            "creator": "admin",
                            "modifier": None,
                            "remark": "",
                            "create_timestamp": 1651138593,
                            "update_timestamp": None,
                            "create_time": "2022-04-28 17:40:01",
                            "status": 1,
                            "ass_json": [
                                {
                                    "db_id": 13,
                                    "assert_list": [
                                        {
                                            "query": "get admin",
                                            "assert_field_list": [
                                                {
                                                    "rule": "==",
                                                    "assert_key": "admin",
                                                    "expect_val": 1,
                                                    "is_expression": 0,
                                                    "python_val_exp": "",
                                                    "expect_val_type": "1"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "creator_id": 1,
                            "modifier_id": None
                        }
                    ]
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:24:51",
                        "data_name": "yyx2",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19296,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [],
                    "case_field_ass_info": []
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 1,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:25:03",
                        "data_name": "yyx3",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19297,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [],
                    "case_field_ass_info": []
                }
            ]
        }
    ],
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

test_obj = {
    "execute_id": 8641,
    "execute_name": "执行用例:[登录成功okc2]",
    "execute_type": "case",
    "execute_label": "only",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": False,
    "is_execute_all": False,
    "case_list": [
        {
            "case_info": {
                "status": 1,
                "total_execution": 10,
                "case_name": "登录成功okc2",
                "is_public": True,
                "create_time": "2022-08-01 11:43:36",
                "request_method": "POST",
                "creator": "admin",
                "id": 8641,
                "request_base_url": "http://106.75.174.40:5000",
                "creator_id": 1,
                "create_timestamp": 1659325393,
                "request_url": "/api/login",
                "modifier": "admin",
                "update_time": "2022-08-01 11:44:03",
                "is_pass": 0,
                "modifier_id": 1,
                "update_timestamp": 1659325393,
                "is_shared": True,
                "remark": "用例: 635-登录成功9999999 的复制",
                "is_deleted": 0
            },
            "bind_info": [
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-04-01 17:16:34",
                        "data_name": "yyyyyyyyyyyyyyy",
                        "data_size": 56,
                        "creator_id": 1,
                        "create_timestamp": 1648804537,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:24:03",
                        "request_headers": {
                            "token": {"a": "123"},
                            "token123": "yyx"
                        },
                        "data_before": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 217,
                        "update_var_list": [
                            {
                                "id": 2,
                                "remark": "脚本生成:1",
                                "status": 1,
                                "creator": "脚本生成:1",
                                "modifier": None,
                                "var_name": "token",
                                "var_type": 2,
                                "is_active": None,
                                "is_public": 1,
                                "last_func": None,
                                "var_value": None,
                                "creator_id": 999999,
                                "expression": "obj.get('data').get('token')",
                                "is_deleted": 0,
                                "var_source": "resp_data",
                                "create_time": "2021-12-09 17:39:17",
                                "modifier_id": None,
                                "update_time": "2021-12-09 17:39:17",
                                "var_get_key": "code",
                                "inputVisible": False,
                                "is_expression": 1,
                                "last_func_var": None,
                                "create_timestamp": 1639042757,
                                "update_timestamp": None
                            }
                        ]
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "1"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "1"}
                    ]
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:24:51",
                        "data_name": "yyx2",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19296,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "2"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "2"}
                    ]
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 1,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:25:03",
                        "data_name": "yyx3",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19297,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "3"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "3"}
                    ]
                }
            ]
        },
        {
            "case_info": {
                "status": 1,
                "total_execution": 10,
                "case_name": "登录成功okc2",
                "is_public": True,
                "create_time": "2022-08-01 11:43:36",
                "request_method": "POST",
                "creator": "admin",
                "id": 8641,
                "request_base_url": "http://106.75.174.40:5000",
                "creator_id": 1,
                "create_timestamp": 1659325393,
                "request_url": "/api/login",
                "modifier": "admin",
                "update_time": "2022-08-01 11:44:03",
                "is_pass": 0,
                "modifier_id": 1,
                "update_timestamp": 1659325393,
                "is_shared": True,
                "remark": "用例: 635-登录成功9999999 的复制",
                "is_deleted": 0
            },
            "bind_info": [
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-04-01 17:16:34",
                        "data_name": "yyyyyyyyyyyyyyy",
                        "data_size": 56,
                        "creator_id": 1,
                        "create_timestamp": 1648804537,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:24:03",
                        "request_headers": {
                            "token": ""
                        },
                        "data_before": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 0,
                                                "python_val_exp": ""
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [
                            {
                                "db_id": 12,
                                "query_list": [
                                    {
                                        "query": "select id, case_name FROM ExileTestPlatform.exile_test_case WHERE id=1 and case_name=\"${sql语句变量}\";",
                                        "field_list": [
                                            {
                                                "var_id": 82,
                                                "field_name": "id",
                                                "field_type": "1",
                                                "is_expression": 0,
                                                "python_val_exp": "obj.get(\"id\")"
                                            },
                                            {
                                                "var_id": 83,
                                                "field_name": "case_name",
                                                "field_type": "2",
                                                "is_expression": 1,
                                                "python_val_exp": "obj.get(\"case_name\")"
                                            }
                                        ]
                                    }
                                ]
                            }
                        ],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 217,
                        "update_var_list": [
                            {
                                "id": 2,
                                "remark": "脚本生成:1",
                                "status": 1,
                                "creator": "脚本生成:1",
                                "modifier": None,
                                "var_name": "token",
                                "var_type": 2,
                                "is_active": None,
                                "is_public": 1,
                                "last_func": None,
                                "var_value": None,
                                "creator_id": 999999,
                                "expression": "obj.get('data').get('token')",
                                "is_deleted": 0,
                                "var_source": "resp_data",
                                "create_time": "2021-12-09 17:39:17",
                                "modifier_id": None,
                                "update_time": "2021-12-09 17:39:17",
                                "var_get_key": "code",
                                "inputVisible": False,
                                "is_expression": 1,
                                "last_func_var": None,
                                "create_timestamp": 1639042757,
                                "update_timestamp": None
                            }
                        ]
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "1"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "1"}
                    ]
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 0,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:24:51",
                        "data_name": "yyx2",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19296,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "2"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "2"}
                    ]
                },
                {
                    "case_data_info": {
                        "status": 1,
                        "is_public": 1,
                        "creator": "admin",
                        "create_time": "2022-08-01 11:25:03",
                        "data_name": "yyx3",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {},
                        "data_before": [],
                        "modifier_id": 1,
                        "update_timestamp": 1659324113,
                        "request_body": {
                            "a": "${测试前置准备(用mysql)}",
                            "b": "${测试前置准备(用redis)}",
                            "password": "123456",
                            "username": "admin"
                        },
                        "is_after": 0,
                        "request_body_type": 2,
                        "data_after": [],
                        "remark": None,
                        "is_deleted": 0,
                        "var_list": None,
                        "md5": None,
                        "id": 19297,
                        "update_var_list": []
                    },
                    "case_resp_ass_info": [
                        {"resp_ass": "3"}
                    ],
                    "case_field_ass_info": [
                        {"field_ass": "3"}
                    ]
                }
            ]
        }
    ],
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


def test_sync_request():
    """1"""
    d = {
        'url': 'http://106.75.174.40:5000/api/login',
        'headers': {
            'token': '123',
            'token123': json.dumps({"a": "123"})
        },
        'json': {'a': 1, 'b': '测试用例B1', 'password': '123456', 'username': 'admin'}
    }
    cr = CaseRunner({})
    resp = cr.current_request('post', **d)
    print(resp)


if __name__ == '__main__':
    """1"""

    # test async request
    acr = AsyncCaseRunner(test_obj=test_obj)
    asyncio.run(acr.test_loader_dev())

    # test_sync_request()
