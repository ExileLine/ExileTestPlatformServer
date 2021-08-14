# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 5:03 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : rule_test_api.py
# @Software: PyCharm

from app.all_reference import *


class RuleTestApi(MethodView):
    """
    取值规程调试Api

    get_dict_val_demo = {
        "rule_str": "okc.get('a').get('b').get('c')",
        "data_self": {
            "a": {
                "b": {
                    "c": [
                        1,
                        2,
                        3
                    ]
                }
            }
        }
    }

    get_list_val_demo = {
        "rule_str": "d[0].get('a')[0]",
        "data_self": [
            {
                "a": [
                    {
                        "b": "b"
                    }
                ]
            }
        ]
    }

    get_str_val_demo = {
        "rule_str": "x[0:3]",
        "data_self": "123456789"
    }

    """

    def post(self):
        """1"""
        data = request.get_json()
        rule_str = data.get('rule_str', "")
        data_self = data.get('data_self', {})
        data_type = data.get('data_type', {})
        print(rule_str)
        print(data_self)

        if isinstance(data_self, dict):
            d = data_self
            rs = rule_str.split('.')
            rs[0] = 'd'
            new_rule_str = '.'.join(rs)
        elif isinstance(data_self, list):
            d = data_self
            rs = rule_str.split("[")
            rs[0] = 'd'
            new_rule_str = '['.join(rs)
        elif isinstance(data_self, str):
            # todo 切片,函数,正则
            # d = data_self
            # rs = rule_str.split("[")
            # rs[0] = 'd'
            new_rule_str = rule_str

        else:
            return api_result(code=400, message='取值参数主体类型应该为:JSON,Dict,List,Str')

        print("exec:{}".format(new_rule_str))

        try:
            _locals = locals()
            # print(globals())
            # print(_locals)
            exec("""rule_result={}""".format(new_rule_str), globals(), _locals)
            rule_result = _locals['rule_result']
        except BaseException as e:
            return api_result(code=400, message='取值规则语法错误:{}:,错误原因:{}'.format(rule_str, str(e)))

        if rule_result:
            resp_data = {
                "bool": True,
                "result_data": rule_result
            }
            return api_result(code=200, message='取值规则正确', data=resp_data)
        else:
            resp_data = {
                "bool": False,
                "result_data": None
            }
            return api_result(code=400, message='未找到对应的值,请检查取值规则', data=resp_data)
