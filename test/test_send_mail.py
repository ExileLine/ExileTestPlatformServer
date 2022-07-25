# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 17:29
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : test_send_mail.py
# @Software: PyCharm

from common.tools.send_mail import SendEmail

if __name__ == '__main__':
    SendEmail(
        to_list=['yangyuexiong@haoyuntech.com'],
        ac_list=['yangyuexiong@haoyuntech.com']
    ).send_attach(
        report_title="测试",
        html_file_path="/Users/yangyuexiong/Desktop/test_reports/api/Test_Report_2022-06-22_00_10_37_执行用例[登录成功9999999.html",
        mail_content="详情查看附件"
    )
