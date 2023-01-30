# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 11:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_runner.py
# @Software: PyCharm

import json
import shortuuid

from common.libs.BaseWebDriver import BaseWebDriver

web_ui_lib_dict = {
    "selenium": BaseWebDriver
}

child_master = {
    "uuid": shortuuid.uuid(),
    "index": 5,
    "title": "循环四(业务块)",
    "type": "master",
    "business_list": [
        {
            "uuid": shortuuid.uuid(),
            "index": 1,
            "type": "ui_control",
            "title": "循环四-点击控件1",
            "function": "click",
            "args": {}
        },
        {
            "uuid": shortuuid.uuid(),
            "index": 2,
            "type": "logic_control",
            "title": "循环控件",
            "function": "for",
            "num": 2,
            "data_source": [],
            "business_list": [
                {
                    "uuid": shortuuid.uuid(),
                    "index": 771,
                    "type": "ui_control",
                    "title": "循环四-内循环-点击控件2",
                    "function": "click",
                    "args": {}
                }
            ]
        }
    ]
}

meta_data = [
    {
        "uuid": shortuuid.uuid(),
        "index": 1,
        "title": "开始",
        "type": "master",
        "business_list": [
            {
                "uuid": shortuuid.uuid(),
                "index": 1,
                "type": "ui_control",
                "title": "启动浏览器控件",
                "function": "open",
                "args": {
                    "url": "https://www.github.com"
                }
            },
        ]
    },
    {
        "uuid": shortuuid.uuid(),
        "index": 2,
        "title": "登录",
        "type": "master",
        "business_list": [
            {
                "uuid": shortuuid.uuid(),
                "index": 1,
                "type": "ui_control",
                "title": "输入控件",
                "function": "input",
                "args": {
                    "username": "admin"
                }
            },
            {
                "uuid": shortuuid.uuid(),
                "index": 2,
                "type": "ui_control",
                "title": "输入控件",
                "function": "input",
                "args": {
                    "password": "123456"
                }
            },
            {
                "uuid": shortuuid.uuid(),
                "index": 3,
                "type": "ui_control",
                "title": "点击控件",
                "function": "click",
                "args": {}
            },
            {
                "uuid": shortuuid.uuid(),
                "index": 4,
                "title": "检验是否登录成功",
                "type": "master",
                "business_list": [
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 1,
                        "type": "assert_control",
                        "title": "UI断言控件",
                        "function": "ui_assert",
                        "args": {
                            "expected_results": "aaa",
                            "rule": "==",
                            "actual_results": "",
                            "actual_results_source": {
                                "source": "web_ui",
                                "args": {
                                    "web_ui": {},
                                    "api_response": {}
                                }
                            },
                        }
                    },
                ]
            },
        ]
    },
    {
        "uuid": shortuuid.uuid(),
        "index": 3,
        "title": "循环录入数据",
        "type": "master",
        "business_list": [
            {
                "uuid": shortuuid.uuid(),
                "index": 1,
                "type": "logic_control",
                "title": "循环控件",
                "function": "for",
                "num": 2,  # 调试
                "data_source": [],
                "business_list": [
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 1,
                        "type": "ui_control",
                        "title": "输入控件A",
                        "function": "input",
                        "args": {
                            "username": "admin"
                        }
                    },
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 2,
                        "type": "ui_control",
                        "title": "输入控件B",
                        "function": "input",
                        "args": {
                            "password": "123456"
                        }
                    },
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 3,
                        "type": "ui_control",
                        "title": "点击控件C",
                        "function": "click",
                        "args": {}
                    },
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 4,
                        "type": "logic",
                        "title": "循环二(逻辑块)",
                        "function": "for",
                        "num": 3,
                        "data_source": [],
                        "business_list": [
                            {
                                "uuid": shortuuid.uuid(),
                                "index": 11,
                                "type": "ui_control",
                                "title": "点击控件X-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": shortuuid.uuid(),
                                "index": 22,
                                "type": "ui_control",
                                "title": "点击控件Y-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": shortuuid.uuid(),
                                "index": 33,
                                "type": "ui_control",
                                "title": "点击控件Z-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": shortuuid.uuid(),
                                "index": 44,
                                "type": "logic",
                                "title": "循环三(逻辑块)",
                                "function": "for",
                                "num": 2,
                                "data_source": [],
                                "business_list": [
                                    {
                                        "uuid": shortuuid.uuid(),
                                        "index": 3331,
                                        "type": "ui_control",
                                        "title": "===点击控件OKC===2",
                                        "function": "click",
                                        "args": {}
                                    },
                                    {
                                        "uuid": shortuuid.uuid(),
                                        "index": 3332,
                                        "type": "ui_control",
                                        "title": "===点击控件LOL===2",
                                        "function": "click",
                                        "args": {}
                                    },
                                ]
                            }
                        ]
                    },
                    child_master
                ]
            },
            {
                "uuid": shortuuid.uuid(),
                "index": 2,
                "title": "操作2",
                "type": "master",
                "business_list": [
                    {
                        "uuid": shortuuid.uuid(),
                        "index": 1,
                        "type": "ui_control",
                        "title": "点击控件",
                        "function": "click",
                        "args": {}
                    },
                ]
            }
        ]
    }
]


class WebUiDriver:
    """1"""


class CustomLogic:
    """自定义逻辑"""

    @classmethod
    def _if(cls, _b: any) -> bool:
        """if"""

        if _b:
            return True
        else:
            return False

    @classmethod
    def _for(cls, business_list: list, *args):
        """for"""

        for b in business_list:
            print(b, args)

    @classmethod
    def _try(cls, _t, _e):
        """try"""

        try:
            _t
        except BaseException as e:
            _e


class ControlFunction:
    """控件方法字典类"""

    web_ui_control_dict = {
        "open": "open",
        "input": "input",
        "click": "click"
    }

    api_control_dict = {
        "api": "",
        "api3": ""
    }

    assert_control_dict = {
        "assert_ui": "",
        "assert_api": "",
        "assert_db": ""
    }

    logic_control_dict = {
        "if": CustomLogic._if,
        "for": CustomLogic._for,
        "try": CustomLogic._try
    }

    message_control_dict = {
        "ding_ding": "",
        "wechat": ""
    }

    middle_control_dict = {
        "redis": "",
        "mq": "",
        "kafka": ""
    }


control_dict = {
    "ui_control": ControlFunction.web_ui_control_dict,
    "api_control": ControlFunction.api_control_dict,
    "assert_control": ControlFunction.assert_control_dict,
    "logic_control": ControlFunction.logic_control_dict,
    "message_control": ControlFunction.message_control_dict,
    "middle_control": ControlFunction.middle_control_dict
}


def query_function(business_dict: dict) -> any:
    """
    获取控件映射的方法
    :param business_dict: 控件json对象
    :return:
    """

    business_type = business_dict.get('type')
    business_function = business_dict.get('function')
    function_name = control_dict.get(business_type).get(business_function)  # .get('ui_control').get('open')

    if not function_name:
        print(f"{business_type} 或 {business_function} 不存在")
        return None
    return function_name


def get_primary_func(o: object, func_name: str):
    """基本func"""

    f = getattr(o, func_name)
    return f


def for_func(action_list: list, data_list: list = None, num: int = 0, deep_num: int = 0, first: bool = True,
             master_function=None, web_driver_example: object = None) -> None:
    """
    for递归
    :param action_list: 任务列表
    :param data_list: 数据列表
    :param num: 轮次(data_list为空时使用,否则按照数据列表长度作为循序次数)
    :param deep_num: 子循环的轮次
    :param first: 是否首次循环
    :param master_function:
    :param web_driver_example:
    :return:
    """

    for i in range(1, num + 1):
        if first:
            print(f'=== 第 {i} 轮开始 ===')

        for index, ac in enumerate(action_list, 1):
            ac_function = ac.get('function')
            if ac_function == 'for':
                ac_num = ac.get('num')
                ac_action = ac.get('business_list')
                for_func(
                    action_list=ac_action,
                    num=ac_num,
                    deep_num=i,
                    first=False,
                    master_function=master_function,
                    web_driver_example=web_driver_example
                )
            else:
                ac_type = ac.get('type')
                if ac_type == 'master':
                    master_function([ac], web_driver_example)
                else:
                    """
                    selenium等驱动逻辑操作...
                    """
                    res_func = query_function(business_dict=ac)
                    if not res_func:
                        raise KeyError(f"异常:{ac}")

                    if first:
                        print(f">>>{i}", ac, first)
                    else:
                        print(f">>>{deep_num}", ac, first)

                    f = get_primary_func(web_driver_example, res_func)
                    print(f)
        if first:
            print(f'=== 第 {i} 轮结束 ===\n')


def recursion_main(data_list: list, web_driver_example: object = None):
    """主递归"""

    for data in data_list:
        business_title = data.get('title')
        data_type = data.get('type')
        business_list = data.get('business_list')

        if data_type == "master" and business_list:
            recursion_main(data_list=business_list, web_driver_example=web_driver_example)
        else:
            res_func = query_function(business_dict=data)
            if not res_func:
                return False

            function = data.get('function')
            child_business_list = data.get('business_list')

            if function == 'for':
                """
                for function 特殊处理
                """
                for_num = data.get('num')
                for_func_kw = {
                    "action_list": child_business_list,
                    "num": for_num,
                    "deep_num": 1,
                    "master_function": recursion_main,
                    "web_driver_example": web_driver_example
                }
                for_func(**for_func_kw)
            else:
                """
                普通 function 执行
                """
                print(">>>", data)
                f = get_primary_func(web_driver_example, res_func)
                print("普通 function 反射执行>>>", function, child_business_list, res_func, f, '\n')


class UiCaseRunner(WebUiDriver):
    """rpa"""

    def __init__(self, data_list: list, web_driver):
        """

        :param data_list:
        """

        self.data_list = data_list
        self.bwd = web_driver(headless=False)

    def main(self):
        """main"""

        recursion_main(data_list=self.data_list, web_driver_example=self.bwd)


if __name__ == '__main__':
    # print(json.dumps(meta_data, ensure_ascii=False))
    # print(control_dict)

    ucr = UiCaseRunner(data_list=meta_data, web_driver=BaseWebDriver)
    ucr.main()
