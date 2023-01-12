# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 14:26
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_meta_data.py
# @Software: PyCharm


child_master = {
    "index": 5,
    "title": "循环四(业务块)",
    "type": "master",
    "business_list": [
        {
            "index": 1,
            "type": "ui_control",
            "desc": "循环四-点击控件1",
            "function": "click",
            "args": {}
        },
        {
            "index": 2,
            "type": "logic_control",
            "function": "for",
            "num": 2,
            "data_source": [],
            "action": [
                {
                    "index": 771,
                    "type": "ui_control",
                    "desc": "循环四-内循环-点击控件2",
                    "function": "click",
                    "args": {}
                }
            ]
        }
    ]
}

meta_data = [
    {
        "index": 1,
        "title": "开始",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "ui_control",
                "desc": "启动浏览器控件",
                "function": "open",
                "args": {
                    "url": "http://localhost:3200/login"
                }
            },
        ]
    },
    {
        "index": 2,
        "title": "登录",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "ui_control",
                "desc": "输入控件",
                "function": "input",
                "args": {
                    "username": "admin"
                }
            },
            {
                "index": 2,
                "type": "ui_control",
                "desc": "输入控件",
                "function": "input",
                "args": {
                    "password": "123456"
                }
            },
            {
                "index": 3,
                "type": "ui_control",
                "desc": "点击控件",
                "function": "click",
                "args": {}
            },
            {
                "index": 4,
                "title": "检验是否登录成功",
                "type": "master",
                "business_list": [
                    {
                        "index": 1,
                        "type": "assert_control",
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
        "index": 3,
        "title": "循环录入数据",
        "type": "master",
        "business_list": [
            {
                "index": 1,
                "type": "logic_control",
                "function": "for",
                "num": 2,  # 调试
                "data_source": [],
                "action": [
                    {
                        "index": 1,
                        "type": "ui_control",
                        "desc": "输入控件A",
                        "function": "input",
                        "args": {
                            "username": "admin"
                        }
                    },
                    {
                        "index": 2,
                        "type": "ui_control",
                        "desc": "输入控件B",
                        "function": "input",
                        "args": {
                            "password": "123456"
                        }
                    },
                    {
                        "index": 3,
                        "type": "ui_control",
                        "desc": "点击控件C",
                        "function": "click",
                        "args": {}
                    },
                    {
                        "index": 4,
                        "type": "logic",
                        "desc": "循环二(逻辑块)",
                        "function": "for",
                        "num": 3,
                        "data_source": [],
                        "action": [
                            {
                                "index": 11,
                                "type": "ui_control",
                                "desc": "点击控件X-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 22,
                                "type": "ui_control",
                                "desc": "点击控件Y-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 33,
                                "type": "ui_control",
                                "desc": "点击控件Z-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "index": 44,
                                "type": "logic",
                                "desc": "循环三(逻辑块)",
                                "function": "for",
                                "num": 2,
                                "data_source": [],
                                "action": [
                                    {
                                        "index": 3331,
                                        "type": "ui_control",
                                        "desc": "===点击控件OKC===2",
                                        "function": "click",
                                        "args": {}
                                    },
                                    {
                                        "index": 3332,
                                        "type": "ui_control",
                                        "desc": "===点击控件LOL===2",
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
                "index": 2,
                "title": "操作2",
                "type": "master",
                "business_list": [
                    {
                        "index": 1,
                        "type": "ui_control",
                        "desc": "点击控件",
                        "function": "click",
                        "args": {}
                    },
                ]
            }
        ]
    }
]
if __name__ == '__main__':
    from common.libs.BaseWebDriver import BaseWebDriver

    bwd = BaseWebDriver()
    bwd.open(url='http://localhost:3200/login')
