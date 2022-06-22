# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 11:58
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : clear_cache.py
# @Software: PyCharm

from common.libs.db import R, project_db


class ClearCache:

    @classmethod
    def clear_test_log(cls):
        """清空日志"""

        all_test_log = R.keys(pattern="test_log_*")
        list(map(lambda x: R.delete(x), all_test_log))
        return len(all_test_log)

    @classmethod
    def clear_first_log(cls):
        """清空最新日志"""

        all_case_first = R.keys(pattern="case_first_log:*")
        all_scenario_first = R.keys(pattern="scenario_first_log:*")
        list(map(lambda x: R.delete(x), all_case_first))
        list(map(lambda x: R.delete(x), all_scenario_first))

        all_project_all_first = R.keys(pattern="project_all_first_log:*")
        all_project_case_first = R.keys(pattern="project_case_first_log:*")
        all_project_scenario_first = R.keys(pattern="project_scenario_first_log:*")
        list(map(lambda x: R.delete(x), all_project_all_first))
        list(map(lambda x: R.delete(x), all_project_case_first))
        list(map(lambda x: R.delete(x), all_project_scenario_first))

        all_version_all_first = R.keys(pattern="version_all_first_log:*")
        all_version_case_first = R.keys(pattern="version_case_first_log:*")
        all_version_scenario_first = R.keys(pattern="version_scenario_first_log:*")
        list(map(lambda x: R.delete(x), all_version_all_first))
        list(map(lambda x: R.delete(x), all_version_case_first))
        list(map(lambda x: R.delete(x), all_version_scenario_first))

        all_task_all_first = R.keys(pattern="task_all_first_log:*")
        all_task_case_first = R.keys(pattern="task_case_first_log:*")
        all_task_scenario_first = R.keys(pattern="task_scenario_first_log:*")
        list(map(lambda x: R.delete(x), all_task_all_first))
        list(map(lambda x: R.delete(x), all_task_case_first))
        list(map(lambda x: R.delete(x), all_task_scenario_first))

        all_module_all_first = R.keys(pattern="module_all_first_log:*")
        all_module_case_first = R.keys(pattern="module_case_first_log:*")
        all_module_scenario_first = R.keys(pattern="module_scenario_first_log:*")
        all_module_app_first = R.keys(pattern="module_app_first_log:*")
        list(map(lambda x: R.delete(x), all_module_all_first))
        list(map(lambda x: R.delete(x), all_module_case_first))
        list(map(lambda x: R.delete(x), all_module_scenario_first))
        list(map(lambda x: R.delete(x), all_module_app_first))
        d = {
            "all_case_first": len(all_case_first),
            "all_scenario_first": len(all_scenario_first),

            "all_project_all_first": len(all_project_all_first),
            "all_project_case_first": len(all_project_case_first),
            "all_project_scenario_first": len(all_project_scenario_first),

            "all_version_all_first": len(all_version_all_first),
            "all_version_case_first": len(all_version_case_first),
            "all_version_scenario_first": len(all_version_scenario_first),

            "all_task_all_first": len(all_task_all_first),
            "all_task_case_first": len(all_task_case_first),
            "all_task_scenario_first": len(all_task_scenario_first),

            "all_module_all_first": len(all_module_all_first),
            "all_module_case_first": len(all_module_case_first),
            "all_module_scenario_first": len(all_module_scenario_first),
            "all_module_app_first": len(all_module_app_first)
        }
        return d

    @classmethod
    def clear_cicd(cls):
        """清空手动触发cicd记录"""

        all_cicd_admin = R.keys(pattern="test_cicd_admin_*")
        list(map(lambda x: R.delete(x), all_cicd_admin))

        return {
            "all_cicd_admin": len(all_cicd_admin)
        }

    @classmethod
    def clear_exile_test_logs(cls):
        """清空db执行记录与操作记录"""

        result1 = project_db.execute_sql("""TRUNCATE exile_test_logs;""")
        result2 = project_db.execute_sql("""TRUNCATE exile_test_execute_logs;""")
        return [result1, result2]


if __name__ == '__main__':
    ClearCache.clear_test_log()
    ClearCache.clear_first_log()
    ClearCache.clear_cicd()
    ClearCache.clear_exile_test_logs()
