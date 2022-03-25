# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 6:05 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : message_push.py
# @Software: PyCharm

import requests

from common.libs.db import project_db


class MessagePush:
    """消息推送"""

    @staticmethod
    def dd_push(ding_talk_url=None, report_name=None, markdown_text=None):
        """钉钉推送"""

        server_url = project_db.select(
            'SELECT server_url FROM exile_platform_conf WHERE weights = (SELECT max(weights) FROM exile_platform_conf);',
            only=True)

        url = ding_talk_url

        print(server_url)
        report_url = f"{server_url.get('server_url', 'http://0.0.0.0:7272')}/static/report/{report_name}"

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

        report_link = "  \n  > 报告地址:[{}]({})".format(report_url, report_url)

        json_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "测试报告",
                "text": markdown_text + report_link
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
