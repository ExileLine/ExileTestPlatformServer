# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 8:19 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CaseDrivenResult.py
# @Software: PyCharm

import os
import sys
import re
import json
import time
import datetime
import platform
import smtplib
from ast import literal_eval
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
import shortuuid
from loguru import logger

from common.libs.db import project_db, R
from common.libs.public_func import check_keys
from common.libs.assert_related import AssertResponseMain, AssertFieldMain
from common.libs.StringIOLog import StringIOLog
from common.libs.execute_code import execute_code
from common.libs.data_dict import var_func_dict, execute_label_tuple, gen_redis_first_logs


class TemplateMixin:
    """HTML模版"""

    def __init__(self, data):
        self.data = data

    @classmethod
    def before_html(cls):
        """1"""
        _before = r"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <!-- import CSS -->
    <link rel="stylesheet" href="https://unpkg.com/element-plus@2.0.5/dist/index.css" />
    <!-- import Vue before Element -->
    <script src="https://unpkg.com/vue@3.2.31/dist/vue.global.js"></script>
    <!-- import JavaScript -->
    <script src="https://unpkg.com/element-plus@2.0.5/dist/index.full.js"></script>

    <style>
      table table thead {
        display: none;
      }

      .el-table__expanded-cell[class*='cell'] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-right: 0 !important;
      }

      .card {
        margin: 30px;
        white-space: pre;
      }

      .pl-20 {
        padding-left: 20px;
      }

      .circle.success {
        color: lightgreen;
      }

      .circle.error {
        color: lightcoral;
      }

      .justify-between {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    </style>
  </head>
    <body>
    <div id="app">
      <el-backtop :bottom="10" :visibility-height="10"></el-backtop>
      <div>
        <h1>自动化测试报告</h1>
        <h3>测试人员 : {{resp.execute_username}}</h3>
        <p>开始时间 : {{resp.create_time}}</p>
        <p>合计耗时 : {{resp.total_time}}</p>
        <p>
          请求统计 : 总数: {{resp.result_summary.req_count}}，成功数 :
          {{resp.result_summary.req_success}}，失败数 : {{resp.result_summary.req_error}}，成功率 :
          {{resp.result_summary.req_success_rate}}，失败率 : {{resp.result_summary.req_error_rate}}
        </p>
        <p>
          响应断言统计 : 总数: {{resp.result_summary.resp_ass_count}}，成功数 :
          {{resp.result_summary.resp_ass_success}}，失败数 :
          {{resp.result_summary.resp_ass_fail}}，成功率 :
          {{resp.result_summary.resp_ass_success_rate}}，失败率 :
          {{resp.result_summary.resp_ass_fail_rate}}
        </p>
        <p>
          字段断言统计 : 总数: {{resp.result_summary.field_ass_count}}，成功数 :
          {{resp.result_summary.field_ass_success}}，失败数 :
          {{resp.result_summary.field_ass_fail}}，成功率 :
          {{resp.result_summary.field_ass_success_rate}}，失败率 :
          {{resp.result_summary.field_ass_fail_rate}}
        </p>
        <p>
          测试结果 : 共 {{resp.result_summary.req_count + resp.result_summary.resp_ass_count +
          resp.result_summary.field_ass_count}}，通过
          {{resp.result_summary.req_success+resp.result_summary.resp_ass_success+resp.result_summary.field_ass_success}}
        </p>
        <p>{{description}}</p>
      </div>

      <el-tabs>
        <el-tab-pane
          :label="`所有(${resp.result_summary.req_count + resp.result_summary.resp_ass_count +
          resp.result_summary.field_ass_count})`"
        >
          <el-tabs type="border-card">
            <el-tab-pane label="用例">
              <el-table border :data="case_all_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <el-card shadow="always" class="card">
                      <p v-for="i in row.case_log">{{i}}</p>
                    </el-card>
                  </template>
                </el-table-column>
                <el-table-column prop="case_name" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.case_id}}-{{row.case_name}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="场景">
              <el-table border :data="group_all_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <div class="pl-20">
                      <el-table border :data="row.scenario_log" show-header="false">
                        <el-table-column type="expand">
                          <template #default="{row}">
                            <el-card shadow="always" class="card">
                              <p v-for="i in row.case_log">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                        <el-table-column prop="case_name">
                          <template #default="{row}">
                            <div class="justify-between">
                              <span>{{row.case_id}}-{{row.case_name}}</span>
                              <span v-if="row.error" class="circle error">X</span>
                              <span v-else class="circle success">✔️</span>
                            </div>
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="scenario_title" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.scenario_id}}-{{row.scenario_title}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
        <el-tab-pane
          :label="`成功(${resp.result_summary.req_success+resp.result_summary.resp_ass_success+resp.result_summary.field_ass_success})`"
        >
          <el-tabs type="border-card">
            <el-tab-pane label="用例">
              <el-table border :data="success_left_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <el-card shadow="always" class="card">
                      <p v-for="i in row.case_log">{{i}}</p>
                    </el-card>
                  </template>
                </el-table-column>
                <el-table-column prop="case_name" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.case_id}}-{{row.case_name}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="场景">
              <el-table border :data="success_right_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <div class="pl-20">
                      <el-table border :data="row.scenario_log" show-header="false">
                        <el-table-column type="expand">
                          <template #default="{row}">
                            <el-card shadow="always" class="card">
                              <p v-for="i in row.case_log">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                        <el-table-column prop="case_name">
                          <template #default="{row}">
                            <div class="justify-between">
                              <span>{{row.case_id}}-{{row.case_name}}</span>
                              <span v-if="row.error" class="circle error">X</span>
                              <span v-else class="circle success">✔️</span>
                            </div>
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="scenario_title" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.scenario_id}}-{{row.scenario_title}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
        <el-tab-pane
          :label="`失败(${resp.result_summary.req_error+resp.result_summary.resp_ass_fail+resp.result_summary.field_ass_fail})`"
        >
          <el-tabs type="border-card">
            <el-tab-pane label="用例">
              <el-table border :data="error_left_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <el-card shadow="always" class="card">
                      <p v-for="i in row.case_log">{{i}}</p>
                    </el-card>
                  </template>
                </el-table-column>
                <el-table-column prop="case_name" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.case_id}}-{{row.case_name}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="场景">
              <el-table border :data="error_right_list" show-header="false">
                <el-table-column type="expand">
                  <template #default="{row}">
                    <div class="pl-20">
                      <el-table border :data="row.scenario_log" show-header="false">
                        <el-table-column type="expand">
                          <template #default="{row}">
                            <el-card shadow="always" class="card">
                              <p v-for="i in row.case_log">{{i}}</p>
                            </el-card>
                          </template>
                        </el-table-column>
                        <el-table-column prop="case_name">
                          <template #default="{row}">
                            <div class="justify-between">
                              <span>{{row.case_id}}-{{row.case_name}}</span>
                              <span v-if="row.error" class="circle error">X</span>
                              <span v-else class="circle success">✔️</span>
                            </div>
                          </template>
                        </el-table-column>
                      </el-table>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="scenario_title" :label="resp.execute_name">
                  <template #default="{row}">
                    <div class="justify-between">
                      <span>{{row.scenario_id}}-{{row.scenario_title}}</span>
                      <span v-if="row.error" class="circle error">X</span>
                      <span v-else class="circle success">✔️</span>
                    </div>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </div>
  </body>
  <script>
  var True = true
  var False = false
"""

        return _before

    @classmethod
    def script_html(cls, data):
        """script"""
        _script = f"""
                var resp = {data};
                """
        return _script

    @classmethod
    def after_html(cls):
        """3"""
        _after = """
var case_result_list = resp.case_result_list
var leftTabList = case_result_list.filter(c => c.report_tab == 1)
var rightTabList = case_result_list.filter(c => c.report_tab == 2)
Vue.createApp({
  data() {
    return {
      resp,
      case_all_list: leftTabList,
      group_all_list: rightTabList,
      success_left_list: leftTabList.filter(left => !left.error),
      error_left_list: leftTabList.filter(left => left.error),
      success_right_list: rightTabList.filter(right => !right.error),
      error_right_list: rightTabList.filter(right => right.error)
    }
  }
})
  .use(ElementPlus)
  .mount('#app')

</script>
</html>
"""
        return _after

    def generate_html_report(self):
        """生成html报告"""
        one = self.before_html()
        two = self.script_html(self.data)
        three = self.after_html()
        html_vue3 = f"{one}{two}{three}"
        return html_vue3


class SendEmail:
    """
    发送邮件
    """

    def __init__(self, to_list=None, ac_list=None):

        # self.mail_from = '872540033@qq.com'  # 发件邮箱账号
        # self.mail_pwd = 'rscfszznxzuubcdb'  # 发件邮箱的授权码

        self.mail_from = 'shipeng@haoyuntech.com'  # 发件邮箱账号
        self.mail_pwd = 'He@789012'  # 发件邮箱的授权码

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
            smtpObj = smtplib.SMTP_SSL("smtp.qiye.aliyun.com", 465)
            # smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
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


class MainTestExpand:
    """扩展"""

    @staticmethod
    def dd_push(ding_talk_url=None, report_name=None, markdown_text=None):
        """钉钉推送"""

        url = "https://oapi.dingtalk.com/robot/send?access_token=fd469de777d85a41f2198b9d8f0d138593239b3ff86a6c7c9d747a1f605848cd"
        # url = ding_talk_url

        if platform.system() == "Linux":
            # report_url = f'http://192.168.14.214:5000/report/{report_name}'
            report_url = f'http://120.24.214.173:5000/report/{report_name}'
        else:
            report_url = f"http://0.0.0.0:7272/report/{report_name}"
            print(report_url)

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

        demo_text = "#### 测试报告:{}  \n  > 测试人员:{}  \n  > 开始时间:{}  \n  > 结束时间:{}  \n  > 持续时间:{}  \n  > 总数:{}  \n  > 成功数:{}  \n  > 失败数:{}  \n  > 错误数:{}  \n  > 通过率:{}  \n  > 报告地址:[前往](1)"

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


class TestResult:
    """测试结果"""

    def __init__(self):
        self.req_count = 0
        self.req_success = 0
        self.req_error = 0
        self.req_success_rate = 0
        self.req_error_rate = 0

        self.resp_ass_count = 0
        self.resp_ass_success = 0
        self.resp_ass_fail = 0
        self.resp_ass_success_rate = 0
        self.resp_ass_fail_rate = 0

        self.field_ass_count = 0
        self.field_ass_success = 0
        self.field_ass_fail = 0
        self.field_ass_error = 0
        self.field_ass_success_rate = 0
        self.field_ass_fail_rate = 0
        self.field_ass_error_rate = 0

        self.all_count = 0

    def get_test_result(self):
        """

        :return:
        """
        self.req_count = self.req_success + self.req_error
        if self.req_count != 0:
            self.req_success_rate = "{}%".format(round(self.req_success / self.req_count, 2) * 100)
            self.req_error_rate = "{}%".format(round(self.req_error / self.req_count, 2) * 100)
            self.resp_ass_count = self.resp_ass_success + self.resp_ass_fail

            self.resp_ass_success_rate = 0 if self.resp_ass_success == 0 else "{}%".format(
                round(self.resp_ass_success / self.resp_ass_count, 2) * 100)

            self.resp_ass_fail_rate = 0 if self.resp_ass_fail == 0 else "{}%".format(
                round(self.resp_ass_fail / self.resp_ass_count, 2) * 100)

            self.field_ass_count = self.field_ass_success + self.field_ass_fail + self.field_ass_error

            self.field_ass_success_rate = 0 if self.field_ass_success == 0 else "{}%".format(
                round(self.field_ass_success / self.field_ass_count, 2) * 100)

            self.field_ass_fail_rate = 0 if self.field_ass_fail == 0 else "{}%".format(
                round(self.field_ass_fail / self.field_ass_count, 2) * 100)

            self.field_ass_error_rate = 0 if self.field_ass_error == 0 else "{}%".format(
                round(self.field_ass_error / self.field_ass_count, 2) * 100)

        d = {
            "req_count": self.req_count,
            "req_success": self.req_success,
            "req_error": self.req_error,
            "req_success_rate": self.req_success_rate,
            "req_error_rate": self.req_error_rate,

            "resp_ass_count": self.resp_ass_count,
            "resp_ass_success": self.resp_ass_success,
            "resp_ass_fail": self.resp_ass_fail,
            "resp_ass_success_rate": self.resp_ass_success_rate,
            "resp_ass_fail_rate": self.resp_ass_fail_rate,

            "field_ass_count": self.field_ass_count,
            "field_ass_success": self.field_ass_success,
            "field_ass_fail": self.field_ass_fail,
            "field_ass_error": self.field_ass_error,
            "field_ass_success_rate": self.field_ass_success_rate,
            "field_ass_fail_rate": self.field_ass_fail_rate,
            "field_ass_error_rate": self.field_ass_error_rate
        }
        return d


class MainTest:
    """
    测试执行

    1.转换参数:
        MainTest.assemble_data_send()√
            MainTest.var_conversion() √

    2.发出请求:
        MainTest.assemble_data_send() √
            MainTest.current_request() √

    3.resp断言前置检查:
        MainTest.resp_check_ass_execute() √
        MainTest.check_resp_ass_keys() √

    4.resp断言执行:
        MainTest.resp_check_ass_execute() √
        MainTest.execute_resp_ass() -> AssertMain.assert_resp_main() √

    5.更新变量:
        MainTest.field_check_ass_execute() √
            MainTest.update_var() √

    6.field断言前置检查:
        MainTest.field_check_ass_execute() √
            MainTest.check_field_ass_keys() √ 【弃用】

    7.field断言执行:
        MainTest.field_check_ass_execute() √
            MainTest.execute_field_ass() -> AssertMain.assert_field_main() √

    8.日志记录:
        MainTest.main()

    9.生成报告:

    """

    # TODO field 前置查询 {"before_query":"select xxx from xxx....","before_field":"username"}
    # TODO sio优化
    # TODO yield 优化 list 消费
    # TODO decimal.Decimal 优化统计数据

    def __init__(self, test_obj):
        self.base_url = test_obj.get('base_url')
        self.use_base_url = test_obj.get('use_base_url')
        self.data_driven = test_obj.get('data_driven')

        self.execute_id = test_obj.get('execute_id')
        self.execute_name = test_obj.get('execute_name')
        self.execute_type = test_obj.get('execute_type')
        self.execute_label = test_obj.get('execute_label')

        self.execute_user_id = test_obj.get('execute_user_id')
        self.execute_username = test_obj.get('execute_username')
        self.sio = test_obj.get('sio', StringIOLog())

        self.is_execute_all = test_obj.get('is_execute_all', False)
        self.execute_dict = test_obj.get('execute_dict', {})
        self.case_list = test_obj.get('case_list', [])

        self.is_dd_push = test_obj.get('is_dd_push', False)
        self.dd_push_id = test_obj.get('dd_push_id')
        self.ding_talk_url = test_obj.get('ding_talk_url')

        self.is_send_mail = test_obj.get('is_send_mail', False)
        self.mail_list = test_obj.get('mail_list')

        if not isinstance(self.case_list, list):
            raise TypeError('MainTest.__init__.case_list 类型错误')

        if self.execute_label not in execute_label_tuple:
            raise TypeError('MainTest.__init__.execute_label 类型错误')

        self.func_name = self.execute_label + "_execute"

        if self.is_execute_all:
            case_list = self.execute_dict.get('case_list', [])
            self.case_generator = (case for case in case_list)
            scenario_list = self.execute_dict.get('scenario_list', [])
            self.scenario_generator = (scenario for scenario in scenario_list)
        else:
            self.case_generator = (case for case in self.case_list)

        self.current_assert_description = None

        self.current_case_resp_ass_error = 0  # 响应断言标识
        self.logs_error_switch = False  # 日志标识
        self.test_result = TestResult()  # 测试结果
        self.case_result_list = []  # 测试结果日志集

        self.create_time = str(datetime.datetime.now())
        self.start_time = time.time()
        self.end_time = 0

        self.save_key = ""
        self.path = ""
        self.report_name = ""

    def json_format(self, d, msg=None):
        """json格式打印"""
        try:
            output = '{}\n'.format(msg) + json.dumps(
                d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False
            )
            self.sio.log(output)
        except BaseException as e:
            self.sio.log('{}\n{}'.format(msg, d))

    def show_log(self, url, headers, req_json, resp_headers, resp_json):
        """测试用例日志打印"""
        self.sio.log(f'=== url ===\n{url}')
        self.json_format(headers, msg='=== headers ===')
        self.json_format(req_json, msg='=== request json ===')
        self.json_format(resp_headers, msg='=== response headers ===')
        self.json_format(resp_json, msg='=== response json ===')

    def var_conversion(self, before_var):
        """变量转换参数"""

        before_var_init = before_var
        if isinstance(before_var_init, (list, dict)):
            before_var = json.dumps(before_var, ensure_ascii=False)

        result_list = re.findall('\\$\\{([^}]*)', before_var)

        if not result_list:
            return before_var_init

        err_var_list = []
        current_dict = {}
        for res in result_list:
            sql = """select var_value, var_type from exile_test_variable where var_name='{}';""".format(res)
            query_result = project_db.select(sql=sql, only=True)
            if query_result:
                var_type = str(query_result.get('var_type'))
                if var_type in var_func_dict.keys():  # 函数
                    current_dict[res] = var_func_dict.get(var_type)
                else:
                    current_dict[res] = json.loads(query_result.get('var_value'))

            elif var_func_dict.get(res):
                current_dict[res] = var_func_dict.get(res)
            else:
                err_var_list.append(res)

        if not current_dict:
            self.sio.log('===未找到变量:{}对应的参数==='.format(err_var_list))
            return before_var_init

        current_str = before_var
        for k, v in current_dict.items():
            old_var = "${%s}" % (k)
            new_var = v
            current_str = current_str.replace(old_var, new_var)
        if isinstance(before_var_init, (list, dict)):
            current_str = json.loads(current_str)
        # print(current_str)
        return current_str

    def check_resp_ass_keys(self, assert_list):
        """
        检查resp断言对象参数类型是否正确
        assert_list: ->list 规则列表
        """

        # cl = [
        #     "assert_key",
        #     "expect_val",
        #     "expect_val_type",
        #     "response_source",
        #     "is_expression",
        #     "python_val_exp",
        #     "rule"
        # ]
        #
        # if not isinstance(assert_list, list) or not assert_list:
        #     self.sio.log("assert_list:类型错误{}".format(assert_list))
        #     return False
        #
        # for ass in assert_list:
        #     if not check_keys(ass, *cl):
        #         self.sio.log("缺少需要的键值对:{}".format(ass), status='error')
        #         return False
        return True

    def execute_resp_ass(self, resp_ass_list, assert_description):
        """
        执行Resp断言
        resp_ass_list demo
            [
                {
                    "assert_key": "code",
                    "expect_val": "200",
                    "expect_val_type": "1",
                    "response_source": "response_body"
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                },
                {
                    "assert_key": "token",
                    "expect_val": "12345678",
                    "expect_val_type": "1",
                    "response_source": "response_headers"
                    "is_expression": 0,
                    "python_val_exp": "okc.get('a').get('b').get('c')[0]",
                    "rule": "__eq__"
                }
            ]
        """
        for resp_ass_dict in resp_ass_list:
            # print(resp_ass_dict)
            new_resp_ass = AssertResponseMain(
                sio=self.sio,
                resp_json=self.resp_json,
                resp_headers=self.resp_headers,
                assert_description=assert_description,
                **resp_ass_dict
            )
            resp_ass_result = new_resp_ass.main()
            # print(resp_ass_result)
            if resp_ass_result.get('status'):  # [bool,str]
                self.test_result.resp_ass_success += 1
            else:
                self.test_result.resp_ass_fail += 1
                self.current_case_resp_ass_error += 1
                self.logs_error_switch = True

    def execute_field_ass(self, ass_json):
        """
        执行Field断言
        """

        field_ass_result = AssertFieldMain(
            sio=self.sio,
            assert_description=self.current_assert_description,
            **ass_json
        ).main()

        self.test_result.field_ass_success += field_ass_result.get('success')
        self.test_result.field_ass_fail += field_ass_result.get('fail')
        self.test_result.field_ass_error += field_ass_result.get('error')
        if self.test_result.field_ass_error != 0:
            self.logs_error_switch = True

    def current_request(self, method=None, **kwargs):
        """
        构造请求
        :param method: 请求方式
        :param kwargs: 请求体以及扩展参数
        :return:
        """

        if hasattr(requests, method):
            response = getattr(requests, method)(**kwargs, verify=False)
            self.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=response.json(),
                resp_headers=response.headers
            )
        else:
            response = {
                "error": "requests 没有 {} 方法".format(method)
            }
            self.show_log(
                kwargs.get('url'),
                kwargs.get('headers'),
                kwargs.get('json', kwargs.get('data', kwargs.get('params'))),
                resp_json=response,
                resp_headers={}
            )
        return response

    def assemble_data_send(self, case_data_info):
        """
        组装数据发送并且更新变量
        :return:
        """

        request_params = case_data_info.get('request_params')
        request_body = case_data_info.get('request_body')
        request_headers = case_data_info.get('request_headers')
        request_body_type = str(case_data_info.get('request_body_type'))
        self.update_var_list = case_data_info.get('update_var_list')

        req_type_dict = {
            "1": {"data": request_body},
            "2": {"json": request_body},
            "3": {"data": request_body}
        }

        method = self.request_method.lower()
        self.sio.log('=== method: {} ==='.format(method))

        url = self.base_url + self.request_url if self.use_base_url else self.request_base_url + self.request_url

        before_send = {
            "url": url,
            "headers": request_headers,
        }
        req_json_data = req_type_dict.get(request_body_type)

        if method == 'get':
            before_send['params'] = request_params
        else:
            before_send.update(req_json_data)

        send = self.var_conversion(before_send)
        self.sio.log('=== send ===')
        resp = self.current_request(method=method, **send)
        self.resp_json = resp.json()
        self.resp_headers = resp.headers

    def resp_check_ass_execute(self, case_resp_ass_info):
        """
        检查 resp 断言规则并执行断言
        :return:
        """
        if not case_resp_ass_info:
            self.sio.log('=== case_resp_ass_info is [] ===')
            return False

        for resp_ass in case_resp_ass_info:  # 遍历断言规则逐一校验
            resp_ass_list = resp_ass.get('ass_json')
            assert_description = resp_ass.get('assert_description')
            # print(resp_ass_list)
            if self.check_resp_ass_keys(assert_list=resp_ass_list):  # 响应检验
                self.execute_resp_ass(resp_ass_list=resp_ass_list, assert_description=assert_description)
            else:
                self.sio.log('=== check_ass_keys error ===', status='error')
                # return False

    def field_check_ass_execute(self, case_field_ass_info):
        """
        检查 field 断言规则并执行断言
        :return:
        """
        if self.current_case_resp_ass_error == 0:  # 所有resp断言规则通过
            self.update_var()  # 更新变量

            for index, field_ass_obj in enumerate(case_field_ass_info, 1):
                self.current_assert_description = field_ass_obj.get('assert_description')
                ass_json_list = field_ass_obj.get('ass_json')

                list(map(self.execute_field_ass, ass_json_list))

        else:
            self.sio.log('=== 断言规则没有100%通过,失败数:{} 不更新变量以及不进行数据库校验 ==='.format(self.current_case_resp_ass_error))

    def update_var(self):
        """更新变量"""

        var_source_dict = {
            "resp_data": self.resp_json,
            "resp_headers": self.resp_headers
        }

        if not self.update_var_list:
            self.sio.log('=== 更新变量列表为空不需要更新变量===')

        for up in self.update_var_list:
            """
            {
                "id": 3,
                "var_value":"123",
                "var_source": "resp_data",
                "expression": "obj.get('code')",
                "is_expression":0,
                "var_get_key": "code"
            }
            """
            id = up.get('id')
            var_value = up.get('var_value')
            var_source = up.get('var_source')
            var_get_key = up.get('var_get_key')
            expression = up.get('expression')
            is_expression = up.get('is_expression', 0)
            data = var_source_dict.get(var_source)

            if bool(is_expression):
                # 表达式取值
                result_json = execute_code(code=expression, data=data)
                update_val_result = result_json.get('result_data')
            else:
                # 直接取值
                update_val_result = data.get(var_get_key)

            old_var = json.dumps(var_value, ensure_ascii=False)
            new_var = json.dumps(update_val_result, ensure_ascii=False)

            sql = """UPDATE exile_test_variable SET var_value='{}' WHERE id='{}';""".format(new_var, id)
            self.sio.log('=== update sql === 【 {} 】'.format(sql), status='success')
            project_db.update_data(sql)

            sql2 = """INSERT INTO exile_test_variable_history ( `create_timestamp`, `is_deleted`, `var_id`, `update_type`, `creator`, `creator_id`, `before_var`, `after_var`) VALUES ('{}',  '0',  '{}', '执行用例更新', '{}', '{}', '{}', '{}');""".format(
                int(self.start_time), id, self.execute_username, self.execute_user_id, old_var, new_var
            )
            self.sio.log('=== update history sql === 【 {} 】'.format(sql2), status='success')
            project_db.create_data(sql2)

    def save_logs(self, log_id):
        """

        :param log_id: 日志id
        :return:
        """

        sql = """INSERT INTO exile_test_execute_logs (`is_deleted`, `create_time`, `create_timestamp`,  `execute_id`, `execute_name`, `execute_type`, `redis_key`, `creator`, `creator_id`) VALUES (0,'{}','{}','{}','{}','{}','{}','{}','{}');""".format(
            self.create_time.split('.')[0],
            int(self.end_time),
            self.execute_id,
            self.execute_name,
            self.execute_type,
            log_id,
            self.execute_username,
            self.execute_user_id
        )
        project_db.create_data(sql)
        logger.success('=== save_logs ok ===')

    def gen_logs(self):
        """组装日志并保存"""

        case_summary = self.test_result.get_test_result()
        self.end_time = time.time()
        self.save_key = "test_log_{}_{}".format(str(int(time.time())), shortuuid.uuid())
        return_case_result = {
            "uuid": self.save_key,
            "execute_user_id": self.execute_user_id,
            "execute_username": self.execute_username,
            "execute_type": self.execute_type,
            "execute_name": self.execute_name,
            "case_result_list": self.case_result_list,
            "result_summary": case_summary,
            "create_time": self.create_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time": self.end_time - self.start_time
        }
        R.set(self.save_key, json.dumps(return_case_result))
        current_save_dict = gen_redis_first_logs(execute_id=self.execute_id)
        save_obj_first = current_save_dict.get(self.execute_type, "未知执行类型")
        R.set(save_obj_first, json.dumps(return_case_result))
        logger.success('=== save redis ok ===')
        self.save_logs(log_id=self.save_key)

    def only_execute(self):
        """
        执行一个用例 -> list[obj] 如: [{}]
        执行一批用例,一个用例场景 -> list[obj,obj,obj...] 如: [{},{},{}...]
        :return:
        """
        print('=== only_execute ===')

        for case_index, case in enumerate(self.case_generator, 1):
            self.sio.log('=== start case: {} ==='.format(case_index))
            self.current_case_resp_ass_error = 0
            case_info = case.get('case_info', {})
            bind_info = case.get('bind_info', [])

            self.case_id = case_info.get('id')
            self.case_name = case_info.get('case_name')

            self.request_base_url = case_info.get('request_base_url')
            self.request_url = case_info.get('request_url')
            self.request_method = case_info.get('request_method')
            self.update_var_list = []

            self.resp_json = {}
            self.resp_headers = {}

            if not bind_info:
                self.sio.log('=== 未配置请求参数 ===')

            for index, bind in enumerate(bind_info, 1):

                self.sio.log("=== 数据驱动:{} ===".format(index))
                case_data_info = bind.get('case_data_info', {})
                case_resp_ass_info = bind.get('case_resp_ass_info', [])
                case_field_ass_info = bind.get('case_field_ass_info', [])

                try:
                    self.test_result.req_success += 1
                    self.assemble_data_send(case_data_info=case_data_info)
                except BaseException as e:
                    self.sio.log("=== 请求失败:{} ===".format(str(e)), status="error")
                    self.test_result.req_error += 1
                    self.sio.log("=== 跳过断言 ===")
                    continue

                self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

                if not self.data_driven:
                    self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                    break

            self.sio.log('=== end case: {} ===\n\n'.format(case_index))

            add_case = {
                "report_tab": 1,
                "case_id": self.case_id,
                "case_name": self.case_name,
                "case_log": self.sio.get_stringio().split('\n'),
                "error": self.logs_error_switch
            }
            self.case_result_list.append(add_case)

        if not self.is_execute_all:
            self.gen_logs()

    def many_execute(self):
        """
        执行多个组用例
        list[list[obj,obj,obj], list[obj,obj,obj], list[obj,obj,obj]] 如: [[{},{},{}...], [{},{},{}...], [{},{},{}...] ...]
        :return:
        """
        print('=== many_execute ===')

        if self.is_execute_all:
            new_scenario_generator = self.scenario_generator
        else:
            new_scenario_generator = self.case_generator

        for group_index, group in enumerate(new_scenario_generator, 1):
            scenario_id = group.get('scenario_id')
            scenario_title = group.get('scenario_title')
            case_list = group.get('case_list')
            self.sio.log('=== start {}: scenario: {} ==='.format(scenario_id, scenario_title))
            scenario_log = []
            for case_index, case in enumerate(case_list, 1):
                self.sio.log('=== start case: {} ==='.format(case_index))
                self.current_case_resp_ass_error = 0
                case_info = case.get('case_info', {})
                bind_info = case.get('bind_info', [])

                self.case_id = case_info.get('id')
                self.case_name = case_info.get('case_name')

                self.request_base_url = case_info.get('request_base_url')
                self.request_url = case_info.get('request_url')
                self.request_method = case_info.get('request_method')
                self.update_var_list = []

                self.resp_json = {}
                self.resp_headers = {}

                if not bind_info:
                    self.sio.log('=== 未配置请求参数 ===')

                for index, bind in enumerate(bind_info, 1):
                    self.sio.log("=== 数据驱动:{} ===".format(index))
                    case_data_info = bind.get('case_data_info', {})
                    case_resp_ass_info = bind.get('case_resp_ass_info', [])
                    case_field_ass_info = bind.get('case_field_ass_info', [])

                    try:
                        self.test_result.req_success += 1
                        self.assemble_data_send(case_data_info=case_data_info)
                    except BaseException as e:
                        self.sio.log("=== 请求失败:{} ===".format(str(e)), status="error")
                        self.test_result.req_error += 1
                        self.sio.log("=== 跳过断言 ===")
                        continue

                    self.resp_check_ass_execute(case_resp_ass_info=case_resp_ass_info)

                    self.field_check_ass_execute(case_field_ass_info=case_field_ass_info)

                    if not self.data_driven:
                        self.sio.log("=== data_driven is false 只执行基础参数与断言 ===")
                        break

                add_case = {
                    "case_id": self.case_id,
                    "case_name": self.case_name,
                    "case_log": self.sio.get_stringio().split('\n'),
                    "error": self.logs_error_switch
                }
                scenario_log.append(add_case)

                self.sio.log(
                    '=== end {}: scenario: {} case: {}===\n\n'.format(scenario_id, scenario_title, case_index))
            add_group = {
                "report_tab": 2,
                "scenario_id": scenario_id,
                "scenario_title": scenario_title,
                "scenario_log": scenario_log,
                "error": self.logs_error_switch
            }
            self.case_result_list.append(add_group)

        if not self.is_execute_all:
            self.gen_logs()

    def all_execute(self):
        """执行用例与场景"""

        print('=== all_execute -> only_execute ===')
        self.only_execute()

        print('=== all_execute -> many_execute ===')
        self.many_execute()

        print('=== all_execute -> gen_logs ===')
        self.gen_logs()

    def save_test_repost(self, report_stt):
        """

        :param report_stt: 测试报告html字符
        :return:
        """

        self.report_name = f"Test_Report_{time.strftime('%Y-%m-%d_%H_%M_%S')}_.html"

        self.path = f"{os.getcwd().split('ExileTestPlatformServer')[0]}ExileTestPlatformServer/app/static/report/{self.report_name}"

        with open(self.path, "w", encoding="utf-8") as f:
            f.write(report_stt)

    def main(self):
        """main"""

        getattr(self, self.func_name)()

        get_data = R.get(self.save_key)
        get_data_to_dict = json.loads(get_data)
        test_repost = TemplateMixin(data=get_data_to_dict).generate_html_report()
        # print(test_repost)

        self.save_test_repost(report_stt=test_repost)

        result_summary = get_data_to_dict.get('result_summary')

        mt = f"#### 测试报告:{self.execute_name}  \n  > 测试人员:{self.execute_username}  \n  > 开始时间:{self.create_time}  \n  > 结束时间:{self.end_time}  \n  > 持续时间:{self.end_time - self.start_time}  \n  > 总数:{result_summary.get('req_count')}  \n  > 成功数:{result_summary.get('req_success')}  \n  > 失败数:{result_summary.get('resp_ass_fail')}  \n  > 错误数:{result_summary.get('req_error_rate')}  \n  > 通过率:{result_summary.get('resp_ass_success_rate')}  \n "

        if self.is_dd_push:
            MainTestExpand.dd_push(ding_talk_url=self.ding_talk_url, report_name=self.report_name, markdown_text=mt)

        # if self.is_send_mail:
            SendEmail(to_list=self.mail_list, ac_list=self.mail_list).send_attach(
                report_title=self.execute_name,
                html_file_path=self.path,
                mail_content="详情查看附件"
            )

        # os.system(f'rm {self.path}')

    def __str__(self):
        return '\n'.join(["{}:{}".format(k, v) for k, v in self.__dict__.items()])


if __name__ == '__main__':
    get_data = R.get("module_all_first_log:3")
    html_str = TemplateMixin(data=json.loads(get_data)).generate_html_report()
    print(html_str)
    report_name = f"Test_Report_{time.strftime('%Y-%m-%d_%H_%M_%S')}_.html"
    path = f"{os.getcwd().split('ExileTestPlatformServer')[0]}ExileTestPlatformServer/app/static/report/{report_name}"
    print(path)
    with open(path, "w",
              encoding="utf-8") as f:
        f.write(html_str)

    # print(os.system(f'rm {path}'))
