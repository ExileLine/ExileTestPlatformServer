# -*- coding: utf-8 -*-
# @Time    : 2021/9/2 5:38 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : data_dict.py
# @Software: PyCharm

import json
import time
import datetime
import random
import string
import operator

import shortuuid


class F:

    @classmethod
    def gen_length(cls, *args, **kwargs):
        """生成数据长度"""

        length = kwargs.get('length')
        if isinstance(length, int) and length:
            return length
        return 6

    @classmethod
    def gen_uuid_long(cls, *args, **kwargs):
        return shortuuid.uuid()[0:11] + str(int(time.time())) + shortuuid.uuid()[0:11]

    @classmethod
    def gen_uuid_short(cls, *args, **kwargs):
        return shortuuid.uuid()[0:16]

    @classmethod
    def gen_date(cls, *args, **kwargs):
        """
        日期:年月日 -> 2020-01-17
        time.strftime("%Y-%m-%d")
        str(datetime.datetime.now().date())
        :return:
        """
        if kwargs.get('func'):
            return datetime.datetime.now().date()
        return time.strftime("%Y-%m-%d")

    @classmethod
    def gen_time(cls, *args, **kwargs):
        """
        时间:时分秒 -> 18:30:33
        str(datetime.datetime.now().time()).split('.')[0]
        time.strftime("%H:%M:%S")
        :return:
        """
        if kwargs.get('func'):
            return datetime.datetime.now().time()
        return time.strftime("%H:%M:%S")

    @classmethod
    def gen_datetime(cls, *args, **kwargs):
        """
        日期:年月日时分秒 -> 2020-01-17 18:30:33
        time.strftime("%Y-%m-%d %H:%M:%S")
        str(datetime.datetime.now()).split('.')[0]
        :return:
        """
        if kwargs.get('func'):
            return datetime.datetime.now()
        if kwargs.get('execute'):
            return time.strftime("%Y-%m-%d_%H-%M-%S")
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def gen_timestamp(cls, key=None, *args, **kwargs):
        """
        时间戳
        10位: str(int(time.time()))
        13位: str(int(time.time() * 1000))
        :return:
        """
        if key:
            return str(int(time.time() * 1000))
        else:
            return str(int(time.time()))

    @classmethod
    def gen_random_int(cls, *args, **kwargs):
        """
        生成随机数字
        :return: 随机数字
        """

        length = cls.gen_length(*args, **kwargs)
        random_int = ''.join(random.choice(string.digits) for _ in range(length))
        if random_int[0] == '0':
            random_int += random.choice(string.digits)
        return int(random_int)

    @classmethod
    def gen_random_str(cls, *args, **kwargs):
        """
        生成随机字符串
        :return: 随机字符串
        """

        length = cls.gen_length(*args, **kwargs)
        random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return random_str

    @classmethod
    def gen_random_str_number(cls, *args, **kwargs):
        """
        生成随机字符串数字
        :return: 随机字符串数字
        """

        length = cls.gen_length(*args, **kwargs)
        random_str_number = ''.join(random.choice(string.digits) for _ in range(length))
        return random_str_number

    @classmethod
    def gen_random_bool(cls, *args, **kwargs):
        """
        生成随机布尔值
        :return:
        """

        return random.choice([True, False])


class GlobalsDict(F):
    """全局字典"""

    @classmethod
    def method_dict(cls):
        """请求方式"""

        d = {
            "GET": "",
            "POST": "",
            "PUT": "",
            "DELETE": "",
            "PATCH": ""
        }
        return d

    @classmethod
    def json_func(cls, x):
        try:
            return json.loads(x)
        except BaseException as e:
            return {}

    @classmethod
    def request_body_type_func(cls):
        """请求参数类型"""

        def_func = lambda x="": x
        d = {
            "none": lambda x=None: '',
            "form-data": cls.json_func,
            "x-form-data": cls.json_func,
            "json": cls.json_func,
            "text": def_func,
            "html": def_func,
            "xml": def_func
        }
        return d

    @classmethod
    def resp_source_tuple(cls):
        """返回值来源"""

        t = ("response_body", "response_headers")
        return t

    @classmethod
    def var_source_tuple(cls):
        """变量来源"""

        t = ("response_body", "response_headers")
        return t

    @classmethod
    def rule_dict_py(cls):
        """
        规则字典(Python内置双下划线方法)
        eq      : equal（等于）
        gt      : greater than（大于）
        ge      : greater and equal（大于等于）
        lt      : less than（小于）
        le      : less and equal（小于等于）
        ne      : not equal (不等于)
        contains: in
        """

        d = {
            "==": "__eq__",
            ">": "__gt__",
            ">=": "__ge__",
            "<": "__lt__",
            "<=": "__le__",
            "!=": "__ne__",
            "in": "__contains__",
            "not_in": ""
        }
        return d

    @classmethod
    def rule_dict_op(cls):
        """规则字典(Python内置函数operator封装后的方法)"""

        d = {
            "==": "eq",
            ">": "gt",
            ">=": "ge",
            "<": "lt",
            "<=": "le",
            "!=": "ne",
            "in": "contains",
            "not_in": ""
        }
        return d

    @classmethod
    def value_type_dict(cls):
        """数据类型"""

        d = {
            "int": int,
            "str": str,
            "float": float,
            "list": list,
            "dict": dict,
            "bool": bool,
            "json": json.loads,
            "json_str": json.dumps,
        }
        return d

    @classmethod
    def variable_type_dict(cls, merge=True):
        """
        变量类型字典
        :param merge: 默认合并数据类型字典
        :return:
        """

        d = {
            "random_int": cls.gen_random_int,
            "random_str": cls.gen_random_str,
            "random_str_number": cls.gen_random_str_number,
            "random_bool": cls.gen_random_bool,
            "date": cls.gen_date,
            "time": cls.gen_time,
            "datetime": cls.gen_datetime,
            "timestamp": cls.gen_timestamp,
            "uuid_short": cls.gen_uuid_short,
            "uuid_long": cls.gen_uuid_long
        }
        if merge:
            d.update(cls.value_type_dict())
        return d

    @classmethod
    def variable_args_dict(cls):
        """变量扩展参数key"""

        t = ("length", "test")
        return t

    @classmethod
    def test_dict(cls, l, r):
        """测试"""

        print(f'{l} == {r}', operator.eq(l, r))
        print(f'{l} > {r}', operator.gt(l, r))
        print(f'{l} >= {r}', operator.ge(l, r))
        print(f'{l} < {r}', operator.lt(l, r))
        print(f'{l} <= {r}', operator.le(l, r))
        print(f'{l} != {r}', operator.ne(l, r))
        print(f'{l} in {r}', operator.contains(str(l), str(r)))

        from types import MethodType, FunctionType
        for k, v in cls.variable_type_dict().items():
            # if isinstance(v, MethodType):
            #     print("MethodType", k)

            # if isinstance(v, FunctionType):
            #     print("FunctionType", k)

            # if isinstance(v, type):
            #     print("type", k)
            print(k, v.__class__)

    @classmethod
    def execute_type_tuple(cls):
        """执行类型"""

        t = (
            "case", "scenario",
            "project_all", "project_case", "project_scenario",
            "version_all", "version_case", "version_scenario",
            "task_all", "task_case", "task_scenario",
            "module_all", "module_case", "module_scenario",
            "module_app",
        )
        return t

    @classmethod
    def redis_first_logs_dict(cls, execute_id):
        """
        redis最新日志存储字典
        :param execute_id:
        :return:
        """

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
            "module_scenario": f"module_scenario_first_log:{execute_id}",
            "ui_case": f"ui_case_first_log:{execute_id}",
            "ui_project_all": f"ui_project_all_first_log:{execute_id}",
            "ui_version_all": f"ui_version_all_first_log:{execute_id}",
            "ui_task_all": f"ui_task_all_first_log:{execute_id}",
            "ui_module_all": f"ui_module_all_first_log:{execute_id}",
        }
        return d


"""断言相关"""

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

rule_dict = {
    '==': '__eq__',
    '>': '__gt__',
    '>=': '__ge__',
    '<': '__lt__',
    '<=': '__le__',
    '!=': '__ne__',
    'in': '__contains__'
}

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

if __name__ == '__main__':
    pass
    a = "123a"
    # a = 123
    # type_conversion(1, a)
    # type_conversion(2, a)
    # type_conversion(3, a)
    # type_conversion(4, a)
    # type_conversion(5, a)
    # type_conversion(6, a)

    # GlobalsDict.test_dict(1, 2)
    print(GlobalsDict.gen_uuid_long(), len(GlobalsDict.gen_uuid_long()))
    print(GlobalsDict.gen_uuid_short(), len(GlobalsDict.gen_uuid_short()))
    print(GlobalsDict.gen_date())
    print(GlobalsDict.gen_time())
    print(GlobalsDict.gen_datetime())
    print(GlobalsDict.gen_timestamp())
    print(GlobalsDict.gen_random_int())
    print(GlobalsDict.gen_random_str())
    print(GlobalsDict.gen_random_str_number())
    print(GlobalsDict.gen_random_bool())
