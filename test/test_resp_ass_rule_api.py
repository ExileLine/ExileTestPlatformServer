# -*- coding: utf-8 -*-
# @Time    : 2021/8/9 5:40 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_resp_ass_rule_api.py
# @Software: PyCharm

import unittest

from test.test_tools import current_request

url = 'http://0.0.0.0:7272/api/resp_ass_rule'


class TestApi(unittest.TestCase):

    def test_001(self):
        """创建成功"""
        json_data = {
            "assert_description": "通用断言1",
            "remark": "remark",
            "ass_json": [
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "mesg",
                    "assert_val": "操作成功",
                    "assert_val_type": "2",
                    "expect_val": "aaa",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
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
            "assert_description": "通用断言1",
            "remark": "remark",
            "ass_json1": [
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "mesg",
                    "assert_val": "操作成功",
                    "assert_val_type": "2",
                    "expect_val": "aaa",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
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
            "assert_description": "通用断言1",
            "remark": "remark",
            "ass_json": [
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp1": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "mesg",
                    "assert_val": "操作成功",
                    "assert_val_type": "2",
                    "expect_val": "aaa",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                },
                {
                    "assert_key": "code",
                    "assert_val": "200",
                    "assert_val_type": "1",
                    "expect_val": "333",
                    "rule": "=",
                    "is_rule_source": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]"
                }
            ]
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert resp_json.json().get('message') == '检验对象错误'


if __name__ == '__main__':
    unittest.main()
