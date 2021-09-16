# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:19 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CaseDrivenResult.py
# @Software: PyCharm

import re
import json
import requests

from loguru import logger

from common.libs.db import project_db
from common.libs.public_func import check_keys
from common.libs.public_func import json_format
from common.libs.assert_related import AssertMain


# TODO 需要重构

class TestLoader:
    """测试用例加载"""

    def __init__(self):
        pass


class TestExecute:
    """测试执行"""

    def __init__(self):
        pass


class TestResult:
    """测试结果"""

    def __init__(self):
        pass


class CaseDrivenResult:
    """
    main
    1.组装用例:
        CaseDrivenResult.__init__ √

    2.转换参数:
        CaseDrivenResult.var_conversion √

    3.发出请求:
        CaseDrivenResult.assemble_data_send √
        CaseDrivenResult.current_request √

    4.resp断言前置检查:
        CaseDrivenResult.resp_check_ass_execute √
        CaseDrivenResult.check_resp_ass_keys √

    5.resp断言执行:
        CaseDrivenResult.resp_check_ass_execute √
        CaseDrivenResult.execute_resp_ass -> AssertMain.assert_resp_main √

    6.更新变量:
        CaseDrivenResult.update_var √

    7.field断言前置检查:
        CaseDrivenResult.field_check_ass_execute √
        CaseDrivenResult.check_field_ass_keys √

    8.field断言执行:
        CaseDrivenResult.field_check_ass_execute √
        CaseDrivenResult.execute_field_ass -> AssertMain.assert_field_main √

    7.日志记录:

    8.生成报告:

    """

    # TODO field 前置查询 {"before_query":"select xxx from xxx....","before_field":"username"}
    # TODO
    #  "case_list":[],
    #  "data_driven": False

    def __init__(self, case):
        self.case = case
        self.case_info = self.case.get('case_info', {})
        self.bind_info = self.case.get('bind_info', [])

        self.base_url = self.case_info.get('base_url')
        self.case_name = self.case_info.get('case_name')
        self.request_url = self.case_info.get('request_url')
        self.request_method = self.case_info.get('request_method')
        self.update_var_list = []

        self.resp_json = {}
        self.resp_headers = {}

        self.resp_ass_count = 0
        self.resp_ass_success = 0
        self.resp_ass_fail = 0
        self.resp_ass_success_rate = 0
        self.resp_ass_fail_rate = 0

        self.field_ass_count = 0
        self.field_ass_success = 0
        self.field_ass_fail = 0
        self.field_ass_success_rate = 0
        self.field_ass_fail_rate = 0

    def assemble_data_send(self, case_data_info):
        """
        组装数据发送并且更新变量
        :return:
        """
        request_body = case_data_info.get('request_body')
        request_headers = case_data_info.get('request_headers')
        request_body_type = str(case_data_info.get('request_body_type'))
        self.update_var_list = case_data_info.get('update_var_list')

        req_type_dict = {
            "1": {"data": request_body},
            "2": {"json": request_body},
            "3": {"data": request_body}
        }

        url = self.base_url + self.request_url if self.base_url else self.request_url

        before_send = {
            "url": url,
            "headers": request_headers,
        }
        req_json_data = req_type_dict.get(request_body_type)
        before_send.update(req_json_data)

        send = self.var_conversion(before_send)

        resp = self.current_request(method=self.request_method.lower(), **send)
        self.resp_json = resp.json()
        self.resp_headers = resp.headers
        json_format(self.resp_json, '用例:{} -> resp_json'.format(self.case_name))
        json_format(self.resp_headers, '用例:{} -> resp_headers'.format(self.case_name))

    def resp_check_ass_execute(self, case_resp_ass_info):
        """
        检查 resp 断言规则并执行断言
        :return:
        """
        if case_resp_ass_info:
            for resp_ass in case_resp_ass_info:  # 遍历断言规则逐一校验
                resp_ass_list = resp_ass.get('ass_json')
                assert_description = resp_ass.get('assert_description')
                # print(resp_ass_list)
                if self.check_resp_ass_keys(assert_list=resp_ass_list):  # 响应检验
                    self.resp_ass_count = len(resp_ass_list)
                    self.execute_resp_ass(resp_ass_list=resp_ass_list, assert_description=assert_description)
                else:
                    logger.error('=== check_ass_keys error ===')
                    return False
        else:
            logger.info('=== case_resp_ass_info is [] ===')
            return False

    def field_check_ass_execute(self, case_field_ass_info):
        """
        检查 field 断言规则并执行断言
        :return:
        """
        if self.resp_ass_fail == 0:  # 所有断言规则通过
            self.update_var()  # 更新变量
            for field_ass in case_field_ass_info:
                field_ass_list = field_ass.get('ass_json')
                assert_description = field_ass.get('assert_description')
                # print(field_ass_list)
                if self.check_field_ass_keys(assert_list=field_ass_list):  # 数据库校验
                    for field_ass_child in field_ass_list:
                        assert_list = field_ass_child.get('assert_list')
                        self.field_ass_count = len(assert_list)
                    self.execute_field_ass(
                        field_ass_list=field_ass_list,
                        assert_description=assert_description
                    )
                else:
                    return False

        else:
            logger.info('=== 断言规则没有100%通过,不更新变量以及不进行数据库校验 ===')

    @staticmethod
    def show_log(url, headers, req_json, resp_headers, resp_json):
        """测试用例日志打印"""
        logger.info('test url\n{}'.format(url))
        json_format(headers, msg='test headers')
        json_format(req_json, msg='test req_json')
        json_format(resp_headers, msg='test resp_headers')
        json_format(resp_json, msg='test resp_json')

    @staticmethod
    def var_conversion(before_var):
        """变量转换参数"""

        before_var_init = before_var
        if isinstance(before_var_init, (list, dict)):
            before_var = json.dumps(before_var, ensure_ascii=False)

        result_list = re.findall('\\$\\{([^}]*)', before_var)

        if result_list:
            err_var_list = []
            current_dict = {}
            for res in result_list:
                sql = """select var_value from exilic_test_variable where var_name='{}';""".format(res)
                query_result = project_db.select(sql=sql, only=True)
                if query_result:
                    current_dict[res] = json.loads(query_result.get('var_value'))
                else:
                    err_var_list.append(res)
            if current_dict:
                current_str = before_var
                for k, v in current_dict.items():
                    old_var = "${%s}" % (k)
                    new_var = v
                    current_str = current_str.replace(old_var, new_var)
                if isinstance(before_var_init, (list, dict)):
                    current_str = json.loads(current_str)
                # print(current_str)
                return current_str
            else:
                logger.info('===未找到变量:{}对应的参数==='.format(err_var_list))
                return before_var_init
        else:
            return before_var_init

    @staticmethod
    def check_resp_ass_keys(assert_list):
        """
        检查resp断言对象参数类型是否正确
        assert_list: ->list 规则列表
        """

        cl = ["assert_key", "expect_val", "expect_val_type", "is_expression", "python_val_exp", "rule"]

        if not isinstance(assert_list, list) or not assert_list:
            logger.info("assert_list:类型错误{}".format(assert_list))
            return False

        for ass in assert_list:
            if not check_keys(ass, *cl):
                logger.error("缺少需要的键值对:{}".format(ass))
                return False
        return True

    @staticmethod
    def check_field_ass_keys(assert_list):
        """
        检查field断言对象参数类型是否正确
        assert_list: ->list 规则列表
        """

        cl = ["assert_key", "expect_val", "expect_val_type", "rule"]

        if not isinstance(assert_list, list) or not assert_list:
            logger.info("assert_list:类型错误{}".format(assert_list))
            return False

        for ass in assert_list:
            child_assert_list = ass.get('assert_list')
            for ass_child in child_assert_list:
                if not check_keys(ass_child, *cl):
                    logger.error("缺少需要的键值对:{}".format(ass))
                    return False
        return True

    @classmethod
    def current_request(cls, method=None, **kwargs):
        """
        构造请求
        :param method: 请求方式
        :param kwargs: 请求体以及扩展参数
        :return:
        """

        if hasattr(requests, method):
            response = getattr(requests, method)(**kwargs, verify=False)
            cls.current_resp_json = response.json()
            cls.current_resp_headers = response.headers
            cls.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=cls.current_resp_json,
                resp_headers=cls.current_resp_headers
            )
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            cls.current_resp_json = response
            cls.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=cls.current_resp_json,
                resp_headers={}
            )
        return response

    def execute_resp_ass(self, resp_ass_list, assert_description):
        """
        执行Resp断言
        resp_ass_list demo
            [
                {
                    "assert_key": "code",
                    "expect_val": "200",
                    "expect_val_type": "1",
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                },
                {
                    "assert_key": "message",
                    "expect_val": "index",
                    "expect_val_type": "1",
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                }
            ]
        """
        for resp_ass_dict in resp_ass_list:
            # print(resp_ass_dict)
            new_resp_ass = AssertMain(
                resp_json=self.resp_json,
                resp_headers=self.resp_headers,
                assert_description=assert_description,
                **resp_ass_dict
            )
            resp_ass_result = new_resp_ass.assert_resp_main()
            # print(resp_ass_result)
            if resp_ass_result.get('status'):  # [bool,str]
                self.resp_ass_success += 1
            else:
                self.resp_ass_fail += 1

    def execute_field_ass(self, field_ass_list, assert_description):
        """
        执行Field断言
        """

        for field_ass_dict in field_ass_list:
            # print(field_ass_dict)
            new_field_ass = AssertMain(
                assert_description=assert_description,
                **field_ass_dict
            )

            field_ass_result = new_field_ass.assert_field_main()

            self.field_ass_success += field_ass_result.get('success')
            self.field_ass_fail += field_ass_result.get('fail')

    def update_var(self):
        """更新变量"""
        if self.update_var_list:
            for up in self.update_var_list:
                current_list = [item for item in up.items()][0]
                id = current_list[0]
                var_value = current_list[1]
                sql = """UPDATE exilic_test_variable SET var_value='{}' WHERE id='{}';""".format(
                    json.dumps(var_value, ensure_ascii=False), id)
                logger.success('=== update sql === 【 {} 】'.format(sql))
                project_db.update_data(sql)
        else:
            logger.info('=== 更新变量列表为空不需要更新变量===')

    def go_test(self):
        """调试"""
        print(self.resp_ass_count)
        print(self.resp_ass_success)
        print(self.resp_ass_fail)
        print(self.update_var_list)

        print(self.resp_ass_count)
        print(self.resp_ass_success)
        print(self.resp_ass_fail)

        print(self.field_ass_count)
        print(self.field_ass_success)
        print(self.field_ass_fail)

    def main(self):
        """main"""

        if self.bind_info:

            for bind in self.bind_info:
                case_data_info = bind.get('case_data_info', {})
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                self.assemble_data_send(case_data_info=case_data_info)

                self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

        else:
            logger.info('=== 未配置请求参数 ===')


if __name__ == '__main__':
    demo = {
        "bind_info": [
            {
                "case_data_info": {
                    "create_time": "2021-09-01 20:34:39",
                    "create_timestamp": 1630499057,
                    "creator": "调试",
                    "creator_id": 1,
                    "data_name": "数据99999",
                    "id": 12,
                    "is_deleted": 0,
                    "modifier": None,
                    "modifier_id": None,
                    "remark": None,
                    "request_body": {},
                    "request_body_type": 1,
                    "request_headers": {},
                    "request_params": {},
                    "status": 1,
                    "update_time": "2021-09-01 20:34:40",
                    "update_timestamp": None,
                    "update_var_list": [
                        {
                            "3": "更新"
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
                                "query": "select id,case_name FROM ExilicTestPlatform.exilic_test_case WHERE id=1;"
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
                        "assert_description": "Resp通用断言123",
                        "create_time": "2021-09-13 12:49:07",
                        "create_timestamp": 1631508310,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 21,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-13 12:49:08",
                        "update_timestamp": None
                    }
                ]
            }
        ],
        "case_info": {
            "case_name": "测试indexApi",
            "create_time": "2021-09-01 20:27:32",
            "create_timestamp": 1630499057,
            "creator": "调试",
            "creator_id": 1,
            "id": 14,
            "is_deleted": 0,
            "modifier": None,
            "modifier_id": None,
            "remark": "remark",
            "request_method": "GET",
            "request_url": "http://127.0.0.1:7272/api",
            "status": 1,
            "update_time": "2021-09-01 20:27:32",
            "update_timestamp": None
        }
    }
    demo1 = {
        'case_info': {'id': 14, 'create_time': '2021-09-01 20:27:32', 'create_timestamp': 1630499057,
                      'update_time': '2021-09-01 20:27:32', 'update_timestamp': None, 'is_deleted': 0, 'status': 1,
                      'case_name': '测试indexApi', 'request_method': 'GET',
                      'request_url': 'http://127.0.0.1:7272/api', 'creator': '调试', 'creator_id': 1,
                      'modifier': None, 'modifier_id': None, 'remark': 'remark'}, 'bind_info': [{'case_data_info': {
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
                {'db_id': 1, 'query': 'select id,case_name FROM ExilicTestPlatform.exilic_test_case WHERE id=1;',
                 'assert_list': [{'rule': '__eq__', 'assert_key': 'id', 'expect_val': 1, 'expect_val_type': '1'},
                                 {'rule': '__eq__', 'assert_key': 'case_name', 'expect_val': '测试用例B1',
                                  'expect_val_type': '2'}]}], 'creator': '调试', 'creator_id': 1, 'modifier': None,
             'modifier_id': None, 'remark': 'remark'}]}]}
    cdr = CaseDrivenResult(case=demo1)
    print(type(cdr))
    # cdr.main()
    # cdr.go_test()
