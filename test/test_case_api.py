# -*- coding: utf-8 -*-
# @Time    : 2021/8/10 6:27 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_case_api.py
# @Software: PyCharm

import time
import unittest

from test.test_tools import current_request

url = 'http://0.0.0.0:7272/api/case'


class TestPostApi(unittest.TestCase):

    def test_001(self):
        """创建成功"""
        json_data = {
            "case_name": "测试用例:{}".format(int(time.time())),
            "request_method": "Get",
            "request_url": "www.baidu.com",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert '创建成功' in resp_json.json().get('message')

    def test_002(self):
        """用例已经存在"""
        json_data = {
            "case_name": "测试用例123456",
            "request_method": "Get",
            "request_url": "www.baidu.com",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert '已经存在' in resp_json.json().get('message')

    def test_003(self):
        """请求方式错误"""
        json_data = {
            "case_name": "测试用例123456",
            "request_method": "Get123",
            "request_url": "www.baidu.com",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert '不存在' in resp_json.json().get('message')

    def test_004(self):
        """变量不存在"""
        json_data = {
            "case_name": "测试用例123456",
            "request_method": "get",
            "request_url": "www.baidu.com",
            "var_list": ["abc"],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='post', **send)
        assert '请先创建创建' in resp_json.json().get('message')


class TestPutApi(unittest.TestCase):

    def test_001(self):
        """编辑成功(用例名称不变)"""
        json_data = {
            "case_id": 1,
            "case_name": "测试用例B1",
            "request_method": "Get",
            "request_url": "www.baidu.com/yyx/okc",
            "request_params": "request_params",
            "request_headers": "request_headers",
            "request_body": "request_body",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='put', **send)
        assert '编辑成功' in resp_json.json().get('message')

    def test_002(self):
        """编辑成功(用例名称已经存在)"""
        json_data = {
            "case_id": 1,
            "case_name": "测试用例1234567",
            "request_method": "Get",
            "request_url": "www.baidu.com/yyx/okc",
            "request_params": "request_params",
            "request_headers": "request_headers",
            "request_body": "request_body",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='put', **send)
        assert '用例名称:{} 已经存在'.format(json_data.get('case_name')) in resp_json.json().get('message')

    def test_003(self):
        """编辑成功(用例不存在)"""
        json_data = {
            "case_id": 999999999,
            "case_name": "测试用例1234567",
            "request_method": "Get",
            "request_url": "www.baidu.com/yyx/okc",
            "request_params": "request_params",
            "request_headers": "request_headers",
            "request_body": "request_body",
            "var_list": [],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='put', **send)
        assert resp_json.json().get('message') == '用例id:{}数据不存在'.format(json_data.get('case_id'))

    def test_004(self):
        """编辑成功(变量不存在)"""
        json_data = {
            "case_id": 1,
            "case_name": "测试用例1234567",
            "request_method": "Get",
            "request_url": "www.baidu.com/yyx/okc",
            "request_params": "request_params",
            "request_headers": "request_headers",
            "request_body": "request_body",
            "var_list": ["杨跃雄"],
            "remark": "remark"
        }
        send = {
            "url": url,
            "headers": {},
            "json": json_data
        }
        resp_json = current_request(method='put', **send)
        assert resp_json.json().get('message') == '应用的变量:{}不存在,请先创建创建'.format(json_data.get('var_list'))


if __name__ == '__main__':
    unittest.main()
