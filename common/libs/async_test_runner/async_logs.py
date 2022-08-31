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
        "logs": [],
        "fail": True,  # bool
        "data_dict": {
            "9": {
                "data_id": 9,
                "data_name": "xx",
                "fail": True,  # bool
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
                    },
                    "response_assert": {
                        "description": '响应断言',
                        "fail": True,  # bool
                        "logs": [
                            '=== 公式取值结果: 200 ===',
                            '=== 断言:1-123-第一个 ===',
                            "=== 键值:{'code': 200} ===",
                            "function: <class 'int'>",
                            "200:<class 'int'> [==] 200:int",
                            '=== Response 断言通过 ===',
                            '=== 取值结果: 200 ===',
                            '=== 断言:1-123-第一个 ===',
                            "=== 键值:{'code': 200} ===",
                            "function: <class 'int'>",
                            "200:<class 'int'> [==] 200:int",
                            '=== Response 断言通过 ===',
                        ],
                    },
                    "field_assert": {
                        "description": '字段断言',
                        "fail": True,  # bool
                        "logs": ["=== case_resp_ass_info ===\n[{'field_ass': '1'}]\n1-123-第一个"],
                    },
                },
                "logs_summary": ['=== 日志1 ===', '=== 日志2 ===', '=== ... ==='],
            }
        }
    }
]

log_desc_dict = {
    "request_before": "=== 前置准备 ===",
    "url": "=== 请求地址接口 ===",
    "method": "=== 请求方式 ===",
    "request_headers": "=== 请求头 ===",
    "request_body": "=== 请求体 ===",
    "http_code": "=== HTTP响应码 ===",
    "response_headers": "=== 响应头 ===",
    "response_body": "=== 响应体 ===",
    "request_after": "=== 后置准备 ===",
    "response_assert": "=== 响应断言汇总 ===",
    "field_assert": "=== 字段断言汇总 ==="
}


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
            },
            "response_assert": {
                "description": "响应断言",
                "logs": []
            },
            "field_assert": {
                "description": "字段断言",
                "logs": []
            }
        }
        self.flag = None
        self.logs_summary = []

    async def set_flag(self, flag: bool):
        """
        设置参数标识(通过/失败)
        :param flag:
        :return:
        """
        self.flag = flag

    async def add_logs(self, key, val, flag=None):
        """
        添加日志
        :param key: 日志分类标识
        :param val: 日志内容
        :param flag: 断言标识,存在失败则为False否则为True
        :return:
        """

        if not self.logs.get(key):
            raise KeyError(f"日志分类错误:{key}")

        self.logs[key]['logs'].append(val)
        self.logs[key]['flag'] = flag

        log_desc = log_desc_dict.get(key)
        if log_desc not in self.logs_summary:
            self.logs_summary.append(log_desc)
        self.logs_summary.append(val)

    async def to_json(self):
        """输入日志"""

        result = {
            "data_id": self.data_id,
            "data_name": self.data_name,
            "logs": self.logs,
            "flag": self.flag,
            "logs_summary": self.logs_summary
        }
        return result


class AsyncLogs:
    """异步日志"""

    def __init__(self):
        self.case_logs_dict = {}  # 用例日志字典
        self.scenario_logs_dict = {}  # 场景日志字典
        self.scenario_case_dict = {}  # 场景中的用例日志字典
        self.flag_dict = {
            "case": self.set_case_flag,
            "scenario": self.set_scenario_flag
        }

    async def gen_case_logs_dict(self, case_list, is_scenario=False):
        """
        生成用例日志字典模型
        :param case_list: 用例列表
        :param is_scenario: 是否场景中的用例
        :return:
        """

        for case in case_list:
            case_id = case.get('case_info').get('id')
            case_name = case.get('case_info').get('case_name')
            d = {
                "case_id": case_id,
                "case_name": case_name,
                "logs": [],
                "flag": None,
                "data_dict": {}
            }
            if is_scenario:
                self.scenario_case_dict[case_id] = d
            else:
                self.case_logs_dict[case_id] = d

    async def gen_scenario_logs_dict(self, scenario_list):
        """
        生成场景日志字典模型
        :param scenario_list: 场景列表
        :return:
        """
        for scenario in scenario_list:
            scenario_id = scenario.get('id')
            scenario_title = scenario.get('scenario_title')
            case_list = scenario.get('case_list')
            await self.gen_case_logs_dict(case_list=case_list, is_scenario=True)
            d = {
                "scenario_id": scenario_id,
                "scenario_title": scenario_title,
                "logs": [],
                "flag": None,
                "case_dict": self.scenario_case_dict
            }
            self.scenario_logs_dict[scenario_id] = d

    async def add_case_logs(self, case_id, logs):
        """
        增加用例日志
        :param case_id: 用例id
        :param logs: 日志内容
        :return:
        """
        self.case_logs_dict.get(case_id)['logs'].append(logs)

    async def add_scenario_logs(self, scenario_id, logs):
        """
        增加用例日志
        :param scenario_id: 场景id
        :param logs: 日志内容
        :return:
        """
        self.scenario_logs_dict.get(scenario_id)['logs'].append(logs)

    async def add_case_data_logs(self, case_id, data_id, logs):
        """
        增加用例中执行参数日志
        :param case_id: 用例id
        :param data_id: 参数id
        :param logs: 日志内容
        :return:
        """
        self.case_logs_dict.get(case_id).get('data_dict')[data_id] = logs

    async def add_scenario_case_data_logs(self, scenario_id, case_id, data_id, logs):
        """
        增加场景用例执行参数日志
        :param scenario_id: 场景id
        :param case_id: 用例id
        :param data_id: 参数id
        :param logs: 日志内容
        :return:
        """
        self.scenario_logs_dict.get(scenario_id).get('case_dict').get(case_id).get('data_dict')[data_id] = logs

    async def set_case_flag(self, case_id, flag: bool):
        """
        设置用例标识(通过/失败)
        :param case_id: 用例id
        :param flag: True/False
        :return:
        """
        self.case_logs_dict.get(case_id)['flag'] = flag

    async def set_scenario_flag(self, scenario_id, flag: bool):
        """
        设置场景标识(通过/失败)
        :param scenario_id: 场景id
        :param flag: True/False
        :return:
        """
        self.scenario_logs_dict.get(scenario_id)['flag'] = flag

    @staticmethod
    async def gen_data_logs_obj(data_id, data_name):
        """
        生成参数日志对象
        :param data_id: 参数id
        :param data_name: 参数名称
        :return:
        """

        return AsyncDataLogs(data_id, data_name)

    async def main(self):
        """main"""
        return
