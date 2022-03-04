# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 5:38 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : data_dict.py
# @Software: PyCharm

import json
import time
import datetime
import shortuuid

# 返回值来源
resp_source_tuple = ("response_body", "response_headers")

var_source_tuple = ('resp_data', 'resp_headers')

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

# 变量转换函数字典
var_func_dict = {
    "7": shortuuid.uuid()[0:10] + str(int(time.time())) + shortuuid.uuid()[0:10],  # uuid
    "8": shortuuid.uuid(),  # short_uuid
    "9": str(datetime.datetime.now().date()),  # date(年月日-2022-01-01)
    "10": str(datetime.datetime.now().time()),  # time(时分秒-09:30:00.123456)
    "11": str(datetime.datetime.now()),  # datetime(年月日时分秒-2022-01-01 09:30:00.123456)
    "12": str(int(time.time()))  # timestamp(时间戳)
}

# 执行类型
execute_type_tuple = (
    "case", "scenario",
    "project_all", "project_case", "project_scenario",
    "version_all", "version_case", "version_scenario",
    "task_all", "task_case", "task_scenario",
    "module_all", "module_case", "module_scenario"
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
    a = "123"
    # a = 123
    print(expect_val_type_dict.get('1')(a))
    print(expect_val_type_dict.get('2')(a))
    print(expect_val_type_dict.get('3')(a))
    print(expect_val_type_dict.get('4')(a))
    print(expect_val_type_dict.get('5')(a))
