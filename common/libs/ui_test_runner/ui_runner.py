# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 11:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_runner.py
# @Software: PyCharm


class CustomAssert:
    """自定义断言"""

    @classmethod
    def assert_ui(cls):
        """ui断言"""

    @classmethod
    def assert_api(cls):
        """api断言"""

    @classmethod
    def assert_db(cls):
        """db断言"""


class CustomLogic:
    """自定义逻辑"""

    @classmethod
    def custom_if(cls, _b: any) -> bool:
        """if"""

        if not _b:
            return False
        return True

    @classmethod
    def custom_try(cls, _t, _e):
        """try"""

        try:
            _t
        except BaseException as e:
            _e


class CustomMessage:
    """自定义消息"""

    @classmethod
    def ding_ding(cls):
        """ding_ding"""

    @classmethod
    def wechat(cls):
        """wechat"""


class CustomMiddle:
    """自定义中间件"""

    @classmethod
    def redis(cls):
        """redis"""

    @classmethod
    def mq(cls):
        """mq"""

    @classmethod
    def kafka(cls):
        """kafka"""


class ControlFunction:
    """控件方法字典类"""

    web_ui_control_dict = {
        "open": "open",
        "close": "close",
        "input": "custom_input",
        "click": "custom_click"
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
        "for": "for",
        "if": CustomLogic.custom_if,
        "try": CustomLogic.custom_try
    }

    message_control_dict = {
        "ding_ding": CustomMessage.ding_ding,
        "wechat": CustomMessage.wechat
    }

    middle_control_dict = {
        "redis": CustomMiddle.redis,
        "mq": CustomMiddle.mq,
        "kafka": CustomMiddle.kafka
    }

    control_dict = {
        "ui_control": web_ui_control_dict,
        "api_control": api_control_dict,
        "assert_control": assert_control_dict,
        "logic_control": logic_control_dict,
        "message_control": message_control_dict,
        "middle_control": middle_control_dict
    }


def query_function(business_dict: dict) -> any:
    """
    获取控件映射的方法
    :param business_dict: 控件json对象
    :return:
    """

    business_type = business_dict.get('type')
    business_function = business_dict.get('function')
    function_name = ControlFunction.control_dict.get(business_type).get(
        business_function)  # 例子: .get('ui_control').get('open')

    if not function_name:
        print(f"{business_type} 或 {business_function} 不存在")
        return None
    return function_name


def getattr_func(o: object, func_name: str) -> any:
    """
    获取实例方法
    :param o: 实例
    :param func_name: 方法名称
    :return:
    """

    f = getattr(o, func_name)
    return f


def for_recursion(action_list: list, data_list: list = None, num: int = 0, deep_num: int = 0, first: bool = True,
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
                for_recursion(
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

                    print(">>>", ac)
                    func = getattr_func(web_driver_example, res_func)
                    func_args = ac.get('args')
                    print(">>> 普通 function 反射执行", func, func_args, '\n')
                    func(**func_args)
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
                for_recursion(**for_func_kw)
            else:
                """
                普通 function 执行
                """
                print(">>>", data)
                func = getattr_func(web_driver_example, res_func)
                func_args = data.get('args')
                print(">>> 普通 function 反射执行", func, func_args, '\n')
                func(**func_args)


class UiCaseRunner:
    """UI用例执行"""

    def __init__(self, data_list: list, web_driver: type, web_driver_kw: dict = None):
        """

        :param data_list: 任务列表
        :param web_driver: WebDriver驱动
        :param web_driver_kw: WebDriver构造函数
        """

        self.data_list = data_list
        self.web_driver_kw = web_driver_kw if web_driver_kw else {}
        self.web_driver_example = web_driver(headless=False, **self.web_driver_kw)

    def main(self):
        """main"""

        recursion_main(data_list=self.data_list, web_driver_example=self.web_driver_example)


if __name__ == '__main__':
    from common.libs.BaseWebDriver import BaseWebDriver
    from common.libs.ui_test_runner.test.meta_data import meta_data

    ucr = UiCaseRunner(data_list=meta_data, web_driver=BaseWebDriver)
    ucr.main()
