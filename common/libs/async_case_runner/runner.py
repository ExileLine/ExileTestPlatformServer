# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 13:18
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : runner.py
# @Software: PyCharm

import re
import json
import time
import aiohttp
import asyncio
import requests

from common.libs.db import project_db
from common.libs.data_dict import var_func_dict
from common.libs.StringIOLog import StringIOLog
from common.libs.async_case_runner.async_assertion import AsyncAssertionResponse, AsyncAssertionField
from common.libs.async_case_runner.async_logs import AsyncRunnerLogs
from common.libs.async_case_runner.async_result import AsyncTestResult


class CaseRunner:
    """同步用例执行"""

    def __init__(self, test_obj=None):

        self.test_obj = test_obj
        self.sio = test_obj.get('sio', StringIOLog())
        self.end_time = 0

    def json_format(self, d, msg=None):
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

    def send_logs(self, url, headers, req_json, http_code, resp_headers, resp_json):
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
        self.json_format(headers, msg='=== headers ===')
        self.json_format(req_json, msg='=== request json ===')
        self.sio.log(f'=== http_code ===\n{http_code}')
        self.json_format(resp_headers, msg='=== response headers ===')
        self.json_format(resp_json, msg='=== response json ===')

    def request_before(self, a):
        """请求前置"""
        print('request_before', a)

    def request_after(self, a):
        """请求后置"""
        print('request_after', a)

    @classmethod
    def check_method(cls, session, method):
        """检查请求方式"""

        if not hasattr(session, method):
            print(f'错误的请求方式:{method}')
            return False
        return True

    @classmethod
    def check_headers(cls, headers):
        """检查headers"""

        for k, v in headers.items():
            if isinstance(v, (dict, list)):
                headers[k] = json.dumps(v)
        return headers

    def current_request(self, method, **kwargs):
        """同步请求"""

        method = method.lower()
        if not self.check_method:
            response = {
                "error": f"错误的请求方式:{method}"
            }
            return response
        kwargs['headers'] = self.check_headers(kwargs.get('headers'))
        response = getattr(requests, method)(**kwargs, verify=False)
        http_code = response.status_code
        try:
            resp_headers = response.headers
            resp_json = response.json()
            result = {
                "http_code": http_code,
                "resp_json": resp_json,
                "resp_headers": resp_headers
            }
            return result
        except BaseException as e:
            result = {
                "http_code": http_code,
                "resp_error": f"{e}"
            }
            return result


class AsyncCaseRunner:
    """
    异步用例执行
    """

    def __init__(self, test_obj=None):

        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.data_driven = test_obj.get('data_driven')

        self.case_list = test_obj.get('case_list')  # 执行用例列表
        self.scenario_list = test_obj.get('scenario_list')  # 执行场景列表
        self.sio = test_obj.get('sio', StringIOLog())  # 控制台日志

        self.var_conversion_active_list = []

        self.arl = AsyncRunnerLogs()  # 测试日志实例
        self.case_logs_dict = {}  # 用例日志字典
        self.scenario_logs_dict = {}  # 场景日志字典

        self.test_result = AsyncTestResult()  # 测试结果实例

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

    async def get_case_logs(self, case_id, case_name):
        """

        :param case_id:
        :param case_name:
        :return:
        """

        case_logs = self.case_logs_dict.get(case_id)
        if case_logs:
            return case_logs
        else:
            self.case_logs_dict[case_id] = await self.arl.gen_case_logs(case_id=case_id, case_name=case_name)
            return self.case_logs_dict.get(case_id)

    async def get_data_logs(self, case_id, data_id, data_name, obj_to_json=False):
        """

        :param case_id:
        :param data_id:
        :param data_name:
        :param obj_to_json: 类转字典结束本次参数日志记录
        :return:
        """

        data_logs = self.case_logs_dict.get(case_id).get('data_dict').get(data_id)
        if obj_to_json:
            self.case_logs_dict.get(case_id).get('data_dict')[data_id] = await data_logs.to_json()
            return True

        if data_logs:
            return data_logs
        else:
            self.case_logs_dict.get(case_id).get('data_dict')[data_id] = await self.arl.gen_data_logs(
                data_id=data_id,
                data_name=data_name)
            return self.case_logs_dict.get(case_id).get('data_dict').get(data_id)

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
        query_result = project_db.select(sql=sql)

        d = {}
        for obj in query_result:  # 生成: {"var_name":"var_value"}
            var_id = obj.get('id')
            var_name = obj.get('var_name')
            var_value = obj.get('var_value')
            var_type = obj.get('var_type')
            is_active = obj.get('is_active')
            print('===var_type===', var_type)
            print('===var_name===', var_name)
            if str(var_type) in var_func_dict.keys():  # 函数
                if var_id not in self.var_conversion_active_list:
                    new_val = var_func_dict.get(str(var_type))()  # 首次触函数
                    d[var_name] = new_val
                    self.current_var_value = new_val
                    self.var_conversion_active_list.append(var_id)
                else:
                    if is_active == 1:
                        new_val = var_func_dict.get(str(var_type))()
                        d[var_name] = new_val
                    else:
                        d[var_name] = self.current_var_value
            else:
                if var_type in (1, 2):
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
        case_id = kwargs.get('case_id')
        url = kwargs.get('url')
        request_method = kwargs.get('request_method')

        case_data_info = data.get('case_data_info', {})
        case_resp_ass_info = data.get('case_resp_ass_info', [])
        case_field_ass_info = data.get('case_field_ass_info', [])

        data_id = case_data_info.get('id')
        data_name = case_data_info.get('data_name')

        data_logs = await self.get_data_logs(case_id=case_id, data_id=data_id, data_name=data_name)

        await self.request_before(data_id, data_name, case_data_info, data_logs)

        headers = case_data_info.get('request_headers')
        request_params = case_data_info.get('request_params')
        request_body = case_data_info.get('request_body')
        request_body_type = case_data_info.get('request_body_type')

        req_type_dict = {
            "1": {"data": request_body},
            "2": {"json": request_body},
            "3": {"data": request_body}
        }
        before_send = {
            "url": url,
            "headers": headers,
            "payload": {},
        }
        req_json_data = req_type_dict.get(str(request_body_type))

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

        await data_logs.add_logs(key='url', val=f"=== 数据驱动:{data_index} ===")
        await data_logs.add_logs(key='url', val=url)
        await data_logs.add_logs(key='method', val=request_method)
        await data_logs.add_logs(key='request_headers', val=headers)
        await data_logs.add_logs(key='request_body', val=payload.get(list(payload.keys())[0]))
        await data_logs.add_logs(key='http_code', val=http_code)
        await data_logs.add_logs(key='response_headers', val=resp_headers)
        await data_logs.add_logs(key='response_body', val=resp_json)

        await self.request_after(data_id, data_name, case_data_info, data_logs)

        ass_resp = AsyncAssertionResponse(
            http_code, resp_headers, resp_json, self.sio, case_resp_ass_info, data_logs, f"{data_id}-{data_name}"
        )
        await ass_resp.main()

        ass_field = AsyncAssertionField(
            self.sio, case_field_ass_info, data_logs, f"{data_id}-{data_name}"
        )
        await ass_field.main()

        await self.get_data_logs(case_id=case_id, data_id=data_id, data_name=data_name, obj_to_json=True)

    async def case_task(self, case_index=None, case=None):
        """用例"""

        # for case_index, case in enumerate(self.case_list, 1):
        case_info = case.get('case_info', {})
        bind_info = case.get('bind_info', [])
        case_expand = case.get('case_expand', {})
        case_sleep = case_expand.get('sleep')

        case_id = case_info.get('id')
        case_name = case_info.get('case_name')
        creator = case_info.get('creator')
        creator_id = case_info.get('creator_id')

        case_logs = await self.get_case_logs(case_id, case_name)
        case_logs['logs'].append(f'=== start case: {case_index} ===')
        case_logs['logs'].append(f'=== 用例ID: {case_id}  用例名称: {case_name}===')
        self.case_logs_dict[case_id] = case_logs

        request_base_url = case_info.get('request_base_url')
        request_url = case_info.get('request_url')
        request_method = case_info.get('request_method')
        url = await self.gen_url(request_base_url=request_base_url, request_url=request_url)
        update_var_list = []

        if not bind_info:
            case_logs['logs'].append('=== 未配置请求参数 ===')
            return None

        p = {
            "case_id": case_id,
            "request_method": request_method,
            "url": url
        }

        if not self.data_driven:
            await self.data_task(data_index=1, data=bind_info[0], **p)
        else:
            data_task = [
                asyncio.create_task(self.data_task(data_index, data, **p)) for data_index, data in
                enumerate(bind_info, 1)
            ]
            await asyncio.wait(data_task)

        """
        for data_index, bind in enumerate(bind_info, 1):
            self.sio.log(f"=== 数据驱动:{data_index} ===")

            case_data_info = bind.get('case_data_info', {})
            case_resp_ass_info = bind.get('case_resp_ass_info', [])
            case_field_ass_info = bind.get('case_field_ass_info', [])

            await self.request_before(case_data_info)

            headers = case_data_info.get('request_headers')
            request_params = case_data_info.get('request_params')
            request_body = case_data_info.get('request_body')
            request_body_type = case_data_info.get('request_body_type')

            req_type_dict = {
                "1": {"data": request_body},
                "2": {"json": request_body},
                "3": {"data": request_body}
            }
            before_send = {
                "url": url,
                "headers": headers,
                "payload": {},
            }
            req_json_data = req_type_dict.get(str(request_body_type))

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
                req_json=req_json_data,
                http_code=http_code,
                resp_headers=resp_headers,
                resp_json=resp_json
            )

            await self.request_after(case_data_info)

            ass_resp = AsyncAssertionResponse(http_code, resp_headers, resp_json, self.sio, case_resp_ass_info)
            await ass_resp.main()

            ass_field = AsyncAssertionField(self.sio, case_field_ass_info)
            await ass_field.main()

            data_info = {
                "data_id": case_data_info.get('id'),
                "data_name": case_data_info.get('data_name'),
                "logs": self.sio.get_stringio().split('\n'),
                # "error": self.logs_error_switch
            }
            self.case_result_dict.get(case_id)['data_list'].append(data_info)
            self.case_result_dict.get(case_id)['error'] = True if True in error_list else False

            if not self.data_driven:
                self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                break
        """

    async def scenario_task(self, scenario_index=None, scenario=None):
        """场景"""

    async def gen_logs(self):
        """日志"""

    async def debug_logs(self):
        """调试日志"""

        print(json.dumps(self.case_logs_dict, ensure_ascii=False))
        print(json.dumps(self.scenario_logs_dict, ensure_ascii=False))

    async def case_loader(self):
        """用例加载执行"""

        start_time = time.time()
        case_task = [
            asyncio.create_task(self.case_task(case_index, case)) for case_index, case in enumerate(self.case_list, 1)
        ]
        await asyncio.wait(case_task)
        self.end_time = f"{time.time() - start_time}s"

        await self.debug_logs()

    async def scenario_loader(self):
        """场景加载执行"""

    async def main(self):
        """main"""

        if self.case_list:
            await self.case_loader()

        if self.scenario_list:
            await self.scenario_loader()
