# -*- coding: utf-8 -*-
# @Time    : 2021/11/9 2:22 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_execute_case.py
# @Software: PyCharm


from common.libs.CaseDrivenResult import MainTest

if __name__ == '__main__':
    demo1 = {
        'case_info': {
            'id': 14, 'create_time': '2021-09-01 20:27:32', 'create_timestamp': 1630499057,
            'update_time': '2021-09-01 20:27:32', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
            'case_name': '测试indexApi', 'request_method': 'GET',
            'request_url': 'http://127.0.0.1:7272/api', 'creator': '调试', 'creator_id': 1,
            'modifier': None, 'modifier_id': None, 'remark': 'remark'},
        'bind_info': [
            {'case_data_info': {
                'id': 12, 'create_time': '2021-09-01 20:34:39', 'create_timestamp': 1630499057,
                'update_time': '2021-09-01 20:34:40', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                'data_name': '数据99999', 'request_params': {}, 'request_headers': {}, 'request_body': {},
                'request_body_type': 1,
                'var_list': ['user_id', 'username'], 'update_var_list': [{'3': '更新'}], 'creator': '调试', 'creator_id': 1,
                'modifier': None, 'modifier_id': None, 'remark': None}, 'case_resp_ass_info': [
                {'id': 21, 'create_time': '2021-09-13 12:49:07', 'create_timestamp': 1631508310,
                 'update_time': '2021-09-13 12:49:08', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                 'assert_description': 'Resp通用断言123', 'ass_json': [
                    {'rule': '__eq__', 'assert_key': 'code', 'expect_val': 200, 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '1'},
                    {'rule': '__ge__', 'assert_key': 'code', 'expect_val': 200, 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '1'},
                    {'rule': '__eq__', 'assert_key': 'message', 'expect_val': 'index', 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '2'},
                    {'rule': '__eq__', 'assert_key': 'message', 'expect_val': 'index', 'is_expression': 1,
                     'python_val_exp': "okc.get('message')", 'expect_val_type': '2'}], 'creator': '调试', 'creator_id': 1,
                 'modifier': None, 'modifier_id': None, 'remark': 'remark'}], 'case_field_ass_info': [
                {'id': 33, 'create_time': '2021-09-11 17:18:10', 'create_timestamp': 1631351884,
                 'update_time': '2021-09-11 17:18:11', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                 'assert_description': 'A通用字段校验', 'ass_json': [
                    {'db_id': 1, 'query': 'select id,case_name FROM ExilicTestPlatform.exile_test_case WHERE id=1;',
                     'assert_list': [{'rule': '__eq__', 'assert_key': 'id', 'expect_val': 1, 'expect_val_type': '1'},
                                     {'rule': '__eq__', 'assert_key': 'case_name', 'expect_val': '测试用例B1',
                                      'expect_val_type': '2'}]}], 'creator': '调试', 'creator_id': 1, 'modifier': None,
                 'modifier_id': None, 'remark': 'remark'}]},
            {'case_data_info': {
                'id': 12, 'create_time': '2021-09-01 20:34:39', 'create_timestamp': 1630499057,
                'update_time': '2021-09-01 20:34:40', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                'data_name': '数据99999', 'request_params': {}, 'request_headers': {}, 'request_body': {},
                'request_body_type': 1,
                'var_list': ['user_id', 'username'], 'update_var_list': [{'3': '更新'}], 'creator': '调试', 'creator_id': 1,
                'modifier': None, 'modifier_id': None, 'remark': None}, 'case_resp_ass_info': [
                {'id': 21, 'create_time': '2021-09-13 12:49:07', 'create_timestamp': 1631508310,
                 'update_time': '2021-09-13 12:49:08', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                 'assert_description': 'Resp通用断言123', 'ass_json': [
                    {'rule': '__eq__', 'assert_key': 'code', 'expect_val': 200, 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '1'},
                    {'rule': '__ge__', 'assert_key': 'code', 'expect_val': 200, 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '1'},
                    {'rule': '__eq__', 'assert_key': 'message', 'expect_val': 'index', 'is_expression': 0,
                     'python_val_exp': "okc.get('a').get('b').get('c')[0]", 'expect_val_type': '2'},
                    {'rule': '__eq__', 'assert_key': 'message', 'expect_val': 'index', 'is_expression': 1,
                     'python_val_exp': "okc.get('message')", 'expect_val_type': '2'}], 'creator': '调试', 'creator_id': 1,
                 'modifier': None, 'modifier_id': None, 'remark': 'remark'}], 'case_field_ass_info': [
                {'id': 33, 'create_time': '2021-09-11 17:18:10', 'create_timestamp': 1631351884,
                 'update_time': '2021-09-11 17:18:11', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                 'assert_description': 'A通用字段校验', 'ass_json': [
                    {'db_id': 1, 'query': 'select id,case_name FROM ExilicTestPlatform.exile_test_case WHERE id=1;',
                     'assert_list': [{'rule': '__eq__', 'assert_key': 'id', 'expect_val': 1, 'expect_val_type': '1'},
                                     {'rule': '__eq__', 'assert_key': 'case_name', 'expect_val': '测试用例B1',
                                      'expect_val_type': '2'}]}], 'creator': '调试', 'creator_id': 1, 'modifier': None,
                 'modifier_id': None, 'remark': 'remark'}]}
        ]
    }

    demo2 = {
        "bind_info": [
            {
                "case_data_info": {
                    "create_time": "2021-10-03 13:58:54",
                    "create_timestamp": 1633240360,
                    "creator": "调试",
                    "creator_id": 1,
                    "data_name": "index测试数据",
                    "id": 15,
                    "is_deleted": 0,
                    "modifier": None,
                    "modifier_id": None,
                    "remark": None,
                    "request_body": {
                        "Date": "${Date}",
                        "DateTime": "${DateTime}",
                        "Time": "${Time}",
                        "TimeStamp": "${TimeStamp}",
                        "UUID": "${UUID}",
                        "token": "${token}"
                    },
                    "request_body_type": 2,
                    "request_headers": {},
                    "request_params": {},
                    "status": 1,
                    "update_time": "2021-10-03 13:58:55",
                    "update_timestamp": None,
                    "update_var_list": [
                        {
                            "id": 3,
                            "var_name": "变量1",
                            "var_value": "更新",
                            "var_source": "resp_data",
                            "expression": "obj.get('message')",
                            "is_expression": 0,
                            "var_get_key": "code"
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
                                        "expect_val": 1,
                                        "expect_val_type": "1",
                                        "rule": "__eq__"
                                    },
                                    {
                                        "assert_key": "case_name",
                                        "expect_val": "测试用例B1",
                                        "expect_val_type": "2",
                                        "rule": "__eq__"
                                    }
                                ],
                                "db_id": 1,
                                "query": "select id,case_name FROM ExilicTestPlatform.exile_test_case WHERE id=1;"
                            }
                        ],
                        "assert_description": "A通用字段校验",
                        "create_time": "2021-09-11 17:18:10",
                        "create_timestamp": 1631351884,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 33,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-11 17:18:11",
                        "update_timestamp": None
                    }
                ],
                "case_resp_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__ge__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "2",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__eq__"
                            }
                        ],
                        "assert_description": "通用断言9",
                        "create_time": "2021-08-08 17:49:53",
                        "create_timestamp": 1628416141,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 1,
                        "is_deleted": 0,
                        "modifier": "调试",
                        "modifier_id": 1,
                        "remark": "remark123",
                        "status": 1,
                        "update_time": "2021-09-11 17:04:00",
                        "update_timestamp": 1631351018
                    },
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "assert_val": "200",
                                "assert_val_type": "1",
                                "expect_val": "333",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "mesg",
                                "assert_val": "操作成功",
                                "assert_val_type": "2",
                                "expect_val": "aaa",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "code",
                                "assert_val": "200",
                                "assert_val_type": "1",
                                "expect_val": "333",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            }
                        ],
                        "assert_description": "通用断言1",
                        "create_time": "2021-08-09 17:56:02",
                        "create_timestamp": 1628502956,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 2,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-08-09 17:56:02",
                        "update_timestamp": None
                    },
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "assert_val": "200",
                                "assert_val_type": "1",
                                "expect_val": "333",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "mesg",
                                "assert_val": "操作成功",
                                "assert_val_type": "2",
                                "expect_val": "aaa",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "code",
                                "assert_val": "200",
                                "assert_val_type": "1",
                                "expect_val": "333",
                                "is_rule_source": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            }
                        ],
                        "assert_description": "通用断言1",
                        "create_time": "2021-08-09 18:00:26",
                        "create_timestamp": 1628503223,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 3,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-08-09 18:00:26",
                        "update_timestamp": None
                    },
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__ge__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "2",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "2",
                                "is_expression": 1,
                                "python_val_exp": "okc.get('message')",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "yangyuexiongyyx",
                                "expect_val_type": "2",
                                "is_expression": 1,
                                "python_val_exp": "okc.get('data').get('token')",
                                "rule": "__eq__"
                            }
                        ],
                        "assert_description": "Resp通用断言yyx",
                        "create_time": "2021-10-03 14:34:38",
                        "create_timestamp": 1633242718,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 23,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-10-03 14:34:38",
                        "update_timestamp": None
                    }
                ]
            }
        ],
        "case_info": {
            "case_name": "测试index-post",
            "create_time": "2021-10-03 13:53:39",
            "create_timestamp": 1633240360,
            "creator": "调试",
            "creator_id": 1,
            "id": 20,
            "is_deleted": 0,
            "is_pass": 0,
            "is_shared": 0,
            "modifier": None,
            "modifier_id": None,
            "remark": "remark",
            "request_base_url": "http://127.0.0.1:7272",
            "request_method": "POST",
            "request_url": "/api/index",
            "status": 1,
            "total_execution": 6,
            "update_time": "2021-10-03 14:42:09",
            "update_timestamp": 1633243280
        }
    }

    demo3 = {
        "bind_info": [
            {
                "case_data_info": {
                    "create_time": "2021-11-11 10:58:18",
                    "create_timestamp": 1636599498,
                    "creator": "脚本生成:0",
                    "creator_id": 999999,
                    "data_name": "数据okc",
                    "id": 1,
                    "is_deleted": 0,
                    "is_public": 0,
                    "modifier": "user_00001",
                    "modifier_id": 1,
                    "remark": "脚本生成:0",
                    "request_body": {},
                    "request_body_type": 1,
                    "request_headers": {},
                    "request_params": {},
                    "status": 1,
                    "update_time": "2021-11-15 10:13:44",
                    "update_timestamp": 1636941307,
                    "update_var_list": [
                        {
                            "expression": "obj.get('message')",
                            "id": 1,
                            "is_expression": 0,
                            "var_get_key": "message",
                            "var_source": "resp_data",
                            "var_value": "yangyuexiong123"
                        },
                        {
                            "expression": "obj.get('code')",
                            "id": 2,
                            "is_expression": 0,
                            "var_get_key": "code",
                            "var_source": "resp_data",
                            "var_value": "变量的值:1"
                        }
                    ],
                    "var_list": None
                },
                "case_field_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_list": [
                                    {
                                        "assert_key": "id",
                                        "expect_val": 1,
                                        "expect_val_type": "1",
                                        "rule": "__eq__"
                                    },
                                    {
                                        "assert_key": "case_name",
                                        "expect_val": "测试用例B1",
                                        "expect_val_type": "2",
                                        "rule": "__eq__"
                                    }
                                ],
                                "db_id": 1,
                                "query": "select id FROM ExileTestPlatform.exile_test_case WHERE id=1;"
                            }
                        ],
                        "assert_description": "调试用例执行专用field断言",
                        "create_time": "2021-11-11 11:23:23",
                        "create_timestamp": 1636601002,
                        "creator": "脚本生成:0",
                        "creator_id": 999999,
                        "id": 1,
                        "is_deleted": 0,
                        "is_public": 1,
                        "modifier": "user_00001",
                        "modifier_id": 1,
                        "remark": "调试用例执行专用field断言",
                        "status": 1,
                        "update_time": "2021-11-16 11:16:32",
                        "update_timestamp": 1637027887
                    }
                ],
                "case_resp_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "code",
                                "expect_val": 200,
                                "expect_val_type": "1",
                                "is_expression": 1,
                                "python_val_exp": "okc.get('code')",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "2",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('message')",
                                "rule": "__eq__"
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "2",
                                "is_expression": 1,
                                "python_val_exp": "okc.get('message')",
                                "rule": "__eq__"
                            }
                        ],
                        "assert_description": "调试用例执行专用resp断言",
                        "create_time": "2021-11-11 11:23:22",
                        "create_timestamp": 1636601002,
                        "creator": "脚本生成:0",
                        "creator_id": 999999,
                        "id": 1,
                        "is_deleted": 0,
                        "is_public": 1,
                        "modifier": "user_00001",
                        "modifier_id": 1,
                        "remark": "调试用例执行专用resp断言",
                        "status": 1,
                        "update_time": "2021-11-16 11:15:52",
                        "update_timestamp": 1637027887
                    }
                ]
            }
        ],
        "case_info": {
            "case_name": "用于执行-resp断言+field断言",
            "create_time": "2021-11-16 09:55:09",
            "create_timestamp": 1637027526,
            "creator": "user_00001",
            "creator_id": 1,
            "id": 48,
            "is_deleted": 0,
            "is_pass": 0,
            "is_public": 1,
            "is_shared": 1,
            "modifier": "user_00001",
            "modifier_id": 1,
            "remark": "/api/index",
            "request_base_url": "http://0.0.0.0:7272",
            "request_method": "POST",
            "request_url": "/api/index",
            "status": 1,
            "total_execution": 7,
            "update_time": "2021-11-16 11:37:38",
            "update_timestamp": 1637033854
        }
    }

    test_obj = {
        "execute_id": 1,
        "execute_name": "开发者调试",
        "execute_type": "case",
        "execute_user_id": 1,
        "execute_username": "开发者调试",
        "base_url": None,
        "case_list": [demo3],
        "data_driven": False,
        # "sio": sio
    }
    MainTest(test_obj=test_obj).main()
