# -*- coding: utf-8 -*-
# @Time    : 2023/1/4 14:36
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : meta_data.py
# @Software: PyCharm


import json

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
                    "url": "https://www.github.com"
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
                "args": {
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
                    ]
                }
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
    print(json.dumps(meta_data, ensure_ascii=False))
