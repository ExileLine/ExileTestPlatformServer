# -*- coding: utf-8 -*-
# @Time    : 2022/3/23 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_send_api.py
# @Software: PyCharm

from decimal import Decimal

from all_reference import *
from common.libs.CaseDrivenResult import MainTest


class CaseReqTestApi(MethodView):
    """
    test send
    """

    def post(self):
        data = request.get_json()
        request_method = data.get('request_method')
        base_url = data.get('request_base_url')
        url = data.get('request_url')
        request_headers = data.get('request_headers', {})
        request_params = data.get('request_params', {})
        request_body = data.get('request_body', {})
        request_body_type = data.get('request_body_type')

        req_type_dict = {
            "1": {"data": request_body},
            "2": {"json": request_body},
            "3": {"data": request_body}
        }

        method = request_method.lower()
        if method == 'get':
            if "?" in url:
                url = url.split("?")[0]

        send = {
            "url": base_url + url if base_url else url,
            "headers": request_headers,
        }

        req_json_data = req_type_dict.get(str(request_body_type))

        if method == 'get':
            send['params'] = request_params
            __key = "params"
        else:
            send.update(req_json_data)
            __key = "json" if "json" in send else "data"

        send = MainTest().var_conversion(send)

        if not hasattr(requests, method):
            return api_result(code=400, message=f'请求方式:{method}不存在')

        start_time = time.time()
        response = getattr(requests, method)(**send, verify=False)
        end_time = time.time()

        try:
            response_content = response.json()
        except BaseException as e:
            response_content = {
                "code": 500,
                "message": response.text
            }
        data = {
            "request_url": send.get('url'),
            "request_method": request_method,
            "request_body_type": __key,
            "request_headers": dict(send.get('headers', {})),
            "request_content": send.get(__key),
            "response_headers": dict(response.headers),
            "response_content": response_content,
            "http_code": response.status_code,
            "time": f"{Decimal((end_time - start_time) * 1000).quantize(Decimal('1'))}ms"
        }
        return api_result(code=200, message='操作成功', data=data)
