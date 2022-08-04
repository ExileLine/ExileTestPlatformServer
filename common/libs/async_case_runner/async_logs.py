# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 01:01
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_logs.py
# @Software: PyCharm


case_logs_demo = [
    {
        "case_id": 1,
        "case_name": "yy",
        "logs": {},
        "data_dict": {
            "9": {
                "data_id": 9,
                "data_name": "xx",
                "logs": {
                    "request_before": {
                        "description": "参数前置准备",
                        "logs": []
                    },
                    "url": {
                        "description": "请求地址",
                        "logs": []
                    },
                    "request_headers": {
                        "description": "请求头",
                        "type": None,
                        "logs": []
                    },
                    "request_body": {
                        "description": "请求体",
                        "logs": []
                    },
                    "http_code": {
                        "description": "HTTP响应码",
                        "logs": []
                    },
                    "response_headers": {
                        "description": "响应头",
                        "logs": []
                    },
                    "response_body": {
                        "description": "响应体",
                        "type": None,
                        "logs": []
                    },
                    "request_after": {
                        "description": "参数后置准备",
                        "logs": []
                    }
                }
            }
        }
    }
]


class AsyncDataLogs:
    """异步日志记录(执行参数)"""

    def __init__(self, data_id, data_name):
        self.data_id = data_id
        self.data_name = data_name
        self.logs = {
            "request_before": {
                "description": "参数前置准备",
                "logs": []
            },
            "url": {
                "description": "请求地址",
                "logs": []
            },
            "method": {
                "description": "请求方式",
                "logs": []
            },
            "request_headers": {
                "description": "请求头",
                "type": None,
                "logs": []
            },
            "request_body": {
                "description": "请求体",
                "logs": []
            },
            "http_code": {
                "description": "HTTP响应码",
                "logs": []
            },
            "response_headers": {
                "description": "响应头",
                "logs": []
            },
            "response_body": {
                "description": "响应体",
                "type": None,
                "logs": []
            },
            "request_after": {
                "description": "参数后置准备",
                "logs": []
            }
        }

    async def add_logs(self, key, val):
        """添加日志"""

        if not self.logs.get(key):
            raise KeyError(f"日志分类错误:{key}")

        self.logs[key]['logs'].append(val)

    async def to_json(self):
        """1"""

        result = {
            "data_id": self.data_id,
            "data_name": self.data_name,
            "logs": self.logs
        }
        return result


class AsyncRunnerLogs:
    """异步日志对象"""

    @staticmethod
    async def gen_case_logs(case_id, case_name):
        """
        生成用例日志对象
        :param case_id: 用例id
        :param case_name: 用例名称
        :return:
        """

        result = {
            "case_id": case_id,
            "case_name": case_name,
            "logs": [],
            "data_dict": {}
        }
        return result

    @staticmethod
    async def gen_data_logs(data_id, data_name):
        """
        生成参数日志对象
        :param data_id: 参数id
        :param data_name: 参数名称
        :return:
        """

        return AsyncDataLogs(data_id, data_name)
