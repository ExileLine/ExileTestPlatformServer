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
        """取值规程调试"""
        data = request.get_json()
        val_exp = data.get('val_exp', "")
        data_source = data.get('data_source', {})

        result = execute_code(code=val_exp, data=data_source)

        return api_result(
            code=200 if result.get('bool') else 400,
            message=result.get('message'),
            data=result.get('result_data')
        )
