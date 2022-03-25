# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 6:03 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : send_mail.py
# @Software: PyCharm

import platform
import smtplib
from ast import literal_eval
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from common.libs.db import project_db


class SendEmail:
    """
    发送邮件
    """

    def __init__(self, to_list=None, ac_list=None):

        send_mail = project_db.select('SELECT * FROM exile_mail_conf WHERE is_send=1;', only=True)

        self.mail_from = send_mail.get('mail')  # 发件邮箱账号
        self.mail_pwd = send_mail.get('send_pwd')  # 发件邮箱的授权码

        if to_list:
            self.to_list = to_list
        if ac_list:
            self.ac_list = ac_list

        # self.to_list = ['yang6333yyx@126.com']
        # self.ac_list = ['417993207@qq.com']

        self.subject = '自动化测试报告'  # 邮件标题

    @classmethod
    def open_test_report(cls, file_path):
        """打开最新测试报告"""
        f = open(file_path, 'rb')  # 打开最新报告
        print('打开报告', f)
        mail_content = f.read()  # 读取->作为邮件内容
        f.close()
        return mail_content

    def send_attach(self, report_title=None, html_file_path=None, mail_content=None, xm_file_path=None):
        """
        附件发送
        :param report_title:
        :param html_file_path:
        :param mail_content:
        :param xm_file_path:
        :return:
        """

        to_list = self.to_list
        ac_list = self.ac_list

        to = ",".join(to_list)  # 收件人
        acc = ",".join(ac_list)  # 抄送人

        # mail_content = cls.open_test_report(file_path)

        message = MIMEMultipart()
        # message['From'] = Header("基础服务" + "<" + '杨跃雄' + ">", 'utf-8')
        # message['To'] = Header("yyx", 'utf-8')
        message['From'] = Header(f'{report_title}-自动化测试<自动发送>', 'utf-8')
        message['To'] = to
        message['Cc'] = acc
        message['Subject'] = Header(self.subject, 'utf-8')
        # message.attach(MIMEText(mail_content, 'html', 'utf-8'))
        message.attach(MIMEText(mail_content, 'plain', 'utf-8'))
        # message.attach(MIMEText('基础服务:自动化测试报告-邮件内容', 'plain', 'utf-8'))  # 邮件内容

        if html_file_path:
            # 附件:HTML
            att_html = MIMEText(open(html_file_path, 'rb').read(), 'base64', 'utf-8')
            att_html["Content-Type"] = 'application/octet-stream'
            # att_html["Content-Disposition"] = 'attachment; filename=' + html_file_path.split(
            #     'reports\\' if platform.system() == "Windows" else 'reports/')[1]

            att_html["Content-Disposition"] = 'attachment; filename=' + html_file_path.split(
                'report\\' if platform.system() == "Windows" else 'report/')[1]

            message.attach(att_html)
        if xm_file_path:
            pass
            # TODO XMind上传
            # 附件:XMind
            # att_xm = MIMEText(open(xm_file_path, 'rb').read(), 'base64', 'utf-8')
            # att_xm["Content-Type"] = 'application/octet-stream'
            # att_xm["Content-Disposition"] = 'attachment; filename=' + xm_file_path.split('xminds/')[1]
            # message.attach(att_xm)

        try:
            if "qq" or "QQ" in self.mail_from:
                smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
            else:
                smtpObj = smtplib.SMTP_SSL("smtp.qiye.aliyun.com", 465)

            # smtpObj = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            smtpObj.login(self.mail_from, self.mail_pwd)
            smtpObj.sendmail(self.mail_from, message['To'].split(',') + message['Cc'].split(','), message.as_string())
            print('发送成功')
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print("发送失败:{}".format(str(e)))

    def send_normal(self, subject, content):
        """
        正常发送
        :param subject:
        :param content:
        :return:
        """
        to = ",".join(literal_eval(self.to_list))
        message = MIMEText(content)
        message["Subject"] = subject
        message["From"] = self.mail_from
        message["To"] = to
        message['Cc'] = ",".join(literal_eval(self.ac_list))
        try:
            smtpObj = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            smtpObj.login(self.mail_from, self.mail_pwd)
            smtpObj.sendmail(self.mail_from, to, message.as_string())
            print("发送成功!")
            smtpObj.quit()
        except BaseException as e:
            print("发送失败:{}".format(str(e)))
