# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 2:12 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

from .demo_api.demo_api import TestApi, TestCeleryAsyncTaskApi
from .index_api.index_api import IndexApi
from .login_api.login_api import LoginApi
from .user_api.user_api import TouristApi, UserApi, UserPasswordApi, UserPageApi, UserProfileApi
from .auth_api.auth_api import AuthApi
from .case_env_api.case_env_api import CaseEnvApi, CaseEnvPageApi
from .case_api.case_api import CaseApi, CasePageApi, CaseCopyApi
from .case_data_api.case_data_api import CaseReqDataApi, CaseReqDataPageApi
from .case_variable_api.case_variable_api import CaseVarApi, CaseVarPageApi, CaseVarHistoryApi
from .case_db_api.case_db_api import CaseDBApi, CaseDBPageApi, CaseDBPingApi
from .case_logs_api.case_logs_api import CaseLogsPageApi
from .case_execute_logs_api.case_execute_logs_api import CaseExecuteLogsApi, CaseExecuteLogsPageApi
from .case_report_api.case_report_api import CaseReportApi
from .case_bind_api.case_bind_api import CaseBindApi
from .case_assertion_api.case_assertion_api import RespAssertionRuleApi, FieldAssertionRuleApi, AssertionRulePageApi
from .rule_test_api.rule_test_api import RuleTestApi
from .case_exec_api.case_exec_api import CaseExecApi
from .case_exec_api.case_send_api import CaseRequestSendApi
from .case_exec_api.case_cicd_api import CaseCICDApi, CaseCICDMapApi, CaseCICDMapPageApi
from .case_execute_api.case_execute_api import CaseExecuteApi
from .case_scenario_api.case_scenario_api import CaseScenarioApi, CaseScenarioPageApi
from .case_set_api.case_set_api import CaseSetApi
from .mail_api.mail_api import MailApi, MailPageApi
from .dingding_api.dingding_api import DingDingApi, DingDingPushPageApi
from .platform_conf_api.platform_conf_api import PlatformConfApi
from .project_api.project_api import ProjectApi, ProjectPageApi
from .project_api.version_api import ProjectVersionApi, ProjectVersionPageApi
from .project_api.version_task_api import VersionTaskApi, VersionTaskPageApi
from .project_api.module_app_api import ModuleAppApi, ModuleAppPageApi
from .timed_task_api.timed_task_api import APSchedulerTaskApi, APSchedulerTaskStatusApi, APSchedulerTaskPageApi
from .download_file_api.download_file_api import DownloadFileApi
from .file_import_api.file_import_api import InterfaceFileImportApi

api = Blueprint('api', __name__)
crm = Blueprint('crm', __name__)

api.add_url_rule('/test', view_func=TestApi.as_view('test_api'))
api.add_url_rule('/test_celery', view_func=TestCeleryAsyncTaskApi.as_view('test_celery'))

api.add_url_rule('/index', view_func=IndexApi.as_view('index_api'))
api.add_url_rule('/index/<version_id>', view_func=IndexApi.as_view('index_version_api'))

api.add_url_rule('/login', view_func=LoginApi.as_view('login_api'))

api.add_url_rule('/tourist', view_func=TouristApi.as_view('tourist_api'))
api.add_url_rule('/user', view_func=UserApi.as_view('user_api'))
api.add_url_rule('/user/<user_id>', view_func=UserApi.as_view('user_detail'))
api.add_url_rule('/user_pwd', view_func=UserPasswordApi.as_view('user_pwd'))
api.add_url_rule('/user_profile', view_func=UserProfileApi.as_view('user_profile'))
api.add_url_rule('/user_profile/<user_id>', view_func=UserProfileApi.as_view('user_profile_detail'))
api.add_url_rule('/user_page', view_func=UserPageApi.as_view('user_page'))

api.add_url_rule('/auth', view_func=AuthApi.as_view('auth_api'))

api.add_url_rule('/case_env', view_func=CaseEnvApi.as_view('case_env'))
api.add_url_rule('/case_env/<env_id>', view_func=CaseEnvApi.as_view('case_env_detail'))
api.add_url_rule('/case_env_page', view_func=CaseEnvPageApi.as_view('case_env_page'))

api.add_url_rule('/case', view_func=CaseApi.as_view('case'))
api.add_url_rule('/case/<case_id>', view_func=CaseApi.as_view('case_detail'))
api.add_url_rule('/case_page', view_func=CasePageApi.as_view('case_page'))
api.add_url_rule('/case_copy', view_func=CaseCopyApi.as_view('case_copy'))

api.add_url_rule('/case_req_data', view_func=CaseReqDataApi.as_view('case_req_data'))
api.add_url_rule('/case_req_data/<req_data_id>', view_func=CaseReqDataApi.as_view('case_req_data_detail'))
api.add_url_rule('/case_req_data_page', view_func=CaseReqDataPageApi.as_view('case_req_data_page'))

api.add_url_rule('/case_variable', view_func=CaseVarApi.as_view('case_variable'))
api.add_url_rule('/case_variable/<var_id>', view_func=CaseVarApi.as_view('case_variable_detail'))
api.add_url_rule('/case_var_history', view_func=CaseVarHistoryApi.as_view('case_var_history'))
api.add_url_rule('/case_variable_page', view_func=CaseVarPageApi.as_view('case_variable_page'))

api.add_url_rule('/case_db', view_func=CaseDBApi.as_view('case_db'))
api.add_url_rule('/case_db/<db_id>', view_func=CaseDBApi.as_view('case_db_detail'))
api.add_url_rule('/case_db_page', view_func=CaseDBPageApi.as_view('case_db_page'))
api.add_url_rule('/case_db_ping/<db_id>', view_func=CaseDBPingApi.as_view('case_db_ping'))

api.add_url_rule('/case_logs_page', view_func=CaseLogsPageApi.as_view('case_logs_page'))
api.add_url_rule('/case_execute_logs/<redis_key>', view_func=CaseExecuteLogsApi.as_view('case_execute_logs'))
api.add_url_rule('/case_execute_logs', view_func=CaseExecuteLogsApi.as_view('case_execute_logs_first'))
api.add_url_rule('/case_execute_logs_page', view_func=CaseExecuteLogsPageApi.as_view('case_execute_logs_page'))

api.add_url_rule('/case_report/<redis_key>', view_func=CaseReportApi.as_view('case_report'))

api.add_url_rule('/resp_ass_rule', view_func=RespAssertionRuleApi.as_view('resp_ass_rule'))
api.add_url_rule('/resp_ass_rule/<ass_resp_id>', view_func=RespAssertionRuleApi.as_view('resp_ass_rule_detail'))
api.add_url_rule('/field_ass_rule', view_func=FieldAssertionRuleApi.as_view('field_ass_rule'))
api.add_url_rule('/field_ass_rule/<ass_field_id>', view_func=FieldAssertionRuleApi.as_view('field_ass_rule_detail'))
api.add_url_rule('/assertion_page', view_func=AssertionRulePageApi.as_view('assertion_page'))

api.add_url_rule('/case_bind', view_func=CaseBindApi.as_view('case_bind'))

api.add_url_rule('/case_scenario', view_func=CaseScenarioApi.as_view('case_scenario'))
api.add_url_rule('/case_scenario/<scenario_id>', view_func=CaseScenarioApi.as_view('case_scenario_detail'))
api.add_url_rule('/case_scenario_page', view_func=CaseScenarioPageApi.as_view('case_scenario_page'))

api.add_url_rule('/rule_test', view_func=RuleTestApi.as_view('rule_test'))
api.add_url_rule('/case_send', view_func=CaseRequestSendApi.as_view('case_send'))
api.add_url_rule('/case_exec', view_func=CaseExecApi.as_view('case_exec'))
api.add_url_rule('/case_execute', view_func=CaseExecuteApi.as_view('case_execute'))
api.add_url_rule('/open_exec', view_func=CaseExecApi.as_view('open_exec'))
api.add_url_rule('/case_set', view_func=CaseSetApi.as_view('case_set'))

api.add_url_rule('/mail_conf', view_func=MailApi.as_view('mail_conf'))
api.add_url_rule('/mail_conf_page', view_func=MailPageApi.as_view('mail_conf_page'))

api.add_url_rule('/dd_conf', view_func=DingDingApi.as_view('dd_conf'))
api.add_url_rule('/dd_conf_page', view_func=DingDingPushPageApi.as_view('dd_conf_page'))

api.add_url_rule('/platform_conf', view_func=PlatformConfApi.as_view('platform_conf'))

api.add_url_rule('/project', view_func=ProjectApi.as_view('project'))
api.add_url_rule('/project/<project_id>', view_func=ProjectApi.as_view('project_detail'))
api.add_url_rule('/project_page', view_func=ProjectPageApi.as_view('project_page'))

api.add_url_rule('/project_version', view_func=ProjectVersionApi.as_view('project_version'))
api.add_url_rule('/project_version/<version_id>', view_func=ProjectVersionApi.as_view('project_version_detail'))
api.add_url_rule('/project_version_page', view_func=ProjectVersionPageApi.as_view('project_version_page'))

api.add_url_rule('/version_task', view_func=VersionTaskApi.as_view('version_task'))
api.add_url_rule('/version_task/<task_id>', view_func=VersionTaskApi.as_view('version_task_detail'))
api.add_url_rule('/version_task_page', view_func=VersionTaskPageApi.as_view('version_task_page'))

api.add_url_rule('/module_app', view_func=ModuleAppApi.as_view('module_app'))
api.add_url_rule('/module_app/<module_id>', view_func=ModuleAppApi.as_view('module_app_detail'))
api.add_url_rule('/module_app_page', view_func=ModuleAppPageApi.as_view('module_app_page'))

api.add_url_rule('/timed_task/<timed_task_uuid>', view_func=APSchedulerTaskApi.as_view('timed_task_detail'))
api.add_url_rule('/timed_task', view_func=APSchedulerTaskApi.as_view('timed_task'))
api.add_url_rule('/timed_task_status', view_func=APSchedulerTaskStatusApi.as_view('timed_task_status'))
api.add_url_rule('/timed_task_page', view_func=APSchedulerTaskPageApi.as_view('timed_task_page'))

api.add_url_rule('/download_file', view_func=DownloadFileApi.as_view('download_file'))

api.add_url_rule('/import_file', view_func=InterfaceFileImportApi.as_view('import_file'))

api.add_url_rule('/open_cicd', view_func=CaseCICDApi.as_view('open_cicd'))
api.add_url_rule('/open_cicd/<cicd_id>', view_func=CaseCICDApi.as_view('open_cicd_test'))
api.add_url_rule('/cicd_map', view_func=CaseCICDMapApi.as_view('cicd_map'))
api.add_url_rule('/cicd_map_page', view_func=CaseCICDMapPageApi.as_view('cicd_map_page'))
