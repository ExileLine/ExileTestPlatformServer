# -*- coding: utf-8 -*-
# @Time    : 2022/3/23 4:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_send_api.py
# @Software: PyCharm

from decimal import Decimal

from all_reference import *


def var_conversion(before_var):
    """变量转换参数"""

    before_var_init = before_var

    if isinstance(before_var_init, (list, dict)):
        before_var = json.dumps(before_var, ensure_ascii=False)

    result_list = re.findall('\\$\\{([^}]*)', before_var)

    if not result_list:
        return before_var_init

    err_var_list = []
    current_dict = {}
    for res in result_list:
        sql = f"""select id, var_name, var_value, var_type, is_active from exile_test_variable where var_name='{res}' and is_deleted=0;"""
        query_result = project_db.select(sql=sql, only=True)
        if query_result:
            var_value = query_result.get('var_value')
            var_type = str(query_result.get('var_type'))
            if var_type in var_func_dict.keys():  # 函数
                new_val = var_func_dict.get(var_type)()
                current_dict[res] = new_val
            else:
                current_dict[res] = json.loads(var_value)

        elif var_func_dict.get(res):
            current_dict[res] = var_func_dict.get(res)
        else:
            err_var_list.append(res)
    if not current_dict:
        return before_var_init

    current_str = before_var
    for k, v in current_dict.items():
        old_var = "${%s}" % (k)
        new_var = v
        current_str = current_str.replace(old_var, new_var)
    if isinstance(before_var_init, (list, dict)):
        current_str = json.loads(current_str)
    return current_str


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
        send = {
            "url": base_url + url if base_url else url,
            "headers": request_headers,
        }
        req_json_data = req_type_dict.get(str(request_body_type))

        method = request_method.lower()

        if method == 'get':
            send['params'] = request_params
            __key = "params"
        else:
            send.update(req_json_data)
            __key = "json" if "json" in send else "data"

        send = var_conversion(send)

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
