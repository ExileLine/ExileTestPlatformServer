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
from common.libs.public_func import json_format


class CaseDrivenResult:
    """
    main
    1.组装用例
    2.转换参数
    3.发出请求
    4.断言
    5.更新变量
    6.日志记录
    7.生成报告
    """

    def __init__(self, case):
        self.case = case
        self.case_info = self.case.get('case_info', {})
        self.bind_info = self.case.get('bind_info', [])

        self.case_name = self.case_info.get('case_name')
        self.request_url = self.case_info.get('request_url')
        self.request_method = self.case_info.get('request_method')

    @staticmethod
    def show_log(url, headers, req_json, resp_headers, resp_json):
        """测试用例日志打印"""
        logger.info('test url\n{}'.format(url))
        logger.info('test headers\n{}'.format(json_format(headers)))
        logger.info('test req_json\n{}'.format(json_format(req_json)))
        logger.info('test resp_headers\n{}'.format(json_format(resp_headers)))
        logger.info('test resp_json\n{}'.format(json_format(resp_json)))

    @staticmethod
    def var_conversion(before_var):
        """变量转换参数"""

        before_var_init = before_var
        if isinstance(before_var_init, (list, dict)):
            before_var = json.dumps(before_var, ensure_ascii=False)

        result_list = re.findall('\\$\\{([^}]*)', before_var)

        if result_list:
            current_dict = {}
            for res in result_list:
                sql = """select var_value from exilic_test_variable where var_name='{}';""".format(res)
                query_result = project_db.select(sql=sql, only=True)
                if query_result:
                    current_dict[res] = json.loads(query_result.get('var_value'))
            if current_dict:
                current_str = before_var
                for k, v in current_dict.items():
                    old_var = "${%s}" % (k)
                    new_var = v
                    current_str = current_str.replace(old_var, new_var)
                if isinstance(before_var_init, (list, dict)):
                    current_str = json.loads(current_str)
                    print('okc')
                # print(current_str)
                return current_str
            else:
                return None
        else:
            return None

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

    def main(self):
        """main"""

        if self.bind_info:

            for bind in self.bind_info:
                case_data_info = bind.get('case_data_info', {})
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                req_type_dict = {
                    "1": {"data": case_data_info.get('request_body')},
                    "2": {"json": case_data_info.get('request_body')},
                    "3": {"data": case_data_info.get('request_body')}
                }

                send = {
                    "url": self.request_url,  # TODO 有 base url 拼接
                    "headers": case_data_info.get('request_headers'),

                }

                go = req_type_dict.get(str(case_data_info.get('request_body_type')))
                send.update(go)

                send = self.var_conversion(send)

                resp = self.current_request(method=self.request_method.lower(), **send)
                print(resp.json())
        else:
            pass


if __name__ == '__main__':
    ddd = {
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
                    "request_body": {"key": "${user_id}"},
                    "request_body_type": 1,
                    "request_headers": {"key": "${user_id}"},
                    "request_params": {"key": "${user_id}"},
                    "status": 1,
                    "update_time": "2021-09-01 20:34:40",
                    "update_timestamp": None,
                    "var_list": [
                        "user_id",
                        "username"
                    ],
                    "update_var_list": [
                        {"3": "更新"}
                    ],
                },
                "case_field_ass_info": [],
                "case_resp_ass_info": [
                    {
                        "ass_json": [
                            {
                                "assert_key": "code",
                                "expect_val": "200",
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            },
                            {
                                "assert_key": "message",
                                "expect_val": "index",
                                "expect_val_type": "1",
                                "is_expression": 0,
                                "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                                "rule": "="
                            }
                        ],
                        "assert_description": "Resp通用断言",
                        "create_time": "2021-09-01 20:30:04",
                        "create_timestamp": 1630499057,
                        "creator": "调试",
                        "creator_id": 1,
                        "id": 10,
                        "is_deleted": 0,
                        "modifier": None,
                        "modifier_id": None,
                        "remark": "remark",
                        "status": 1,
                        "update_time": "2021-09-01 20:30:05",
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

    cdr = CaseDrivenResult(case=ddd)
    cdr.main()
