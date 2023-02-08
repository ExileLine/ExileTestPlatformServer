# -*- coding: utf-8 -*-
# @Time    : 2023/2/8 15:04
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_ctrl.py
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
