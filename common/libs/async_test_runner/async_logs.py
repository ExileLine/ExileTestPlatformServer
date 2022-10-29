# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 01:01
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_logs.py
# @Software: PyCharm


log_desc_dict = {
    "request_before": "=== 前置准备 ===",
    "url": "=== 请求地址接口 ===",
    "method": "=== 请求方式 ===",
    "request_headers": "=== 请求头 ===",
    "request_body": "=== 请求体 ===",
    "http_code": "=== HTTP响应码 ===",
    "response_headers": "=== 响应头 ===",
    "response_body": "=== 响应体 ===",
    "response_assert": "=== 响应断言汇总 ===",
    "field_assert": "=== 字段断言汇总 ===",
    "request_after": "=== 后置准备 ===",
    "update_variable": "=== 更新变量 ==="
}


class AsyncDataLogs:
    """异步日志记录(执行参数)"""

    def __init__(self, data_id, data_name):
        self.data_id = data_id
        self.data_name = data_name
        self.logs = {
            "request_before": {
                "description": "参数前置准备",
                "logs": [],
                "flag": True
            },
            "url": {
                "description": "请求地址",
                "logs": [],
                "flag": True
            },
            "method": {
                "description": "请求方式",
                "logs": [],
                "flag": True
            },
            "request_headers": {
                "description": "请求头",
                "type": None,
                "logs": [],
                "flag": True
            },
            "request_body": {
                "description": "请求体",
                "logs": [],
                "flag": True
            },
            "http_code": {
                "description": "HTTP响应码",
                "logs": [],
                "flag": True
            },
            "response_headers": {
                "description": "响应头",
                "logs": [],
                "flag": True
            },
            "response_body": {
                "description": "响应体",
                "type": None,
                "logs": [],
                "flag": True
            },
            "response_assert": {
                "description": "响应断言",
                "logs": [],
                "flag": True
            },
            "field_assert": {
                "description": "字段断言",
                "logs": [],
                "flag": True
            },
            "request_after": {
                "description": "参数后置准备",
                "logs": [],
                "flag": True
            },
            "update_variable": {
                "description": "更新变量记录",
                "logs": [],
                "flag": True
            }
        }
        self.flag = True
        self.logs_summary = []

    async def set_flag(self, flag: bool):
        """
        设置参数标识(通过/失败)
        :param flag:
        :return:
        """
        if self.flag:
            self.flag = flag

    async def add_logs(self, key, val, flag=True):
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
        if self.logs[key].get('flag'):
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
    """异步执行日志"""

    def __init__(self):
        self.case_logs_dict = {}  # 用例日志字典
        self.scenario_logs_dict = {}  # 场景日志字典

    async def gen_case_logs_dict(self, case_list):
        """
        生成用例日志字典模型
        :param case_list: 用例列表
        :return:
        """

        for case in case_list:
            case_uuid = case.get('uuid')
            case_id = case.get('case_info').get('id')
            case_name = case.get('case_info').get('case_name')
            d = {
                "case_uuid": case_uuid,
                "case_id": case_id,
                "case_name": case_name,
                "logs": [],
                "flag": True,
                "data_dict": {}
            }
            self.case_logs_dict[case_uuid] = d

    async def gen_scenario_logs_dict(self, scenario_list):
        """
        生成场景日志字典模型
        :param scenario_list: 场景列表
        :return:
        """

        for scenario in scenario_list:
            scenario_uuid = scenario.get('uuid')
            scenario_id = scenario.get('id')
            scenario_title = scenario.get('scenario_title')
            case_list = scenario.get('case_list')
            d = {
                "scenario_uuid": scenario_uuid,
                "id": scenario_id,
                "scenario_title": scenario_title,
                "logs": [],
                "flag": True,
                "case_dict": {}
            }
            for case in case_list:
                case_uuid = case.get('uuid')
                case_id = case.get('case_info').get('id')
                case_name = case.get('case_info').get('case_name')
                case_dict = {
                    "case_uuid": case_uuid,
                    "case_id": case_id,
                    "case_name": case_name,
                    "logs": [],
                    "flag": True,
                    "data_dict": {}
                }
                d['case_dict'][case_uuid] = case_dict

            self.scenario_logs_dict[scenario_uuid] = d

    async def add_case_logs(self, case_uuid, logs):
        """
        增加用例日志
        :param case_uuid: 用例uuid
        :param logs: 日志内容
        :return:
        """
        self.case_logs_dict.get(case_uuid)['logs'].append(logs)

    async def add_scenario_logs(self, scenario_uuid, logs):
        """
        增加用例日志
        :param scenario_uuid: 场景uuid
        :param logs: 日志内容
        :return:
        """
        self.scenario_logs_dict.get(scenario_uuid)['logs'].append(logs)

    async def add_case_data_logs(self, case_uuid, data_id, logs):
        """
        增加用例中执行参数日志
        :param case_uuid: 用例uuid
        :param data_id: 参数id
        :param logs: 日志内容
        :return:
        """
        self.case_logs_dict.get(case_uuid).get('data_dict')[data_id] = logs

    async def add_scenario_case_data_logs(self, scenario_uuid, case_uuid, data_id, logs):
        """
        增加场景用例执行参数日志
        :param scenario_uuid: 场景uuid
        :param case_uuid: 用例uuid
        :param data_id: 参数id
        :param logs: 日志内容
        :return:
        """
        self.scenario_logs_dict.get(scenario_uuid).get('case_dict').get(case_uuid).get('data_dict')[data_id] = logs

    async def set_case_flag(self, case_uuid, flag: bool):
        """
        设置用例标识(通过/失败)
        :param case_uuid: 用例uuid
        :param flag: True/False
        :return:
        """

        if self.case_logs_dict.get(case_uuid).get('flag'):
            self.case_logs_dict.get(case_uuid)['flag'] = flag

    async def set_scenario_flag(self, scenario_uuid, case_uuid, flag: bool):
        """
        设置场景标识(通过/失败)
        :param scenario_uuid: 场景uuid
        :param case_uuid: 场景里面用例的uuid
        :param flag: True/False
        :return:
        """

        if self.scenario_logs_dict.get(scenario_uuid).get('flag'):
            self.scenario_logs_dict.get(scenario_uuid)['flag'] = flag

        if self.scenario_logs_dict.get(scenario_uuid).get('case_dict').get(case_uuid).get('flag'):
            self.scenario_logs_dict.get(scenario_uuid).get('case_dict').get(case_uuid)['flag'] = flag

    async def set_flag(self, logs_type, flag: bool, case_uuid=None, scenario_uuid=None):
        """
        设置用例/场景(通过/失败)
        :param logs_type: 类型(case;scenario)
        :param case_uuid:
        :param scenario_uuid:
        :param flag:
        :return:
        """

        if logs_type == 'case':
            await self.set_case_flag(case_uuid=case_uuid, flag=flag)
        elif logs_type == 'scenario':
            await self.set_scenario_flag(scenario_uuid=scenario_uuid, case_uuid=case_uuid, flag=flag)
        else:
            raise TypeError(f'错误logs_type:{logs_type}')
