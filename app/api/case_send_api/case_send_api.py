# -*- coding: utf-8 -*-
# @Time    : 2022/3/23 4:12 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_send_api.py
# @Software: PyCharm

from decimal import Decimal

from all_reference import *
from common.libs.async_test_runner.async_runner import AsyncCaseRunner

params_key = [
    ("request_base_url", "请求地址"),
    ("request_url", "接口"),
    ("request_method", "请求方式")
]


class CaseRequestSendApi(MethodView):
    """
    Send用例调试与Postman相似
    """

    async def post(self):
        """用例调试"""

        data = request.get_json()
        project_id = data.get('project_id')
        request_base_url = data.get('request_base_url')
        request_url = data.get('request_url')
        request_method = data.get('request_method')
        request_params_hash = data.get('request_params_hash', [])
        request_params = gen_request_dict(request_params_hash)
        request_headers_hash = data.get('request_headers_hash', [])
        request_headers = gen_request_dict(request_headers_hash)
        request_body_type = data.get('request_body_type')
        _func = GlobalsDict.request_body_type_func().get(request_body_type)
        request_body_hash = data.get('request_body_hash')
        request_body = _func(request_body_hash)

        check_bool, check_msg = RequestParamKeysCheck(data, params_key).result()
        if not check_bool:
            return api_result(code=NO_DATA, message=check_msg)

        try:
            url = request_base_url + request_url
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
                "headers": request_headers,
                "payload": {},
            }
            req_json_data = req_type_dict.get(request_body_type)

            if not req_json_data:
                before_send['payload']['params'] = request_params
            else:
                before_send['payload'].update(req_json_data)

            acr = AsyncCaseRunner(test_obj={"project_id": project_id})
            send = await acr.var_conversion(before_send)
            url = send.get('url')
            headers = send.get('headers')
            payload = send.get('payload')

            start_time = time.time()
            response = await acr.current_request(method=request_method, url=url, headers=headers, **payload)
            end_time = time.time()

            response_headers = response.get("resp_headers")
            response_body = response.get("resp_json")
            http_code = response.get('http_code')

            result = {
                "url": url,
                "request_method": request_method,
                "request_body_type": request_body_type,
                "request_headers": request_headers,
                "request_params": request_params,
                "request_body": request_body,
                "response_headers": response_headers,
                "response_body": response_body,
                "http_code": http_code,
                "time": f"{Decimal((end_time - start_time) * 1000).quantize(Decimal('1'))}ms"
            }
            return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)
        except BaseException as e:
            return api_result(code=BUSINESS_ERROR, message=f'参数异常:{e}')
