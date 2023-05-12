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
    def execute_key_tuple(cls):
        """执行key"""

        t = (
            "case", "scenario",
            "project_all", "project_case", "project_scenario",
            "version_all", "version_case", "version_scenario",
            "task_all", "task_case", "task_scenario",
            "module_all", "module_case", "module_scenario", "module_app"
        )
        return t

    @classmethod
    def execute_type_tuple(cls):
        """执行类型"""

        t = ("case", "scenario", "project", "version", "task", "module")
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


class FieldListRender:
    """fieldList"""

    mode_list = [
        {"value": "ID", 'label': 'id'},
        {"value": "XPATH", 'label': 'xpath'},
        {"value": "NAME", 'label': 'name'},
        {"value": "TAG_NAME", 'label': 'tag name'},
        {"value": "CLASS_NAME", 'label': 'class name'},
        {"value": "CSS_SELECTOR", 'label': 'css selector'},
        {"value": "LINK_TEXT", 'label': 'link text'},
        {"value": "PARTIAL_LINK_TEXT", 'label': 'partial link text'}
    ]

    @classmethod
    def mode_dict(cls, label: str = "定位方式") -> dict:
        """定位方式目标对象"""

        res = {
            "value": "mode",
            "label": label,
            "component": "t-select",
            "list": cls.mode_list
        }
        return res

    @classmethod
    def ele_value_dict(cls, label: str = "元素") -> dict:
        """元素模板对象"""

        res = {
            "value": "value",
            "label": label,
            "component": 't-input'
        }
        return res

    @classmethod
    def ele_data_dict(cls, label: str = "值") -> dict:
        """值模板对象"""

        res = {
            "value": "data",
            "label": label,
            "component": 't-input'
        }
        return res


class RulesRender:
    """rules"""

    @classmethod
    def rules(cls, trigger: str, message: str, required: bool = True) -> list:
        """下拉框/输入框验证规则"""

        if trigger not in ("change", "blur"):
            raise TypeError(f"模板渲染失败，验证规则 {trigger} 不存在")

        res = [
            {
                "required": required,
                "message": message,
                "type": "error",
                "trigger": trigger
            }
        ]
        return res


class ExtraRender:
    """extra"""

    @classmethod
    def extra(cls, lw: (int, float)) -> dict:
        """输入框宽度"""

        res = {
            "label-width": f"{lw}em"
        }
        return res


class TemplateRender(FieldListRender, RulesRender, ExtraRender):
    """组件渲染"""

    @classmethod
    def common_dict(cls, label: str = "通用模板") -> dict:
        """通用模板"""

        res = {
            "value": "num",
            "label": label,
            "component": 't-input'
        }
        return res


class UiControlDict(TemplateRender):
    """UI控件字典"""

    ui_control_list = [
        {
            "title": '启动浏览器(URL)',
            "type": 'ui_control',
            "function": "open",
            "args": {
                "url": ""
            }
        },
        {
            "title": "关闭(quit)",
            "type": "ui_control",
            "function": "close",
            "args": {},
        },
        {
            "title": "输入(input)",
            "type": "ui_control",
            "function": "input",
            "args": {
                "data": "",
                "mode": "",  # XPATH
                "value": ""  # //*[@id=\"login-form\"]/div[1]/div[2]/div/div/div/input
            },
        },
        {
            "title": "点击(click)",
            "type": "ui_control",
            "function": "click",
            "args": {
                "mode": "",
                "value": ""
            },
        },
        {
            "title": "清空输入框(clear)",
            "type": "ui_control",
            "function": "clear",
            "args": {
                "mode": "",
                "value": ""
            },
        },
        {
            "title": "获取文本(text)",
            "type": "ui_control",
            "function": "text",
            "args": {
                "mode": "",
                "value": "",
                "data": ""
            },
        },
        {
            "title": "键盘事件",
            "type": "ui_control",
            "function": "keyboard",
            "args": {}
        },
        {
            "title": "鼠标事件",
            "type": "ui_control",
            "function": "mouse",
            "args": {}
        },
        {
            "title": "调用其他UI用例",
            "type": "ui_control",
            "function": "other_case",
            "args": {}
        },
        {
            "title": "等待",
            "type": "ui_control",
            "function": "sleep",
            "args": {}
        },
    ]

    api_control_list = [
        {
            "title": "已有Api",
            "type": "api_control",
            "function": "api",
            "args": {}
        },
        {
            "title": "外部Api",
            "type": "api_control",
            "function": "api3",
            "args": {}
        },
        {
            "title": "OpenApi",
            "type": "api_control",
            "function": "open_api",
            "args": {}
        },
        {
            "title": "其他",
            "type": "api_control",
            "function": "other_api",
            "args": {}
        },
    ]

    assert_control_list = [
        {
            "title": "ui(页面)",
            "type": "assert_control",
            "function": "assert_ui",
        },
        {
            "title": "api(响应)",
            "type": "assert_control",
            "function": "assert_api",
        },
        {
            "title": "数据(db)",
            "type": "assert_control",
            "function": "assert_db",
        },
        {
            "title": "其他",
            "type": "assert_control",
            "function": "assert_order",
        }
    ]

    logic_control_list = [
        {
            "title": "循环(for)",
            "type": "logic_control",
            "function": "for",
            "num": 1,
            "data_source": [],
            "business_list": []
        },
        {
            "title": "判断(if)",
            "type": "logic_control",
            "function": "if",
            "business_list": []
        },
        {
            "title": "进入下次循环(continue)",
            "type": "logic_control",
            "function": "continue"
        },
        {
            "title": "终止循环(break)",
            "type": "logic_control",
            "function": "break"
        },
        {
            "title": "异常捕获(try)",
            "type": "logic_control",
            "function": "try",
            "business_list": []
        },
        {
            "title": "变量(var)",
            "type": "logic_control",
            "function": "var",
            "business_list": []
        },
    ]

    @classmethod
    def get_uc_dict(cls):
        """获取UI控件字典(页面左边的控件tag块)"""

        result = [
            {
                "title": "Ui",
                "type": "ui_control",
                "control_list": cls.ui_control_list,
            },
            {
                "title": "Api",
                "type": "api_control",
                "control_list": cls.api_control_list,
            },
            {
                "title": "断言",
                "type": "assert_control",
                "control_list": cls.assert_control_list,
            },
            {
                "title": "逻辑",
                "type": "logic_control",
                "control_list": cls.logic_control_list,
            },
        ]

        return result

    @classmethod
    def get_uc_mapping(cls):
        """获取UI控件映射(控件tag块弹窗细节渲染)"""

        ui_dict = {
            "demo": {
                "fieldList": [
                    {
                        "value": "input",
                        "label": "输入框",
                        "component": "t-input",
                    },
                    {
                        "value": "select",
                        "label": "下拉",
                        "component": "t-select",
                        "list": [
                            {"version_name": "xxx", "id": 1}
                        ],
                        "extraProps": {
                            "url": "/api/project_version_page",
                            "labelKey": "version_name",
                            "valueKey": "id",
                        },
                    },
                    {
                        "value": "list",
                        "label": "多选下拉",
                        "component": "remote-select",
                        "extraProps": {
                            "url": "/api/module_app_page",
                            "labelKey": "module_name",
                            "valueKey": "id",
                            "valueType": "object",  # 写object就是传对象，不要这个key就传id，即传valueKey
                            "multiple": True,
                        }
                    }
                ],
                "rules": {
                    "input": [
                        {
                            "required": True,
                            "message": "请输入xxx'",  # 验证错误提示
                            "type": "error",
                            "trigger": "blur",  # select用change，input用blur
                        }
                    ],
                    "select": [
                        {
                            "required": True,
                            "message": "请选择xxx'",  # 验证错误提示
                            "type": "error",
                            "trigger": "change",  # select用change，input用blur
                        }
                    ],
                    "list": [
                        {
                            "required": True,
                            "message": "请选择xxx'",  # 验证错误提示
                            "type": "error",
                            "trigger": "change",  # select用change，input用blur
                        }
                    ]
                },
                "extra": {
                    "label-width": "4em"
                }
            },
            "open": {
                "fieldList": [
                    {
                        "value": "url",
                        "label": "URL",
                        "component": 't-input',
                    }
                ],
                "rules": {
                    "url": cls.rules("blur", "请输入url")
                },
                "extra": cls.extra(4.5)
            },
            "input": {
                "fieldList": [
                    cls.mode_dict(),
                    cls.ele_value_dict(),
                    cls.ele_data_dict()
                ],
                "rules": {
                    "mode": cls.rules("change", "请选择定位方式"),
                    "value": cls.rules("blur", "请输入元素")
                },
                "extra": cls.extra(5.5)
            },
            "click": {
                "fieldList": [
                    cls.mode_dict(),
                    cls.ele_value_dict(),
                ],
                "rules": {
                    "mode": cls.rules("change", "请选择定位方式"),
                    "value": cls.rules("blur", "请输入元素")
                },
                "extra": cls.extra(5.5)
            },
            "clear": {
                "fieldList": [
                    cls.mode_dict(),
                    cls.ele_value_dict(),
                ],
                "rules": {
                    "mode": cls.rules("change", "请选择定位方式"),
                    "value": cls.rules("blur", "请输入元素")
                },
                "extra": cls.extra(5.5)
            },
            "text": {
                "fieldList": [
                    cls.mode_dict(),
                    cls.ele_value_dict(),
                    cls.ele_data_dict(label="临时变量名称")
                ],
                "rules": {
                    "mode": cls.rules("change", "请选择定位方式"),
                    "value": cls.rules("blur", "请输入元素"),
                    "data": cls.rules("blur", "请输入临时变量名称")
                },
                "extra": cls.extra(7.5)
            },
            "sleep": {
                "fieldList": [
                    cls.common_dict(label="等待时间(s)")
                ],
                "rules": {
                    "num": cls.rules("blur", "请输入等待时间(s)"),
                },
                "extra": cls.extra(6.5)
            }
        }

        logic_dict = {
            "for": {
                "fieldList": [
                    cls.common_dict(label="循环次数")
                ],
                "rules": {
                    "num": cls.rules("blur", "输入循环次数"),
                },
                "extra": cls.extra(6.5)
            }
        }

        result = {
            **ui_dict,
            **logic_dict
        }
        return result


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
