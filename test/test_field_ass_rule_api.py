# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 5:40 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_field_ass_rule_api.py
# @Software: PyCharm

import unittest

from test.test_tools import current_request

url = 'http://0.0.0.0:7272/api/field_ass_rule'


class TestApi(unittest.TestCase):

    def test_001(self):
        """创建成功"""
        json_data = {
            "assert_description": "字段校验规则999",
            "remark": "remark",
            "ass_json": [
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        },
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                },
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                }
            ]
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert resp_json.json().get('message') == '创建成功'

    def test_002(self):
        """缺少必须的key"""
        json_data = {
            "assert_description": "字段校验规则999",
            "remark": "remark",
            "ass_json1": [
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        },
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                },
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                }
            ]
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert resp_json.json().get('message') == 'CustomException:【参数类型错误】'

    def test_003(self):
        """检验对象必须的key"""
        json_data = {
            "assert_description": "字段校验规则999",
            "remark": "remark",
            "ass_json": [
                {
                    "db_name1": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        },
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                },
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                }
            ]
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert resp_json.json().get('message') == 'ass_json 参数错误'

    def test_004(self):
        """检验query的对象"""
        json_data = {
            "assert_description": "字段校验规则999",
            "remark": "remark",
            "ass_json": [
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name1": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        },
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                },
                {
                    "db_name": "online",
                    "table_name": "ol_user",
                    "query": [
                        {
                            "field_name": "id",
                            "field_key": "1",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        },
                        {
                            "field_name": "name",
                            "field_key": "yyx",
                            "query_rule": "=",
                            "is_sql": "1",
                            "sql": "SELECT * FROM ol_user WHERE id=1;"
                        }
                    ],
                    "assert_list": [
                        {
                            "assert_key": "id",
                            "assert_val": "1",
                            "assert_val_type": "1",
                            "rule": "="
                        }
                    ]
                }
            ]
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert 'query对象key错误' in resp_json.json().get('message')


if __name__ == '__main__':
    unittest.main()
