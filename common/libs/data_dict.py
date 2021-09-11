# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 5:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : data_dict.py
# @Software: PyCharm

import json

# RespAssertionRuleApi 新增,编辑时候使用
rule_save_dict = {
    "=": 1,
    "<": 2,
    ">": 3,
    "<=": 4,
    ">=": 5,
    "!=": 6,
    "in": 7,
    "not in": 8
}

# RespAssertionRuleApi 新增,编辑时候使用
expect_val_type_dict = {
    '1': int,
    '2': str,
    '3': list,
    # '4': dict("{}".format(data)),
    '4': json.loads,
    '5': json.dumps
}

rule_dict = {
    '==': '__eq__',
    '>': '__gt__',
    '>=': '__ge__',
    '<': '__lt__',
    '<=': '__le__',
    '!=': '__ne__',
    'in': '__contains__'
}

if __name__ == '__main__':
    a = "123"
    # a = 123
    print(expect_val_type_dict.get('1')(a))
    print(expect_val_type_dict.get('2')(a))
    print(expect_val_type_dict.get('3')(a))
    print(expect_val_type_dict.get('4')(a))
    print(expect_val_type_dict.get('5')(a))
