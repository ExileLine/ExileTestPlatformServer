# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 6:05 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : message_push.py
# @Software: PyCharm

import requests

from common.libs.db import project_db


class MessagePush:
    """消息推送"""

    @staticmethod
    def dd_push(ding_talk_url=None, report_url=None, is_safe_scan=None, safe_scan_report_path=None, markdown_text=None):
        """
        钉钉推送
        :param ding_talk_url: 钉钉群token
        :param report_url: 测试报告链接
        :param is_safe_scan: 是否安全测试报告
        :param safe_scan_report_path: 安全测试报告链接
        :param markdown_text: 推送模板
        :return:
        """

        url = ding_talk_url

        if not url.strip():
            raise TypeError('钉钉推送失败: DING_TALK_URL 未配置')

        headers = {"Content-Type": "application/json;charset=utf-8"}

        # msg = """{}\n报告地址: {}""".format(report_result, report_url)

        """
        text:
        
        json_data = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "atMobiles": AT_MOBILES,
                "atUserIds": AT_USER_IDS,
                "isAtAll": IS_AT_ALL
            }
        }
        """

        demo_text = "#### 测试报告:{}  \n  > 测试人员:{}  \n  > 开始时间:{}  \n  > 结束时间:{}  \n  > 合计耗时:{}  \n  > 用例总数:{}  \n  > 成功数:{}  \n  > 失败数:{}  \n  > 错误数:{}  \n  > 通过率:{}  \n  > 报告地址:[前往](1)"

        report_link = f"  \n  > 报告地址:[{report_url}]({report_url})"
        safe_scan_report_link = f"  \n  > 安全报告:[{safe_scan_report_path}]({safe_scan_report_path})"

        # text = markdown_text + report_link + safe_scan_report_link
        text = f"{markdown_text}{report_link}{safe_scan_report_link if is_safe_scan else ''}"
        json_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试报告",
                "text": text
                # "text": demo_text + report_link
            },
            "at": {
                "atMobiles": [],
                "atUserIds": [],
                "isAtAll": True
            }
        }

        response = requests.post(url, json=json_data, headers=headers, verify=False)
        print(response.json())

    @staticmethod
    def ding_ding_push(ding_talk_url=None, report_url=None, markdown_text=None):
        """
        钉钉推送
        :param ding_talk_url:
        :param report_url:
        :param markdown_text:
        :return:
        """

        url = ding_talk_url

        headers = {
            "Content-Type": "application/json;charset=utf-8"
        }

        report_link = f"  \n  > 报告地址:[{report_url}]({report_url})"
        text = f"{markdown_text}{report_link}"
        json_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试报告",
                "text": text
                # "text": demo_text + report_link
            },
            "at": {
                "atMobiles": [],
                "atUserIds": [],
                "isAtAll": True
            }
        }

        response = requests.post(url, headers=headers, json=json_data, verify=False)
        print(response.json())
