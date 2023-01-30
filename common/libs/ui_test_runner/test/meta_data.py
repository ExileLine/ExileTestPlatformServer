# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 12:00
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : meta_data.py
# @Software: PyCharm

meta_data = [
    {
        "uuid": "SSKXwjUKoQNqG5sV5qNRP8",
        "index": 1,
        "title": "开始",
        "type": "master",
        "business_list": [
            {
                "uuid": "dq9nUTPm6nypqbDt2xwzA9",
                "index": 1,
                "type": "ui_control",
                "title": "启动浏览器控件",
                "function": "open",
                "args": {
                    "url": "https://www.github.com"
                }
            }
        ]
    },
    {
        "uuid": "KT59rxZaB7c4tMfRJCQzRb",
        "index": 2,
        "title": "登录",
        "type": "master",
        "business_list": [
            {
                "uuid": "PancmWgaEfCPcwuSFFr3nC",
                "index": 1,
                "type": "ui_control",
                "title": "输入控件",
                "function": "input",
                "args": {
                    "username": "admin"
                }
            },
            {
                "uuid": "YYtJPzKKAfZ6K2L9CAZrz8",
                "index": 2,
                "type": "ui_control",
                "title": "输入控件",
                "function": "input",
                "args": {
                    "password": "123456"
                }
            },
            {
                "uuid": "fnvL2vEpqk95ARzC8n5Bmi",
                "index": 3,
                "type": "ui_control",
                "title": "点击控件",
                "function": "click",
                "args": {}
            },
            {
                "uuid": "UAgXfArTT37o8tvGfvCPAf",
                "index": 4,
                "title": "检验是否登录成功",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "oAfe5DJdyjo8H2QcmgrybP",
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
                            }
                        }
                    }
                ]
            }
        ]
    },
    {
        "uuid": "8s2vTYVAmnAx75hd7Zb6oW",
        "index": 3,
        "title": "循环录入数据",
        "type": "master",
        "business_list": [
            {
                "uuid": "2HHDpYRcYAbjMjvb2JcgnW",
                "index": 1,
                "type": "logic_control",
                "title": "循环控件",
                "function": "for",
                "num": 2,
                "data_source": [],
                "business_list": [
                    {
                        "uuid": "Q2HSWNo6F37LBQnGce3YZF",
                        "index": 1,
                        "type": "ui_control",
                        "title": "输入控件A",
                        "function": "input",
                        "args": {
                            "username": "admin"
                        }
                    },
                    {
                        "uuid": "Tgpqau5oLojKckjYCSSq34",
                        "index": 2,
                        "type": "ui_control",
                        "title": "输入控件B",
                        "function": "input",
                        "args": {
                            "password": "123456"
                        }
                    },
                    {
                        "uuid": "Ao5wFr6aJ6XD9aWpRbwJX6",
                        "index": 3,
                        "type": "ui_control",
                        "title": "点击控件C",
                        "function": "click",
                        "args": {}
                    },
                    {
                        "uuid": "nmt6gHBAMZNoozMox6AjUb",
                        "index": 4,
                        "type": "logic",
                        "title": "循环二(逻辑块)",
                        "function": "for",
                        "num": 3,
                        "data_source": [],
                        "business_list": [
                            {
                                "uuid": "fVWxPXe3wvnAzQb6W8qQX9",
                                "index": 11,
                                "type": "ui_control",
                                "title": "点击控件X-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": "4X4THtoLhBqAh7MSCNJh37",
                                "index": 22,
                                "type": "ui_control",
                                "title": "点击控件Y-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": "b8GKiADD35x5B6ENx4EDqU",
                                "index": 33,
                                "type": "ui_control",
                                "title": "点击控件Z-3",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": "3Exf8tts4NrdLYxZSSyN5W",
                                "index": 44,
                                "type": "logic",
                                "title": "循环三(逻辑块)",
                                "function": "for",
                                "num": 2,
                                "data_source": [],
                                "business_list": [
                                    {
                                        "uuid": "YY3TM9xBPSsonno8iBo6F9",
                                        "index": 3331,
                                        "type": "ui_control",
                                        "title": "===点击控件OKC===2",
                                        "function": "click",
                                        "args": {}
                                    },
                                    {
                                        "uuid": "2YReAR6kUBRLVBnkjxqq6Q",
                                        "index": 3332,
                                        "type": "ui_control",
                                        "title": "===点击控件LOL===2",
                                        "function": "click",
                                        "args": {}
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "uuid": "XnvkzYRmBzDkoUAiZbYqqv",
                        "index": 5,
                        "title": "循环四(业务块)",
                        "type": "master",
                        "business_list": [
                            {
                                "uuid": "Fh6owJBcj8cHrxJALjy5Zs",
                                "index": 1,
                                "type": "ui_control",
                                "title": "循环四-点击控件1",
                                "function": "click",
                                "args": {}
                            },
                            {
                                "uuid": "P4uJAvG2BW7ELBMF6kSqXt",
                                "index": 2,
                                "type": "logic_control",
                                "title": "循环控件",
                                "function": "for",
                                "num": 2,
                                "data_source": [],
                                "business_list": [
                                    {
                                        "uuid": "5RGFfqizkAajQUnWw3CFZz",
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
                ]
            },
            {
                "uuid": "DTVNfXZTsKNZFRSSh2eTkx",
                "index": 2,
                "title": "操作2",
                "type": "master",
                "business_list": [
                    {
                        "uuid": "cSbPDUizQPZyaWwgYwrkoz",
                        "index": 1,
                        "type": "ui_control",
                        "title": "点击控件",
                        "function": "click",
                        "args": {}
                    }
                ]
            }
        ]
    }
]
