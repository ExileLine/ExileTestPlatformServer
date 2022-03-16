# -*- coding: utf-8 -*-
# @Time    : 2022/3/15 4:25 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : report_template.py
# @Software: PyCharm


class RepostTemplate:
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
        <p>结束时间 : {{resp.end_time}}</p>
        <p>合计耗时 : {{resp.total_time}}s</p>
        <p>用例总数 : {{resp.result_summary.all_test_count}}</p>
        <p>成功数 : {{resp.result_summary.pass_count}}</p>
        <p>失败数 : {{resp.result_summary.fail_count}}</p>
        <p>通过率 : {{resp.result_summary.pass_rate}}</p>
      </div>

      <el-tabs>
        <el-tab-pane
          :label="`所有(${resp.result_summary.all_test_count})`"
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
          :label="`成功(${resp.result_summary.pass_count})`"
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
          :label="`失败(${resp.result_summary.fail_count})`"
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
