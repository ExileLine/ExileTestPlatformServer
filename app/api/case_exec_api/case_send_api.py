# -*- coding: utf-8 -*-
# @Time    : 2022/3/23 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_send_api.py
# @Software: PyCharm

from all_reference import *


class CaseReqTestApi(MethodView):
    """
    test send
    """

    def post(self):
        data = request.get_json()
        method = data.get('method')
        base_url = data.get('base_url')
        url = data.get('url')
        headers = data.get('headers', {})
        req_type = data.get('req_type')
        body = data.get('body', {})

        send = {
            "url": base_url + url if base_url else url,
            "headers": headers,
            req_type: body
        }

        if req_type not in ["params", "data", "json"]:
            return api_result(code=400, message='req_type 应该为:{}'.format(["params", "data", "json"]))

        try:
            if hasattr(requests, method):
                response = getattr(requests, method)(**send, verify=False)
                data = {
                    "response": response.json(),
                    "response_headers": dict(response.headers)
                }
                return api_result(code=200, message='操作成功', data=data)
            else:
                return api_result(code=400, message='请求方式:{}不存在'.format(method))
        except BaseException as e:
            return api_result(code=400, message='请求方式失败:{}'.format(str(e)))
