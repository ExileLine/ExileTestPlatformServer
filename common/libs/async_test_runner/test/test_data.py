# -*- coding: utf-8 -*-
# @Time    : 2022/9/2 14:03
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_data.py
# @Software: PyCharm


case1 = {
    "case_info": {
        "id": 177,
        "case_name": "登录成功177",
        "status": 1,
        "total_execution": 10,
        "is_public": True,
        "create_time": "2022-08-01 11:43:36",
        "request_method": "POST",
        "creator": "admin",
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
                "id": 1771,
                "data_name": "177-第一个",
                "status": 1,
                "is_public": 0,
                "creator": "admin",
                "create_time": "2022-04-01 17:16:34",
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
                "request_body_type": "json",
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
                "update_var_list": [
                    {
                        "id": 801,
                        "var_name": "801-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    },
                    {
                        "id": 802,
                        "var_name": "802-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    }
                ]
            },
            "case_resp_ass_info": [
                {"rule": "==", "uuid": "Xz4RF45iCgDHCkTiGYS2fT-1661339358", "assert_key": "code",
                 "expect_val": "200", "is_expression": True, "python_val_exp": "obj.get(\"code\")",
                 "expect_val_type": "int", "response_source": "response_body"},
                {"rule": "==", "uuid": "hxYzEfCNoSQzkdMXQHELa3-1661339358", "assert_key": "code",
                 "expect_val": "200", "is_expression": False, "python_val_exp": "", "expect_val_type": "int",
                 "response_source": "response_body"},
                {"rule": ">", "uuid": "bxCDs7PfdsPUdJzua3x3UD-1661339358", "assert_key": "code",
                 "expect_val": "100", "is_expression": False, "python_val_exp": "", "expect_val_type": "int",
                 "response_source": "response_body"},
                {"rule": "<", "uuid": "LLoZqmYtWjGY3uMrBTAS9i-1661339358", "assert_key": "code",
                 "expect_val": "300", "is_expression": False, "python_val_exp": "", "expect_val_type": "int",
                 "response_source": "response_body"},
                {"rule": "==", "uuid": "htsX2dSHnn8A2V6vNqoSmA-1661339358", "assert_key": "message",
                 "expect_val": "登录成功", "is_expression": False, "python_val_exp": "", "expect_val_type": "str",
                 "response_source": "response_body"},
                {"rule": "==", "uuid": "RKwtqExkiSPtvCL2KaBQGR-1661339358", "assert_key": "log_uuid",
                 "expect_val": "${重构url}", "is_expression": False,
                 "python_val_exp": "", "expect_val_type": "str", "response_source": "response_headers"}
            ],
            "case_field_ass_info": [
                {"field_ass": "177-1"}
            ]
        },
        {
            "case_data_info": {
                "id": 1772,
                "data_name": "177-第二个",
                "status": 1,
                "is_public": 0,
                "creator": "admin",
                "create_time": "2022-08-01 11:24:51",
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
                "request_body_type": "json",
                "data_after": [],
                "remark": None,
                "is_deleted": 0,
                "var_list": None,
                "md5": None,
                "update_var_list": [
                    {
                        "id": 803,
                        "var_name": "803-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    },
                    {
                        "id": 804,
                        "var_name": "804-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    }
                ]
            },
            "case_resp_ass_info": [],
            "case_field_ass_info": [
                {"field_ass": "177-2"}
            ]
        },
        {
            "case_data_info": {
                "id": 1773,
                "data_name": "177-第三个",
                "status": 1,
                "is_public": 1,
                "creator": "admin",
                "create_time": "2022-08-01 11:25:03",
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
                "request_body_type": "json",
                "data_after": [],
                "remark": None,
                "is_deleted": 0,
                "var_list": None,
                "md5": None,
                "update_var_list": [
                    {
                        "id": 805,
                        "var_name": "805-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    },
                    {
                        "id": 806,
                        "var_name": "806-token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "expression": "obj.get('data').get('token')",
                        "var_source": "response_body",
                        "var_get_key": "code",
                        "is_expression": 1
                    }
                ]
            },
            "case_resp_ass_info": [],
            "case_field_ass_info": [
                {"field_ass": "177-3"}
            ]
        }
    ]
}
case2 = {
    "case_info": {
        "id": 102,
        "case_name": "登录成功102",
        "status": 1,
        "total_execution": 10,
        "is_public": True,
        "create_time": "2022-08-01 11:43:36",
        "request_method": "POST",
        "creator": "admin",
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
                "id": 1241,
                "data_name": "124-第一个",
                "status": 1,
                "is_public": 0,
                "creator": "admin",
                "create_time": "2022-04-01 17:16:34",
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
                "request_body_type": "json",
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
                "update_var_list": [
                    {
                        "id": 2,
                        "remark": "脚本生成:1",
                        "status": 1,
                        "creator": "脚本生成:1",
                        "modifier": None,
                        "var_name": "token",
                        "var_type": "str",
                        "is_active": None,
                        "is_public": 1,
                        "last_func": None,
                        "var_value": None,
                        "creator_id": 999999,
                        "expression": "obj.get('data').get('token')",
                        "is_deleted": 0,
                        "var_source": "response_body",
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
            "case_resp_ass_info": [],
            "case_field_ass_info": [
                {"field_ass": "102-1"}
            ]
        },
        {
            "case_data_info": {
                "id": 1242,
                "data_name": "124-第二个",
                "status": 1,
                "is_public": 0,
                "creator": "admin",
                "create_time": "2022-08-01 11:24:51",
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
                "request_body_type": "json",
                "data_after": [],
                "remark": None,
                "is_deleted": 0,
                "var_list": None,
                "md5": None,
                "update_var_list": []
            },
            "case_resp_ass_info": [],
            "case_field_ass_info": [
                {"field_ass": "102-2"}
            ]
        },
        {
            "case_data_info": {
                "id": 1243,
                "data_name": "124-第三个",
                "status": 1,
                "is_public": 1,
                "creator": "admin",
                "create_time": "2022-08-01 11:25:03",
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
                "request_body_type": "json",
                "data_after": [],
                "remark": None,
                "is_deleted": 0,
                "var_list": None,
                "md5": None,
                "update_var_list": []
            },
            "case_resp_ass_info": [],
            "case_field_ass_info": [
                {"field_ass": "102-3"}
            ]
        }
    ]
}
case_list = [
    case1
]

scenario_list = [
    {
        "case_list": [
            {
                "case_info": {
                    "status": 1,
                    "total_execution": 10,
                    "case_name": "登录成功123",
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
                            "request_body_type": "json",
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
                            "id": 199,
                            "update_var_list": [
                                {
                                    "id": 2,
                                    "remark": "脚本生成:1",
                                    "status": 1,
                                    "creator": "脚本生成:1",
                                    "modifier": None,
                                    "var_name": "token",
                                    "var_type": "str",
                                    "is_active": None,
                                    "is_public": 1,
                                    "last_func": None,
                                    "var_value": None,
                                    "creator_id": 999999,
                                    "expression": "obj.get('data').get('token')",
                                    "is_deleted": 0,
                                    "var_source": "response_body",
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
                            {"rule": "==", "uuid": "Xz4RF45iCgDHCkTiGYS2fT-1661339358", "assert_key": "code",
                             "expect_val": "200", "is_expression": True, "python_val_exp": "obj.get(\"code\")",
                             "expect_val_type": "int", "response_source": "response_body"},
                            {"rule": "==", "uuid": "hxYzEfCNoSQzkdMXQHELa3-1661339358", "assert_key": "code",
                             "expect_val": "200", "is_expression": False, "python_val_exp": "",
                             "expect_val_type": "int",
                             "response_source": "response_body"},
                            {"rule": ">", "uuid": "bxCDs7PfdsPUdJzua3x3UD-1661339358", "assert_key": "code",
                             "expect_val": "100", "is_expression": False, "python_val_exp": "",
                             "expect_val_type": "int",
                             "response_source": "response_body"},
                            {"rule": "<", "uuid": "LLoZqmYtWjGY3uMrBTAS9i-1661339358", "assert_key": "code",
                             "expect_val": "300", "is_expression": False, "python_val_exp": "",
                             "expect_val_type": "int",
                             "response_source": "response_body"},
                            {"rule": "==", "uuid": "htsX2dSHnn8A2V6vNqoSmA-1661339358", "assert_key": "message",
                             "expect_val": "登录成功", "is_expression": False, "python_val_exp": "",
                             "expect_val_type": "str",
                             "response_source": "response_body"},
                            {"rule": "==", "uuid": "RKwtqExkiSPtvCL2KaBQGR-1661339358", "assert_key": "log_uuid",
                             "expect_val": "${重构url}", "is_expression": False,
                             "python_val_exp": "", "expect_val_type": "str", "response_source": "response_headers"}
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
                            "request_body_type": "json",
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
                            "request_body_type": "json",
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
                ],
                "case_expand": {
                    "sleep": 1
                }
            },
            {
                "case_info": {
                    "status": 1,
                    "total_execution": 10,
                    "case_name": "登录成功456",
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
                            "request_body_type": "json",
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
                            "id": 256,
                            "update_var_list": [
                                {
                                    "id": 2,
                                    "remark": "脚本生成:1",
                                    "status": 1,
                                    "creator": "脚本生成:1",
                                    "modifier": None,
                                    "var_name": "token",
                                    "var_type": "str",
                                    "is_active": None,
                                    "is_public": 1,
                                    "last_func": None,
                                    "var_value": None,
                                    "creator_id": 999999,
                                    "expression": "obj.get('data').get('token')",
                                    "is_deleted": 0,
                                    "var_source": "response_body",
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
                        "case_resp_ass_info": [],
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
                            "request_body_type": "json",
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
                            "request_body_type": "json",
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
                ],
                "case_expand": {}
            }
        ],
        "create_time": "2022-08-29 14:37:24",
        "create_timestamp": 1661754807,
        "creator": "admin",
        "creator_id": 1,
        "id": 63,
        "is_deleted": 0,
        "is_public": True,
        "is_shared": False,
        "modifier": "admin",
        "modifier_id": 1,
        "module_list": [],
        "remark": None,
        "scenario_title": "测试编辑场景",
        "status": 1,
        "total_execution": 0,
        "update_time": "2022-08-29 14:38:43",
        "update_timestamp": 1661754807,
        "version_list": []
    }
]

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
