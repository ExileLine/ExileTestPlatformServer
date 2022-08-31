# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 13:18
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : async_runner.py
# @Software: PyCharm

import re
import json
import time
import aiohttp
import asyncio

from common.libs.db import project_db
from common.libs.data_dict import GlobalsDict
from common.libs.StringIOLog import StringIOLog
from common.libs.async_test_runner.async_assertion import AsyncAssertionResponse, AsyncAssertionField
from common.libs.async_test_runner.async_logs import AsyncLogs
from common.libs.async_test_runner.async_result import AsyncTestResult

value_type_dict = GlobalsDict.value_type_dict()
variable_type_dict = GlobalsDict.variable_type_dict(merge=False)


class AsyncCaseRunner:
    """
    异步用例执行
    """

    def __init__(self, test_obj=None):

        self.test_obj = test_obj if test_obj else {}
        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.data_driven = test_obj.get('data_driven')

        self.case_list = test_obj.get('case_list')  # 执行用例列表
        self.scenario_list = test_obj.get('scenario_list')  # 执行场景列表
        self.sio = StringIOLog()  # 控制台日志
        # self.sio = test_obj.get('sio', StringIOLog())  # 控制台日志

        self.var_conversion_active_list = []

        self.al = AsyncLogs()  # 异步日志
        self.test_result = AsyncTestResult()  # 测试结果实例

        self.start_time = 0
        self.end_time = 0

    async def json_format(self, d, msg=None):
        """
        json格式打印
        :param d:
        :param msg:
        :return:
        """
        try:
            output = '{}\n'.format(msg) + json.dumps(
                d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False
            )
            self.sio.log(output)
        except BaseException as e:
            self.sio.log('{}\n{}'.format(msg, d))

    async def send_logs(self, url, headers, req_json, http_code, resp_headers, resp_json):
        """
        测试用例日志打印
        :param url:
        :param headers:
        :param req_json:
        :param http_code:
        :param resp_headers:
        :param resp_json:
        :return:
        """
        self.sio.log(f'=== url ===\n{url}')
        await self.json_format(headers, msg='=== headers ===')
        await self.json_format(req_json, msg='=== request json ===')
        self.sio.log(f'=== http_code ===\n{http_code}')
        await self.json_format(resp_headers, msg='=== response headers ===')
        await self.json_format(resp_json, msg='=== response json ===')

    async def get_data_logs(self, logs_type, data_id, data_name, case_id=None, scenario_id=None):
        """

        :param logs_type: 日志类型(用例;场景)
        :param data_id: 参数id
        :param data_name: 参数名称
        :param case_id: 用例id
        :param scenario_id: 场景id
        :return:
        """

        data_logs = await self.al.gen_data_logs_obj(data_id=data_id, data_name=data_name)

        if logs_type == 'case':
            await self.al.add_case_data_logs(case_id=case_id, data_id=data_id, logs=data_logs)

        elif logs_type == 'scenario':
            await self.al.add_scenario_case_data_logs(
                scenario_id=scenario_id, case_id=case_id, data_id=data_id, logs=data_logs
            )
        else:
            return False

        return data_logs

    async def data_logs_to_json(self, logs_type, data_id, case_id=None, scenario_id=None):
        """
        将原来类型为class的参数日志转为json
        :param logs_type: 日志类型(用例;场景)
        :param data_id: 参数id
        :param case_id: 用例id
        :param scenario_id: 场景id
        :return:
        """

        if logs_type == 'case':
            data_logs = self.al.case_logs_dict.get(case_id).get('data_dict').get(data_id)
            if data_logs:
                data_logs_json = await data_logs.to_json()
                await self.al.add_case_data_logs(case_id=case_id, data_id=data_id, logs=data_logs_json)
                return True
            return False

        elif logs_type == 'scenario':
            data_logs = self.al.scenario_logs_dict.get(scenario_id).get('case_dict').get(case_id).get('data_dict').get(
                data_id)
            if data_logs:
                data_logs_json = await data_logs.to_json()
                await self.al.add_scenario_case_data_logs(
                    scenario_id=scenario_id, case_id=case_id, data_id=data_id, logs=data_logs_json
                )
                return True
            return False
        else:
            return False

    async def var_conversion_main(self, json_str, d):
        """
        变量转换参数
        :param json_str: json字符串
        :param d: 数据字典
        :return:
        """
        matchList = re.findall(r'("?\$\{.*?\}.*?")', json_str)
        for match in matchList:
            varList = re.findall(r'\$\{.*?\}', match)
            if len(varList) > 1:
                _match = match
                for var in varList:
                    key = var[2:-1]
                    val = d.get(key)
                    if val:
                        if isinstance(val, int):
                            _match = _match.replace('${' + key + '}', json.dumps(val, ensure_ascii=False))
                        elif isinstance(val, str):
                            _match = _match.replace('${' + key + '}', json.dumps(val, ensure_ascii=False)[1:-1])
                        else:
                            _match = _match.replace('${' + key + '}',
                                                    re.sub(r'"', '\\"', json.dumps(val, ensure_ascii=False)))
                json_str = json_str.replace(match, _match)
            else:
                _matchList = re.findall(r'\$\{(.*?)\}(.*?")', match)
                key = _matchList[0][0]
                val = d.get(key)
                if val:
                    if _matchList[0][1] == '"':
                        if isinstance(val, str):
                            json_str = json_str.replace(match, match.replace('${' + key + '}', val))
                        else:
                            json_str = json_str.replace(match, match.replace('${' + key + '}',
                                                                             json.dumps(val, ensure_ascii=False))[1:-1])
                    else:
                        if isinstance(val, str):
                            json_str = json_str.replace(match, match.replace('${' + key + '}', val))
                        else:
                            res = match.replace('${' + key + '}',
                                                re.sub(r'"', '\\"', json.dumps(val, ensure_ascii=False)))
                            json_str = json_str.replace(match, res)

        result_data = json.loads(json_str)
        print(">>>", json_str)
        print(">>>", result_data)
        return result_data

    async def var_conversion(self, before_value):
        """
        变量转换参数
        :param before_value:
        :return:
        """
        if isinstance(before_value, int):
            return before_value

        json_str = json.dumps(before_value, ensure_ascii=False)
        var_name_list = re.findall('\\$\\{([^}]*)', json_str)  # 找出参数中带 ${} 的字符串
        print('=== var_name_list ===')
        print(var_name_list)

        if not var_name_list:
            return before_value

        # TODO 改为 aiomysql
        sql = f"""
        select id, var_name, var_value, var_type, is_active 
        from exile_test_variable 
        where {f"var_name in {tuple(var_name_list)}" if len(var_name_list) > 1 else f"var_name='{var_name_list[-1]}'"} 
        and is_deleted=0;
        """
        print('=== sql ===')
        print(sql)
        query_result = project_db.select(sql=sql)

        print('=== value_type_dict ===')
        print(value_type_dict)

        print('=== variable_type_dict ===')
        print(variable_type_dict)

        d = {}
        for obj in query_result:  # 生成: {"var_name":"var_value"}
            var_id = obj.get('id')
            var_name = obj.get('var_name')
            var_value = obj.get('var_value')
            var_type = obj.get('var_type')
            is_active = obj.get('is_active')
            print('===var_type===', var_type)
            print('===var_name===', var_name)
            if var_type in variable_type_dict.keys():  # 函数
                if var_id not in self.var_conversion_active_list:
                    new_val = variable_type_dict.get(var_type)()  # 首次触函数
                    d[var_name] = new_val
                    self.current_var_value = new_val
                    self.var_conversion_active_list.append(var_id)
                else:
                    if is_active == 1:
                        new_val = variable_type_dict.get(var_type)()
                        d[var_name] = new_val
                    else:
                        d[var_name] = self.current_var_value
            else:
                if var_type in value_type_dict:
                    d[var_name] = json.loads(var_value)
                else:
                    d[var_name] = var_value
        print(d)
        # return json_str, d
        result = await self.var_conversion_main(json_str=json_str, d=d)
        return result

    async def request_before(self, data_id, data_name, case_data_info, data_logs):
        """请求前置"""

        await data_logs.add_logs(key='request_before', val=f"=== 参数前置准备:{data_id}-{data_name} ===")

        print("=== 参数前置准备 ===")
        print(case_data_info)
        is_before = case_data_info.get('is_before')
        data_before = case_data_info.get('data_before')

        try:
            if is_before:
                print('is_before')
                # data_before = self.var_conversion(data_before)
                print('=== data_before ===')
                print(data_before)
                # list(map(self.gen_case_data_ready, data_before))
        except BaseException as e:
            self.sio.log(f"=== 参数前置准备失败:{str(e)} ===", status="error")
            await data_logs.add_logs(key='request_after', val=f"=== 参数前置准备失败:{str(e)} ===")

    async def request_after(self, data_id, data_name, case_data_info, data_logs):
        """请求后置"""

        await data_logs.add_logs(key='request_after', val=f"=== 参数后置准备:{data_id}-{data_name} ===")

    @classmethod
    async def check_method(cls, session, method):
        """检查请求方式"""

        if not hasattr(session, method):
            print(f'错误的请求方式:{method}')
            return False
        return True

    @classmethod
    async def check_headers(cls, headers):
        """检查headers"""

        for k, v in headers.items():
            if isinstance(v, (dict, list)):
                headers[k] = json.dumps(v)
        return headers

    async def gen_url(self, request_base_url, request_url):
        """
        生成url
        :param request_base_url: 用例环境
        :param request_url: 用例url
        :return:
        """

        url = self.base_url + request_url if self.use_base_url else request_base_url + request_url
        return url

    async def current_request(self, method, url, headers=None, **kwargs):
        """异步请求"""

        sem = asyncio.Semaphore(100)  # 并发数量限制
        # timeout = aiohttp.ClientTimeout(total=3)  # 超时
        async with sem:
            headers = await self.check_headers(headers)
            async with aiohttp.ClientSession(headers=headers, cookies='') as session:
                method = method.lower()
                result = await self.check_method(session, method)
                if not result:
                    resp = {
                        "error": f"错误的请求方式:{method}"
                    }
                    return resp
                async with getattr(session, method)(url, **kwargs) as resp:
                    http_code = resp.status
                    try:
                        json_resp = await resp.json()
                        resp_headers = {k: v for k, v in resp.headers.items()}
                        result = {
                            "http_code": http_code,
                            "resp_json": json_resp,
                            "resp_headers": resp_headers
                        }
                        return result
                    except BaseException as e:
                        result = {
                            "http_code": http_code,
                            "resp_error": f"{e}"
                        }
                        return result

    async def data_task(self, data_index=None, data=None, **kwargs):
        """参数"""

        # for data_index, bind in enumerate(bind_info, 1):
        scenario_id = kwargs.get('scenario_id')
        logs_type = kwargs.get('logs_type')
        case_id = kwargs.get('case_id')
        url = kwargs.get('url')
        request_method = kwargs.get('request_method')

        case_data_info = data.get('case_data_info', {})
        case_resp_ass_info = data.get('case_resp_ass_info', [])
        case_field_ass_info = data.get('case_field_ass_info', [])

        data_id = case_data_info.get('id')
        data_name = case_data_info.get('data_name')

        data_logs = await self.get_data_logs(
            logs_type=logs_type,
            data_id=data_id,
            data_name=data_name,
            case_id=case_id,
            scenario_id=scenario_id
        )

        await self.request_before(data_id, data_name, case_data_info, data_logs)

        headers = case_data_info.get('request_headers')
        request_params = case_data_info.get('request_params')
        request_body = case_data_info.get('request_body')
        request_body_type = case_data_info.get('request_body_type')

        req_type_dict = {
            "none": "",
            "text": {"text": request_body},
            "html": {"text": request_body},
            "xml": {"text": request_body},
            "form-data": {"data": request_body},
            "x-form-data": {"data": request_body},
            "json": {"json": request_body}
        }
        before_send = {
            "url": url,
            "headers": headers,
            "payload": {},
        }
        req_json_data = req_type_dict.get(request_body_type)

        if not req_json_data:
            before_send['payload']['params'] = request_params
        else:
            before_send['payload'].update(req_json_data)

        print('=== before_send ===')
        print(before_send)

        send = await self.var_conversion(before_send)
        print("=== send ===")
        print(send)

        url = send.get('url')
        headers = send.get('headers')
        payload = send.get('payload')

        try:
            result = await self.current_request(
                method=request_method,
                url=url,
                headers=headers,
                **payload
            )
            print('=== result ===')
            print(result)

            resp_headers = result.get("resp_headers")
            http_code = result.get('http_code')
            resp_json = result.get("resp_json")

            await self.send_logs(
                url=url,
                headers=headers,
                req_json=payload,
                http_code=http_code,
                resp_headers=resp_headers,
                resp_json=resp_json
            )

            await data_logs.add_logs(key='url', val=f"=== 数据驱动:{data_index} ===")
            await data_logs.add_logs(key='url', val=url)
            await data_logs.add_logs(key='method', val=request_method)
            await data_logs.add_logs(key='request_headers', val=headers)
            await data_logs.add_logs(key='request_body', val=payload.get(list(payload.keys())[0]))
            await data_logs.add_logs(key='http_code', val=http_code)
            await data_logs.add_logs(key='response_headers', val=resp_headers)
            await data_logs.add_logs(key='response_body', val=resp_json)
            await self.al.set_case_flag(case_id=case_id, flag=True)

        except BaseException as e:
            await data_logs.add_logs(key='url', val=f"=== 数据驱动:{data_index} ===")
            await data_logs.add_logs(key='url', val=url)
            await data_logs.add_logs(key='method', val=request_method)
            await data_logs.add_logs(key='request_headers', val=headers)
            await data_logs.add_logs(key='request_body', val=payload.get(list(payload.keys())[0]))
            await data_logs.add_logs(key='http_code', val=f"请求失败:{e}")
            await self.al.set_case_flag(case_id=case_id, flag=False)
            return False

        await self.request_after(data_id, data_name, case_data_info, data_logs)

        case_resp_ass_info = await self.var_conversion(case_resp_ass_info)
        ass_resp = AsyncAssertionResponse(
            http_code=http_code,
            resp_headers=resp_headers,
            resp_json=resp_json,
            case_resp_ass_info=case_resp_ass_info,
            data_logs=data_logs,
            desc=f"{data_id}-{data_name}",
            sio=self.sio
        )
        ass_resp_result = await ass_resp.main()
        await self.test_result.add_resp_ass(ass_resp_result)
        # 从下至上设置flag以最下为基准
        current_flag = ass_resp_result.get('flag', 'flag异常')
        await self.al.set_case_flag(case_id=case_id, flag=current_flag)
        await data_logs.set_flag(flag=current_flag)

        ass_field = AsyncAssertionField(
            case_field_ass_info=case_field_ass_info,
            data_logs=data_logs,
            desc=f"{data_id}-{data_name}",
            sio=self.sio
        )
        ass_field_result = await ass_field.main()
        await self.test_result.add_field_ass(ass_field_result)
        """
        current_flag = ass_field_result.get('flag', 'flag异常')
        await self.al.set_case_flag(case_id=case_id, flag=current_flag)
        await data_logs.set_flag(flag=current_flag)
        """

        # 结束日志,用例执行的参数格式化后加入到用例日志字典中
        await self.data_logs_to_json(logs_type=logs_type, data_id=data_id, case_id=case_id, scenario_id=scenario_id)

    async def case_task(self, case_index=None, case=None, **kwargs):
        """
        用例
        :param case_index:
        :param case:
        :param kwargs:
        :return:
        """

        # for case_index, case in enumerate(self.case_list, 1):
        case_info = case.get('case_info', {})
        bind_info = case.get('bind_info', [])
        case_expand = case.get('case_expand', {})
        case_sleep = case_expand.get('sleep')

        case_id = case_info.get('id')
        case_name = case_info.get('case_name')
        creator = case_info.get('creator')
        creator_id = case_info.get('creator_id')

        is_scenario = kwargs.get('is_scenario')
        if is_scenario:
            scenario_index = kwargs.get('scenario_index')
            scenario_id = kwargs.get('scenario_id')
            scenario_title = kwargs.get('scenario_title')
            await self.al.add_scenario_logs(scenario_id=scenario_id, logs=f'=== 执行场景: {scenario_index} ===')
            await self.al.add_scenario_logs(scenario_id=scenario_id,
                                            logs=f'=== 场景ID: {scenario_id} 场景名称: {scenario_title} ===')
            await self.al.add_scenario_logs(scenario_id=scenario_id, logs=f'=== 用例ID: {case_id}  用例名称: {case_name} ===')
            if not bind_info:
                await self.al.add_scenario_logs(scenario_id=scenario_id, logs='=== 未配置请求参数 ===')
                return None
        else:
            await self.al.add_case_logs(case_id=case_id, logs=f'=== 执行用例: {case_index} ===')
            await self.al.add_case_logs(case_id=case_id, logs=f'=== 用例ID: {case_id}  用例名称: {case_name} ===')
            if not bind_info:
                await self.al.add_case_logs(case_id=case_id, logs='=== 未配置请求参数 ===')
                return None

        request_base_url = case_info.get('request_base_url')
        request_url = case_info.get('request_url')
        request_method = case_info.get('request_method')
        url = await self.gen_url(request_base_url=request_base_url, request_url=request_url)
        update_var_list = []

        p = {
            "logs_type": "scenario" if is_scenario else "case",
            "scenario_id": scenario_id if is_scenario else None,
            "case_id": case_id,
            "request_method": request_method,
            "url": url
        }

        if not self.data_driven:
            print('=== 数据驱动 === False')
            await self.data_task(data_index=1, data=bind_info[0], **p)
        else:
            print('=== 数据驱动 === True')
            data_task = [
                asyncio.create_task(self.data_task(data_index, data, **p)) for data_index, data in
                enumerate(bind_info, 1)
            ]
            await asyncio.wait(data_task)

    async def scenario_task(self, scenario_index=None, scenario=None):
        """场景"""

        scenario_id = scenario.get('id')
        scenario_title = scenario.get('scenario_title')
        case_list = scenario.get('case_list')
        d = {
            "is_scenario": True,
            "logs_type": "scenario",
            "scenario_index": scenario_index,
            "scenario_id": scenario_id,
            "scenario_title": scenario_title
        }
        for case_index, case in enumerate(case_list, 1):
            await self.al.add_scenario_logs(scenario_id=scenario_id, logs=f'=== start scenario: {scenario_index} ===')
            await self.al.add_scenario_logs(scenario_id=scenario_id,
                                            logs=f'=== 场景ID: {scenario_index}  场景名称: {scenario_title}===')
            await self.case_task(case_index, case, **d)

    async def gen_logs(self):
        """日志"""

    async def debug_logs(self):
        """调试日志"""

        self.sio.log("=== 用例日志 ===")
        case_logs = [v for k, v in self.al.case_logs_dict.items()]
        case_logs_json = json.dumps(case_logs, ensure_ascii=False)
        self.sio.log(case_logs_json)

        self.sio.log("=== 场景日志 ===")
        scenario_logs = [v for k, v in self.al.scenario_logs_dict.items()]
        scenario_logs_json = json.dumps(scenario_logs, ensure_ascii=False)
        self.sio.log(scenario_logs_json)

    async def case_loader(self):
        """用例加载执行"""

        case_task = [
            asyncio.create_task(self.case_task(case_index, case)) for case_index, case in enumerate(self.case_list, 1)
        ]
        await asyncio.wait(case_task)

        await self.debug_logs()

    async def scenario_loader(self):
        """场景加载执行"""

        scenario_task = [
            asyncio.create_task(self.scenario_task(scenario_index, scenario)) for scenario_index, scenario in
            enumerate(self.scenario_list, 1)
        ]
        await asyncio.wait(scenario_task)

        await self.debug_logs()

    async def main(self):
        """main"""

        # 生成日志数据结构
        await self.al.gen_case_logs_dict(case_list=self.case_list)
        await self.al.gen_scenario_logs_dict(scenario_list=self.scenario_list)

        # 开始时间
        self.start_time = time.time()

        if self.case_list:
            await self.case_loader()

        if self.scenario_list:
            await self.scenario_loader()

        await self.gen_logs()

        # 结束时间
        self.end_time = f"{time.time() - self.start_time}s"
