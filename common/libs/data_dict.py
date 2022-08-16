# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 5:38 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : data_dict.py
# @Software: PyCharm

import json
import time
import datetime
import shortuuid
import operator

# print(operator.eq(1, 2))


"""请求方式"""
method_dict = {
    "GET": "",
    "POST": "",
    "PUT": "",
    "DELETE": "",
    "PATCH": ""
}

"""请求参数类型"""


def json_func(x):
    try:
        return json.loads(x)
    except BaseException as e:
        return {}


def_func = lambda x="": x
request_body_type_func = {
    "none": lambda x=None: '',
    "form-data": json_func,
    "x-form-data": json_func,
    "json": json_func,
    "text": def_func,
    "html": def_func,
    "xml": def_func
}

"""断言相关"""
# 返回值来源
resp_source_tuple = ("response_body", "response_headers")

var_source_tuple = ('resp_data', 'resp_headers')

# RespAssertionRuleApi, FieldAssertionRuleApi 新增,编辑时候使用
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

# RespAssertionRuleApi, FieldAssertionRuleApi 新增,编辑时候使用
expect_val_type_dict = {
    '1': int,
    '2': str,
    '3': list,
    # '4': dict("{}".format(data)),
    '4': json.loads,
    '5': json.dumps,
    '6': bool
}

"""
eq     :equal（等于）
gt     :greater than（大于）
ge     :greater and equal（大于等于）
lt     :less than（小于）
le     :less and equal（小于等于）
ne     :not equal (不等于)
contains: in
"""

rule_dict = {
    '==': '__eq__',
    '>': '__gt__',
    '>=': '__ge__',
    '<': '__lt__',
    '<=': '__le__',
    '!=': '__ne__',
    'in': '__contains__'
}

"""变量相关"""


def gen_shortuuid_1():
    return shortuuid.uuid()[0:10] + str(int(time.time())) + shortuuid.uuid()[0:10]


def gen_shortuuid_2():
    return shortuuid.uuid()


def gen_date():
    return str(datetime.datetime.now().date())


def gen_time():
    return str(datetime.datetime.now().time())


def gen_datetime():
    return str(datetime.datetime.now())


def gen_timestamp():
    return str(int(time.time()))


# 变量原生函数字典
var_native_func_dict = {
    "1": str,
    "2": int,
    "3": json.loads,
    "4": json.dumps,
    "5": json.loads,
    "6": json.dumps,

}

# 变量转换函数字典
var_func_dict = {
    "7": gen_shortuuid_1,  # uuid
    "8": gen_shortuuid_2,  # short_uuid
    "9": gen_date,  # date(年月日-2022-01-01)
    "10": gen_time,  # time(时分秒-09:30:00.123456)
    "11": gen_datetime,  # datetime(年月日时分秒-2022-01-01 09:30:00.123456)
    "12": gen_timestamp  # timestamp(时间戳)
}


def type_conversion(type_key, val, type_dict=None):
    """
    类型转换
    :param type_key: 类型字典key
    :param val: 需要转换的值
    :param type_dict: 使用那个字典
    :return:
    """
    if type_dict == 'ass':
        bf = expect_val_type_dict.get(str(type_key))
    else:
        bf = var_native_func_dict.get(str(type_key))
    print(bf)
    try:
        new_val = bf(val)
        print(f"值:{val}-{type(val)} 【func-{bf}】 {new_val}-{type(new_val)}")
        return True, new_val
    except BaseException as e:
        print(f'参数:{val} 无法转换至 类型:{bf} ERROR:{e}')
        return False, f'参数:{val} 无法转换至 类型:{bf}'


"""执行相关"""
# 执行类型
execute_type_tuple = (
    "case", "scenario",
    "project_all", "project_case", "project_scenario",
    "version_all", "version_case", "version_scenario",
    "task_all", "task_case", "task_scenario",
    "module_app", "module_all", "module_case", "module_scenario"
)

# 执行标签
execute_label_tuple = ('only', 'many', 'all')


# redis最新日志存储字典
def gen_redis_first_logs(execute_id):
    """redis最新日志存储字典"""
    d = {
        "case": f"case_first_log:{execute_id}",
        "scenario": f"scenario_first_log:{execute_id}",
        "project_all": f"project_all_first_log:{execute_id}",
        "project_case": f"project_case_first_log:{execute_id}",
        "project_scenario": f"project_scenario_first_log:{execute_id}",
        "version_all": f"version_all_first_log:{execute_id}",
        "version_case": f"version_case_first_log:{execute_id}",
        "version_scenario": f"version_scenario_first_log:{execute_id}",
        "task_all": f"task_all_first_log:{execute_id}",
        "task_case": f"task_case_first_log:{execute_id}",
        "task_scenario": f"task_scenario_first_log:{execute_id}",
        "module_app": f"module_app_first_log:{execute_id}",
        "module_all": f"module_all_first_log:{execute_id}",
        "module_case": f"module_case_first_log:{execute_id}",
        "module_scenario": f"module_scenario_first_log:{execute_id}"
    }
    return d


case_type_dict = {
    "1": "api自动化测试",
    "2": "ui自动化测试",
    "3": "性能测试",
    "4": "安全测试"
}

if __name__ == '__main__':
    a = "123a"
    # a = 123
    type_conversion(1, a)
    type_conversion(2, a)
    type_conversion(3, a)
    type_conversion(4, a)
    type_conversion(5, a)
    type_conversion(6, a)
