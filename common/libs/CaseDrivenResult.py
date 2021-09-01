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

    current_url = ""
    current_headers = {}
    current_req_json = {}
    current_resp_headers = {}
    current_resp_json = {}

    def __init__(self, case):
        pass
        # self.case_name = case_name
        # self.request_url = request_url
        # self.request_method = request_method

    @classmethod
    def show_log(cls):
        """测试用例日志打印"""
        logger.info('test url\n{}'.format(cls.current_url))
        logger.info('test headers\n{}'.format(cls.current_headers))
        logger.info('test req_json\n{}'.format(cls.current_req_json))
        logger.info('test resp_headers\n{}'.format(cls.current_resp_headers))
        logger.info('test resp_json\n{}'.format(cls.current_resp_json))

    @staticmethod
    def var_conversion(before_var):
        """变量转换参数"""

        if isinstance(before_var, (list, dict)):
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
                if isinstance(before_var, (list, dict)):
                    current_str = json.loads(current_str)
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
            cls.show_log()
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            cls.current_resp_json = response
            cls.show_log()
        return response
