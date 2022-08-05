# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:40
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_case_loader.py
# @Software: PyCharm

import asyncio
import json

from common.libs.async_case_runner import CaseRunner, AsyncCaseRunner

test_obj = {
    "execute_id": 8641,
    "execute_name": "执行用例:[登录成功okc2]",
    "execute_type": "case",
    "execute_label": "only",
    "execute_user_id": 1,
    "execute_username": "admin",
    "base_url": "",
    "use_base_url": False,
    "data_driven": True,
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
                "id": 123,
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
                        "data_name": "123-第一个",
                        "data_size": 56,
                        "creator_id": 1,
                        "create_timestamp": 1648804537,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:24:03",
                        "request_headers": {
                            "token": {"a": "123"},
                            "token123": "123-第一个"
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
                        "id": 1,
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
                        "data_name": "123-第二个",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {
                            "a": "123-第二个"
                        },
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
                        "id": 2,
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
                        "data_name": "123-第三个",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {
                            "a": "123-第三个"
                        },
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
                        "id": 3,
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
                "id": 124,
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
                        "data_name": "124-第一个",
                        "data_size": 56,
                        "creator_id": 1,
                        "create_timestamp": 1648804537,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:24:03",
                        "request_headers": {
                            "token": "124-第一个"
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
                        "id": 4,
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
                        "data_name": "124-第二个",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {
                            "token": "124-第二个"
                        },
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
                        "id": 5,
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
                        "data_name": "124-第三个",
                        "data_size": 169,
                        "creator_id": 1,
                        "create_timestamp": 1659324113,
                        "request_params": {},
                        "is_before": 0,
                        "modifier": "admin",
                        "update_time": "2022-08-01 11:25:08",
                        "request_headers": {
                            "token": "124-第三个"
                        },
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
                        "id": 6,
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
    asyncio.run(acr.case_loader())

    # test_sync_request()
