# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 2:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

from .demo_api.demo_api import TestApi
from .index_api.index_api import IndexApi
from .login_api.login_api import LoginApi
from .user_api.user_api import TouristApi, UserApi, UserPasswordApi, UserPageApi, UserProfileApi
from .case_env_api.case_env_api import CaseEnvApi, CaseEnvPageApi
from .case_api.case_api import CaseApi, CasePageApi, CaseCopyApi
from .case_data_api.case_data_api import CaseReqDataApi, CaseReqDataPageApi
from .case_var_api.case_var_api import CaseVarApi, CaseVarPageApi, CaseVarHistoryApi
from .case_db_api.case_db_api import CaseDBApi, CaseDBPageApi, CaseDBPingApi
from .case_logs_api.case_logs_api import CaseLogsPageApi
from .case_execute_logs_api.case_execute_logs_api import CaseExecuteLogsApi, CaseExecuteLogsPageApi
from .case_bind_api.case_bind_api import CaseBindApi, CaseBindDataApi, CaseBindRespAssApi, CaseBindFieldAssApi
from .case_ass_rule_api.case_ass_rule_api import RespAssertionRuleApi, FieldAssertionRuleApi, \
    RespAssertionRulePageApi, FieldAssertionRulePageApi
from .rule_test_api.rule_test_api import RuleTestApi
from .case_exec_api.case_exec_api import CaseExecApi, CaseReqTestApi
from .case_scenario_api.case_scenario_api import CaseScenarioApi, CaseScenarioPageApi
from .case_report_api.case_report_api import CaseRepostApi
from .case_set_api.case_set_api import CaseSetApi
from .mail_api.mail_api import MailApi, MailPageApi
from .dingding_api.dingding_api import DingDingApi, DingDingPushPageApi
from .platform_conf_api.platform_conf_api import PlatformConfApi
from .ui_auto_file_api.ui_auto_file_api import UiAutoFileApi, UiAutoFilePageApi
from .project_api.project_api import ProjectApi, ProjectPageApi
from .project_api.version_api import ProjectVersionApi, ProjectVersionPageApi, VersionBindCaseApi
from .project_api.version_task_api import VersionTaskApi, VersionTaskPageApi

api = Blueprint('api', __name__)
crm = Blueprint('crm', __name__)

api.add_url_rule('/test', view_func=TestApi.as_view('test_api'))

api.add_url_rule('/index', view_func=IndexApi.as_view('index_api'))
api.add_url_rule('/index/<version_id>', view_func=IndexApi.as_view('index_version_api'))

api.add_url_rule('/login', view_func=LoginApi.as_view('login_api'))

api.add_url_rule('/tourist', view_func=TouristApi.as_view('tourist_api'))
api.add_url_rule('/user', view_func=UserApi.as_view('user_api'))
api.add_url_rule('/user_pwd', view_func=UserPasswordApi.as_view('user_pwd'))
api.add_url_rule('/user_profile', view_func=UserProfileApi.as_view('user_profile'))
api.add_url_rule('/user_profile/<user_id>', view_func=UserProfileApi.as_view('user_detail'))
api.add_url_rule('/user_page', view_func=UserPageApi.as_view('user_page'))

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

api.add_url_rule('/case_var', view_func=CaseVarApi.as_view('case_var'))
api.add_url_rule('/case_var/<var_id>', view_func=CaseVarApi.as_view('case_var_detail'))
api.add_url_rule('/case_var_history', view_func=CaseVarHistoryApi.as_view('case_var_history'))
api.add_url_rule('/case_var_page', view_func=CaseVarPageApi.as_view('case_var_page'))

api.add_url_rule('/case_db', view_func=CaseDBApi.as_view('case_db'))
api.add_url_rule('/case_db/<db_id>', view_func=CaseDBApi.as_view('case_db_detail'))
api.add_url_rule('/case_db_page', view_func=CaseDBPageApi.as_view('case_db_page'))
api.add_url_rule('/case_db_ping/<db_id>', view_func=CaseDBPingApi.as_view('case_db_ping'))

api.add_url_rule('/case_logs_page', view_func=CaseLogsPageApi.as_view('case_logs_page'))
api.add_url_rule('/case_execute_logs', view_func=CaseExecuteLogsApi.as_view('case_execute_logs'))
api.add_url_rule('/case_execute_logs_page', view_func=CaseExecuteLogsPageApi.as_view('case_execute_logs_page'))

api.add_url_rule('/resp_ass_rule', view_func=RespAssertionRuleApi.as_view('resp_ass_rule'))
api.add_url_rule('/resp_ass_rule/<ass_resp_id>', view_func=RespAssertionRuleApi.as_view('resp_ass_rule_detail'))
api.add_url_rule('/resp_ass_rule_page', view_func=RespAssertionRulePageApi.as_view('resp_ass_rule_page'))

api.add_url_rule('/field_ass_rule', view_func=FieldAssertionRuleApi.as_view('field_ass_rule'))
api.add_url_rule('/field_ass_rule/<ass_field_id>', view_func=FieldAssertionRuleApi.as_view('field_ass_rule_detail'))
api.add_url_rule('/field_ass_rule_page', view_func=FieldAssertionRulePageApi.as_view('field_ass_rule_page'))

api.add_url_rule('/case_bind', view_func=CaseBindApi.as_view('case_bind'))
api.add_url_rule('/case_bind_data', view_func=CaseBindDataApi.as_view('case_bind_data'))
api.add_url_rule('/case_bind_resp_ass', view_func=CaseBindRespAssApi.as_view('case_bind_resp_ass'))
api.add_url_rule('/case_bind_field_ass', view_func=CaseBindFieldAssApi.as_view('case_bind_field_ass'))

api.add_url_rule('/case_scenario', view_func=CaseScenarioApi.as_view('case_scenario'))
api.add_url_rule('/case_scenario/<scenario_id>', view_func=CaseScenarioApi.as_view('case_scenario_detail'))
api.add_url_rule('/case_scenario_page', view_func=CaseScenarioPageApi.as_view('case_scenario_page'))

api.add_url_rule('/rule_test', view_func=RuleTestApi.as_view('rule_test'))
api.add_url_rule('/case_send', view_func=CaseReqTestApi.as_view('case_send'))
api.add_url_rule('/case_exec', view_func=CaseExecApi.as_view('case_exec'))
api.add_url_rule('/case_report', view_func=CaseRepostApi.as_view('case_report'))
api.add_url_rule('/case_set', view_func=CaseSetApi.as_view('case_set'))

api.add_url_rule('/mail_conf', view_func=MailApi.as_view('mail_conf'))
api.add_url_rule('/mail_conf_page', view_func=MailPageApi.as_view('mail_conf_page'))

api.add_url_rule('/dd_conf', view_func=DingDingApi.as_view('dd_conf'))
api.add_url_rule('/dd_conf_page', view_func=DingDingPushPageApi.as_view('dd_conf_page'))

api.add_url_rule('/platform_conf', view_func=PlatformConfApi.as_view('platform_conf'))

api.add_url_rule('/ui_auto_file', view_func=UiAutoFileApi.as_view('ui_auto_file'))
api.add_url_rule('/ui_auto_file/<file_id>', view_func=UiAutoFileApi.as_view('ui_auto_file_detail'))
api.add_url_rule('/ui_auto_file_page', view_func=UiAutoFilePageApi.as_view('ui_auto_file_page'))

api.add_url_rule('/project', view_func=ProjectApi.as_view('project'))
api.add_url_rule('/project/<project_id>', view_func=ProjectApi.as_view('project_detail'))
api.add_url_rule('/project_page', view_func=ProjectPageApi.as_view('project_page'))

api.add_url_rule('/project_version', view_func=ProjectVersionApi.as_view('project_version'))
api.add_url_rule('/project_version/<version_id>', view_func=ProjectVersionApi.as_view('project_version_detail'))
api.add_url_rule('/project_version_page', view_func=ProjectVersionPageApi.as_view('project_version_page'))

api.add_url_rule('/version_task', view_func=VersionTaskApi.as_view('version_task'))
api.add_url_rule('/version_task/<task_id>', view_func=VersionTaskApi.as_view('version_task_detail'))
api.add_url_rule('/version_task_page', view_func=VersionTaskPageApi.as_view('version_task_page'))

# api.add_url_rule('/version_bind_case', view_func=VersionBindCaseApi.as_view('version_bind_case'))
# api.add_url_rule('/version_bind_case/<version_id>', view_func=VersionBindCaseApi.as_view('version_bind_case_detail'))
