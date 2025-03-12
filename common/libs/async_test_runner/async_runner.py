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
import traceback

from config.config import config_obj
from common.libs.db import project_db, R
from common.libs.db import MYSQL_CONF, AIO_REDIS_CONF
from common.libs.async_db import MyAioMySQL, MyAioRedis
from common.libs.data_dict import GlobalsDict, F
from common.libs.StringIOLog import StringIOLog
from common.libs.async_test_runner.async_assertion import AsyncAssertionResponse, AsyncAssertionField
from common.libs.async_test_runner.async_logs import AsyncLogs, AsyncDataLogs
from common.libs.async_test_runner.async_result import AsyncTestResult
from common.libs.execute_code import execute_code
from common.tools.message_push import MessagePush

resp_source_tuple = GlobalsDict.resp_source_tuple()
value_type_dict = GlobalsDict.value_type_dict()
variable_type_dict = GlobalsDict.variable_type_dict(merge=False)


# TODO: request_before; request_after
# TODO: 异步任务中 aio_redis 执行一次后缺少事件循环的问题
class AsyncCaseRunner:
    """
    异步用例执行
    """

    def __init__(self, test_obj=None, is_debug=False):

        self.is_debug = is_debug

        self.aio_db = MyAioMySQL(conf_dict=MYSQL_CONF, debug=True)  # 异步Mysql
        # self.aio_redis = MyAioRedis(is_pool=True, conf_dict=AIO_REDIS_CONF).redis  # 异步Redis

        self.test_obj = test_obj if test_obj else {}
        self.project_id = test_obj.get('project_id')  # 项目归属id
        self.execute_id = test_obj.get('execute_id')  # 执行名称(用例id,场景id,任务id,模块id...)
        self.execute_key = test_obj.get('execute_key')
        self.execute_name = test_obj.get('execute_name')  # 执行名称(用例名,场景名,任务名,模块名...)
        self.execute_type = test_obj.get('execute_type')  # 执行类型(case,scenario,task,module...)
        self.execute_username = test_obj.get('execute_username')
        self.execute_user_id = test_obj.get('execute_user_id')
        self.trigger_type = test_obj.get('trigger_type')  # 触发执行类型(user_execute,timed_execute...)
        self.execute_logs_id = test_obj.get('execute_logs_id')  # 执行日志id用于执行完毕后回写redis_key等数据

        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.data_driven = test_obj.get('data_driven')

        self.case_list = test_obj.get('case_list')  # 执行用例列表
        self.scenario_list = test_obj.get('scenario_list')  # 执行场景列表

        self.use_dd_push = test_obj.get('use_dd_push', False)  # 钉钉推送
        self.ding_talk_url = test_obj.get('ding_talk_url')  # 钉钉推送群url

        self.sio = StringIOLog()  # 控制台日志
        # self.sio = test_obj.get('sio', StringIOLog())  # 控制台日志

        self.var_conversion_active_list = []

        self.al = AsyncLogs()  # 异步日志
        self.case_logs = {}  # 格式化用例日志
        self.scenario_logs = {}  # 格式化场景日志
        self.test_result = AsyncTestResult()  # 测试结果实例
        self.result_summary = {}  # 测试结果汇总
        self.redis_key = ""  # redis缓存日志的key
        self.execute_status = True  # 执行完全通过标识

        self.start_time = 0
        self.end_time = 0

        self.obj_id_list = []

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

    async def get_data_logs(self, logs_type, data_logs=None, case_uuid=None, scenario_uuid=None):
        """

        :param logs_type: 日志类型(用例;场景)
        :param data_logs: 参数日志实例
        :param case_uuid: 用例uuid
        :param scenario_uuid: 场景uuid
        :return:
        """

        if logs_type == 'case':
            await self.al.add_case_data_logs(case_uuid=case_uuid, data_id=data_logs.data_id, logs=data_logs)

        elif logs_type == 'scenario':
            await self.al.add_scenario_case_data_logs(
                scenario_uuid=scenario_uuid, case_uuid=case_uuid, data_id=data_logs.data_id, logs=data_logs
            )
        else:
            return False

    async def data_logs_to_json(self, logs_type, data_id, case_uuid=None, scenario_uuid=None):
        """
        将原来类型为class的参数日志转为json
        :param logs_type: 日志类型(用例;场景)
        :param data_id: 参数id
        :param case_uuid: 用例uuid
        :param scenario_uuid: 场景uuid
        :return:
        """

        if logs_type == 'case':
            data_logs = self.al.case_logs_dict.get(case_uuid).get('data_dict').get(data_id)
            if data_logs:
                data_logs_json = await data_logs.to_json()
                await self.al.add_case_data_logs(case_uuid=case_uuid, data_id=data_id, logs=data_logs_json)
                return True
            return False

        elif logs_type == 'scenario':
            data_logs = self.al.scenario_logs_dict.get(scenario_uuid).get('case_dict').get(case_uuid).get(
                'data_dict').get(data_id)
            if data_logs:
                data_logs_json = await data_logs.to_json()
                await self.al.add_scenario_case_data_logs(
                    scenario_uuid=scenario_uuid, case_uuid=case_uuid, data_id=data_id, logs=data_logs_json
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

        sql = f"""
        SELECT id, var_name, var_value, var_type, var_args, is_active 
        FROM exile5_test_variable 
        WHERE {f"var_name in {tuple(var_name_list)}" if len(var_name_list) > 1 else f"var_name='{var_name_list[-1]}'"} 
        AND is_deleted=0 AND project_id={self.project_id};
        """
        print('=== sql ===')
        print(sql)
        # query_result = project_db.select(sql=sql)

        query_result = await self.aio_db.query(sql=sql)
        print(query_result)

        d = {}
        for obj in query_result:  # 生成: {"var_name":"var_value"}
            var_id = obj.get('id')
            var_name = obj.get('var_name')
            var_value = obj.get('var_value')
            var_type = obj.get('var_type')
            var_args = obj.get('var_args')
            is_active = obj.get('is_active')

            print('=== var_name ===', var_name)
            print('=== var_value ===', var_value)
            print('=== var_type ===', var_type)
            print('=== var_args ===', var_args)

            if var_type in variable_type_dict.keys():  # 自定义函数
                if var_id not in self.var_conversion_active_list:
                    new_val = variable_type_dict.get(var_type)(**var_args)  # 首次触函数
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
                if var_type in value_type_dict:  # 内置函数
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

    async def update_variable(self, data_id, data_name, update_var_list, resp_headers, resp_json, data_logs):
        """
        更新关系变量
        :param data_id: 参数id
        :param data_name: 参数名称
        :param update_var_list: 关系变量列表
        :param resp_headers: 响应头
        :param resp_json: 响应体
        :param data_logs: 日志对象
        :return:
        """

        self.sio.log(f"=== update_var_list ===\n{update_var_list}")

        var_source_dict = {
            "response_headers": resp_headers,
            "response_body": resp_json
        }

        for var_index, variable_obj in enumerate(update_var_list, 1):
            """
            {
                "id": 3,
                "var_value":"123",
                "var_source": "response_body",
                "expression": "obj.get('code')",
                "is_expression":0,
                "var_get_key": "code"
            }
            """
            self.sio.log(f"=== 参数ID:{data_id} 名称:{data_name} ===\n=== 更新关系变量 === {var_index} {variable_obj}")

            var_id = variable_obj.get('id')
            var_name = variable_obj.get('var_name')
            var_value = variable_obj.get('var_value')
            var_source = variable_obj.get('var_source')
            var_get_key = variable_obj.get('var_get_key')
            expression = variable_obj.get('expression')
            is_expression = variable_obj.get('is_expression')
            data = var_source_dict.get(var_source)

            if is_expression:
                # 表达式取值
                result_json = execute_code(code=expression, data=data)
                update_val_result = result_json.get('result_data')
            else:
                # 直接取值
                update_val_result = data.get(var_get_key)

            old_var = json.dumps(var_value, ensure_ascii=False)
            new_var = json.dumps(update_val_result, ensure_ascii=False)

            sql = f"""
            UPDATE exile5_test_variable SET var_value='{new_var}', update_time='{F.gen_datetime()}', update_timestamp={F.gen_timestamp()} WHERE id='{var_id}' and project_id={self.project_id}; """
            self.sio.log(f'=== update variable sql ===\n{sql}', status='success')
            # project_db.update(sql)
            await self.aio_db.execute(sql=sql)

            await data_logs.add_logs(key='update_variable', val=f"变量: {var_name} 值更新为: {update_val_result}")

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
        """
        前置准备->变量转换参数->请求->变量转换参数->响应断言->字段断言->更新变量
        :param data_index: 参数下标
        :param data: 参数对象
        :param kwargs: 通用参数
        :return:
        """

        logs_type = kwargs.get('logs_type')
        scenario_uuid = kwargs.get('scenario_uuid')
        case_uuid = kwargs.get('case_uuid')
        url = kwargs.get('url')
        request_method = kwargs.get('request_method')

        case_data_info = data.get('data_info', {})
        case_resp_ass_info = data.get('case_resp_ass_info', [])
        case_field_ass_info = data.get('case_field_ass_info', [])

        data_id = case_data_info.get('id')
        data_name = case_data_info.get('data_name')
        update_var_list = case_data_info.get('update_var_list')

        data_logs = AsyncDataLogs(data_id=data_id, data_name=data_name)
        self.obj_id_list.append(id(data_logs))

        await self.get_data_logs(
            logs_type=logs_type,
            data_logs=data_logs,
            case_uuid=case_uuid,
            scenario_uuid=scenario_uuid
        )

        await self.request_before(data_id, data_name, case_data_info, data_logs)

        headers = case_data_info.get('request_headers', {})
        request_params = case_data_info.get('request_params', {})
        request_body = case_data_info.get('request_body', {})
        request_body_type = case_data_info.get('request_body_type', 'none')

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
            await self.al.set_flag(logs_type=logs_type, flag=True, case_uuid=case_uuid, scenario_uuid=scenario_uuid)
            await self.test_result.add_request(True)
            await self.set_execute_status(True)

        except BaseException as e:
            await data_logs.add_logs(key='url', val=f"=== 数据驱动:{data_index} ===")
            await data_logs.add_logs(key='url', val=url)
            await data_logs.add_logs(key='method', val=request_method)
            await data_logs.add_logs(key='request_headers', val=headers)
            await data_logs.add_logs(key='request_body', val=payload.get(list(payload.keys())[0]))
            await data_logs.add_logs(key='http_code', val=f"请求失败:{e}")
            await self.al.set_flag(logs_type=logs_type, flag=False, case_uuid=case_uuid, scenario_uuid=scenario_uuid)
            await self.test_result.add_request(False)
            await self.set_execute_status(False)

            # 请求失败,结束日志,用例执行的参数格式化后加入到用例日志字典中
            await self.data_logs_to_json(
                logs_type=logs_type, data_id=data_id, case_uuid=case_uuid, scenario_uuid=scenario_uuid
            )
            return False

        await self.request_after(data_id, data_name, case_data_info, data_logs)

        # 响应断言
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
        current_flag = ass_resp_result.get('flag', 'flag异常')  # 从下至上设置flag以最下为基准
        await data_logs.set_flag(flag=current_flag)
        await self.al.set_flag(
            logs_type=logs_type, flag=current_flag, case_uuid=case_uuid, scenario_uuid=scenario_uuid
        )
        await self.test_result.add_resp_ass(current_flag)
        await self.set_execute_status(current_flag)
        await data_logs.add_logs(key='response_assert', val="-" * 33)

        # 字段断言
        case_field_ass_info = await self.var_conversion(case_field_ass_info)
        ass_field = AsyncAssertionField(
            case_field_ass_info=case_field_ass_info,
            data_logs=data_logs,
            desc=f"{data_id}-{data_name}",
            sio=self.sio
        )
        ass_field_result = await ass_field.main()
        current_flag = ass_field_result.get('flag', 'flag异常')
        await data_logs.set_flag(flag=current_flag)
        await self.al.set_flag(
            logs_type=logs_type, flag=current_flag, case_uuid=case_uuid, scenario_uuid=scenario_uuid
        )
        await self.test_result.add_field_ass(current_flag)
        await self.set_execute_status(current_flag)
        await data_logs.add_logs(key='field_assert', val="-" * 33)

        self.sio.log(f"=== data_logs_flag === {data_logs.flag}")
        if data_logs.flag:
            # 更新关系变量
            await self.update_variable(
                data_id=data_id,
                data_name=data_name,
                update_var_list=update_var_list,
                resp_headers=resp_headers,
                resp_json=resp_json,
                data_logs=data_logs
            )
        else:
            self.sio.log(f"=== data_logs_flag False 不更新变量 ===")

        # 正常流程执行完毕,结束日志,用例执行的参数格式化后加入到用例日志字典中
        await self.data_logs_to_json(
            logs_type=logs_type, data_id=data_id, case_uuid=case_uuid, scenario_uuid=scenario_uuid
        )

    async def consume_data_task(self, bind_info: list, **kwargs):
        """
        根据数据驱动标识调用用例参数
        :param bind_info: 参数列表
        :param kwargs:  扩展参数
        :return:
        """

        if self.data_driven:
            print('=== 数据驱动 === True')
            for data_index, data in enumerate(bind_info, 1):
                await self.data_task(data_index, data, **kwargs)
        else:
            print('=== 数据驱动 === False')
            await self.data_task(data_index=1, data=bind_info[0], **kwargs)

    async def case_task(self, case_index=None, case=None):
        """
        用例
        :param case_index:  用例下标
        :param case:    用例对象
        :return:
        """

        # for case_index, case in enumerate(self.case_list, 1):
        case_info = case.get('case_info', {})
        bind_info = case.get('bind_info', [])
        case_expand = case.get('case_expand', {})
        case_sleep = case_expand.get('sleep')

        case_uuid = case.get('case_uuid')
        case_id = case_info.get('id')
        case_name = case_info.get('case_name')
        creator = case_info.get('creator')
        creator_id = case_info.get('creator_id')

        await self.al.add_case_logs(case_uuid=case_uuid, logs=f'=== 执行用例: {case_index} ===')
        await self.al.add_case_logs(case_uuid=case_uuid, logs=f'=== 用例ID: {case_id}  用例名称: {case_name} ===')
        if not bind_info:
            await self.al.add_case_logs(case_uuid=case_uuid, logs='=== 未配置请求参数 ===')
            return None

        request_base_url = case_info.get('request_base_url')
        request_url = case_info.get('request_url')
        request_method = case_info.get('request_method')
        url = await self.gen_url(request_base_url=request_base_url, request_url=request_url)

        p = {
            "logs_type": "case",
            "case_uuid": case_uuid,
            "case_id": case_id,
            "request_method": request_method,
            "url": url
        }

        await self.consume_data_task(bind_info, **p)

        current_case_execute_result = self.al.case_logs_dict.get(case_uuid).get('flag')
        await self.test_result.add_count(uuid_key=case_uuid, flag=current_case_execute_result)

    async def scenario_case_task(self, **kwargs):
        """
        场景中的用例
        :param kwargs: 扩展参数
        :return:
        """

        scenario_uuid = kwargs.get('scenario_uuid')
        scenario_index = kwargs.get('scenario_index')
        scenario_id = kwargs.get('id')
        scenario_title = kwargs.get('scenario_title')
        case_index = kwargs.get('case_index')
        case = kwargs.get('case')
        case_info = case.get('case_info', {})
        case_uuid = case.get('case_uuid')
        case_id = case_info.get('id')
        case_name = case_info.get('case_name')
        case_expand = case.get('case_expand', {})
        case_sleep = case_expand.get('sleep')
        bind_info = case.get('bind_info', [])

        await self.al.add_scenario_logs(
            scenario_uuid=scenario_uuid,
            logs=f'=== 场景下标: {scenario_index} 场景ID: {scenario_id} 场景名称: {scenario_title} ==='
        )
        await self.al.add_scenario_logs(
            scenario_uuid=scenario_uuid, logs=f'=== 用例ID: {case_id}  用例名称: {case_name} ==='
        )
        if not bind_info:
            await self.al.add_scenario_logs(scenario_uuid=scenario_uuid, logs='=== 未配置请求参数 ===')
            return None

        request_base_url = case_info.get('request_base_url')
        request_url = case_info.get('request_url')
        request_method = case_info.get('request_method')
        url = await self.gen_url(request_base_url=request_base_url, request_url=request_url)

        p = {
            "logs_type": "scenario",
            "scenario_uuid": scenario_uuid,
            "scenario_id": scenario_id,
            "case_uuid": case_uuid,
            "case_id": case_id,
            "request_method": request_method,
            "url": url
        }

        await self.consume_data_task(bind_info, **p)

        current_scenario_execute_result = self.al.scenario_logs_dict.get(scenario_uuid).get('flag')
        await self.test_result.add_count(uuid_key=scenario_uuid, flag=current_scenario_execute_result)

    async def scenario_task(self, scenario_index=None, scenario=None):
        """
        场景
        :param scenario_index:  场景下标
        :param scenario:    场景对象
        :return:
        """

        scenario_uuid = scenario.get('scenario_uuid')
        scenario_id = scenario.get('id')
        scenario_title = scenario.get('scenario_title')
        case_list = scenario.get('case_list')
        d = {
            "scenario_uuid": scenario_uuid,
            "scenario_index": scenario_index,
            "id": scenario_id,
            "scenario_title": scenario_title
        }
        for case_index, case in enumerate(case_list, 1):
            await self.al.add_scenario_logs(
                scenario_uuid=scenario_uuid, logs=f'=== start scenario: {scenario_index} ==='
            )
            await self.al.add_scenario_logs(
                scenario_uuid=scenario_uuid, logs=f'=== 场景ID: {scenario_id}  场景名称: {scenario_title}==='
            )
            d['case_index'] = case_index
            d['case'] = case
            await self.scenario_case_task(**d)

    async def set_execute_status(self, flag: bool):
        """
        设置执行完全通过标识
        :param flag:
        :return:
        """

        if self.execute_status:
            self.execute_status = flag

    async def gen_logs(self):
        """
        日志格式化并缓存redis
        :return:
        """

        self.case_logs = [v for k, v in self.al.case_logs_dict.items()]
        case_logs_json = json.dumps(self.case_logs, ensure_ascii=False)
        if self.is_debug:
            self.sio.log(f"=== 用例日志 ===\n{case_logs_json}")

        self.scenario_logs = [v for k, v in self.al.scenario_logs_dict.items()]
        scenario_logs_json = json.dumps(self.scenario_logs, ensure_ascii=False)
        if self.is_debug:
            self.sio.log(f"=== 场景日志 ===\n{scenario_logs_json}")

        self.result_summary = await self.test_result.get_test_result()

        self.redis_key = f"api_test_log:{F.gen_datetime(**{'execute': True})}_{F.gen_uuid_short()}"

        return_case_result = {
            "uuid": self.redis_key,
            "execute_user_id": self.execute_user_id,
            "execute_username": self.execute_username,
            "execute_key": self.execute_key,
            "execute_type": self.execute_type,
            "execute_name": self.execute_name,
            "case_logs": self.case_logs,
            "scenario_logs": self.scenario_logs,
            "ui_case_logs": [],  # 兼容测试报告数据结构
            "result_summary": self.result_summary
        }
        json_str = json.dumps(return_case_result, ensure_ascii=False)

        if self.is_debug:
            self.sio.log(f'=== json_str ===\n{json_str}')

        R.set(self.redis_key, json_str)
        R.expire(self.redis_key, 86400 * 30)
        # await self.aio_redis.set(self.redis_key, json_str)
        # await self.aio_redis.expire(self.redis_key, 86400 * 30)

        current_save_dict = GlobalsDict.redis_first_logs_dict(execute_id=self.execute_id)
        save_obj_first = current_save_dict.get(self.execute_key, "未知执行标识")
        R.set(save_obj_first, json_str)
        R.expire(save_obj_first, 86400 * 30)
        # await self.aio_redis.set(save_obj_first, json_str)
        # await self.aio_redis.expire(save_obj_first, 86400 * 30)

        self.sio.log('=== 生成日志写入Redis完成 ===', status="success")

    async def save_logs(self, report_url=None, file_name=None):
        """
        日志上层信息写入mysql
        :param report_url: 报告地址
        :param file_name: 文件名称
        :return:
        """

        sql = """INSERT INTO exile5_test_execute_logs (`is_deleted`, `create_time`, `create_timestamp`,  `project_id`, `execute_id`, `execute_name`, `execute_key`, `execute_type`, `redis_key`, `report_url`, `execute_status`, `creator`, `creator_id`, `trigger_type`, `file_name`) VALUES (0,'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}','{}');""".format(
            F.gen_datetime(),
            int(self.start_time),
            self.project_id,
            self.execute_id,
            self.execute_name,
            self.execute_key,
            self.execute_type,
            self.redis_key,
            report_url,
            self.execute_status,
            self.execute_username,
            self.execute_user_id,
            self.trigger_type,
            file_name
        )
        # project_db.insert(sql)
        await self.aio_db.execute(sql)
        self.sio.log(f'=== save_logs sql ===\n{sql}')
        self.sio.log('=== save_logs ok ===', status="success")

    async def gen_report_url(self):
        """生产测试报告链接"""

        try:
            conf = config_obj['new']
            host = conf.RUN_HOST
            port = conf.RUN_PORT
            report_url = f'http://{host}:{port}/api/case_report/{self.redis_key}'  # 测试报告地址
        except BaseException as e:
            report_url = f'http://0.0.0.0:5000/api/case_report/{self.redis_key}'  # 测试报告地址

        return report_url

    async def write_back_logs(self, report_url=None, file_name=None):
        """
        回写日志标识:替代 save_logs 方法
        """

        sql = """UPDATE exile5_test_execute_logs SET redis_key='{}', report_url='{}', execute_status={}, file_name='{}', update_time='{}', update_timestamp={} WHERE id={};""".format(
            self.redis_key,
            report_url,
            int(self.execute_status),
            file_name,
            GlobalsDict.gen_datetime(),
            int(time.time()),
            self.execute_logs_id
        )
        await self.aio_db.execute(sql)
        self.sio.log(f'=== write_back_logs sql ===\n{sql}')
        self.sio.log('=== write_back_logs ok ===', status="success")

    async def case_loader(self):
        """用例加载执行"""

        case_task = [
            asyncio.create_task(self.case_task(case_index, case)) for case_index, case in enumerate(self.case_list, 1)
        ]
        await asyncio.wait(case_task)

    async def scenario_loader(self):
        """场景加载执行"""

        scenario_task = [
            asyncio.create_task(self.scenario_task(scenario_index, scenario)) for scenario_index, scenario in
            enumerate(self.scenario_list, 1)
        ]
        await asyncio.wait(scenario_task)

    async def main(self):
        """main"""

        # 生成日志数据结构
        await self.al.gen_case_logs_dict(case_list=self.case_list)
        await self.al.gen_scenario_logs_dict(scenario_list=self.scenario_list)

        # 设置总用例/场景数
        self.test_result.start_time = time.time()
        await self.test_result.set_count(
            test_case_count=len(self.al.case_logs_dict),
            test_scenario_count=len(self.al.scenario_logs_dict)
        )

        if self.is_debug:
            print(json.dumps(self.al.case_logs_dict, ensure_ascii=False))
            print("=" * 100)
            print(json.dumps(self.al.scenario_logs_dict, ensure_ascii=False))

        # 开始时间戳
        self.start_time = time.time()

        if self.case_list:
            await self.case_loader()

        if self.scenario_list:
            await self.scenario_loader()

        await self.gen_logs()  # 日志格式化并缓存redis

        # await self.save_logs()  # 日志上层信息写入mysql

        await self.write_back_logs()  # 回写redis_key等数据

        if self.is_debug:
            print('obj_id_list', self.obj_id_list)

        report_url = await self.gen_report_url()
        print("=== report_url ===")
        print(report_url)

        if self.use_dd_push:

            start_time = self.result_summary.get('start_time')
            end_time = self.result_summary.get('end_time')
            total_time = self.result_summary.get('total_time')
            all_test_count = self.result_summary.get('all_test_count')
            pass_count = self.result_summary.get('pass_count')
            fail_count = self.result_summary.get('fail_count')
            pass_rate = self.result_summary.get('pass_rate')
            markdown_text = f"#### 测试报告:{self.execute_name}  \n  > 测试人员:{self.execute_username}  \n  > 开始时间:{start_time}  \n  > 结束时间:{end_time}  \n  > 合计耗时:{total_time}s  \n  > 用例总数:{all_test_count}  \n  > 成功数:{pass_count}  \n  > 失败数:{fail_count}  \n  > 通过率:{pass_rate}  \n "
            try:
                MessagePush.ding_ding_push(
                    ding_talk_url=self.ding_talk_url,
                    report_url=report_url,
                    markdown_text=markdown_text
                )
                error_info = ""
                status = 1
            except BaseException as e:
                print(str(e))
                error_info = traceback.format_exc()
                status = 2

            sql = f"""INSERT INTO exile5_ding_ding_push_logs (`send_message`, `error_info`, `status`) VALUES ('{markdown_text}', '{error_info}', {status});"""
            print(sql)
            await self.aio_db.execute(sql=sql)
