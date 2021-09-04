# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 2:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

from .api.index_api.index_api import IndexApi
from .api.case_env_api.case_env_api import CaseEnvApi, CaseEnvPageApi
from .api.case_api.case_api import CaseApi, CasePageApi
from .api.case_data_api.case_data_api import CaseReqDataApi, CaseReqDataPageApi
from .api.case_var_api.case_var_api import CaseVarApi, CaseVarPageApi
from .api.case_db_api.case_db_api import CaseDBApi, CaseDBPageApi
from .api.case_bind_api.case_bind_api import CaseBindDataApi, CaseBindRespAssApi, CaseBindFieldAssApi
from .api.case_ass_rule_api.case_ass_rule_api import RespAssertionRuleApi, FieldAssertionRuleApi, \
    RespAssertionRulePageApi, FieldAssertionRulePageApi
from .api.rule_test_api.rule_test_api import RuleTestApi
from .api.case_exec_api.case_exec_api import CaseExecApi

api = Blueprint('api', __name__)

api.add_url_rule('/', view_func=IndexApi.as_view('index_api'))

api.add_url_rule('/case_env', view_func=CaseEnvApi.as_view('case_env'))
api.add_url_rule('/case_env/<env_id>', view_func=CaseEnvApi.as_view('case_env_detail'))
api.add_url_rule('/case_env_page', view_func=CaseEnvPageApi.as_view('case_env_page'))

api.add_url_rule('/case', view_func=CaseApi.as_view('case'))
api.add_url_rule('/case/<case_id>', view_func=CaseApi.as_view('case_detail'))
api.add_url_rule('/case_page', view_func=CasePageApi.as_view('case_page'))

api.add_url_rule('/case_req_data', view_func=CaseReqDataApi.as_view('case_req_data'))
api.add_url_rule('/case_req_data/<req_data_id>', view_func=CaseReqDataApi.as_view('case_req_data_detail'))
api.add_url_rule('/case_req_data_page', view_func=CaseReqDataPageApi.as_view('case_req_data_page'))

api.add_url_rule('/case_var', view_func=CaseVarApi.as_view('case_var'))
api.add_url_rule('/case_var/<var_id>', view_func=CaseVarApi.as_view('case_var_detail'))
api.add_url_rule('/case_var_page', view_func=CaseVarPageApi.as_view('case_var_page'))

api.add_url_rule('/case_db', view_func=CaseDBApi.as_view('case_db'))
api.add_url_rule('/case_db/<db_id>', view_func=CaseDBApi.as_view('case_db_detail'))
api.add_url_rule('/case_db_page', view_func=CaseDBPageApi.as_view('case_db_page'))

api.add_url_rule('/resp_ass_rule', view_func=RespAssertionRuleApi.as_view('resp_ass_rule'))
api.add_url_rule('/resp_ass_rule/<ass_resp_id>', view_func=RespAssertionRuleApi.as_view('resp_ass_rule_detail'))
api.add_url_rule('/resp_ass_rule_page', view_func=RespAssertionRulePageApi.as_view('resp_ass_rule_page'))

api.add_url_rule('/field_ass_rule', view_func=FieldAssertionRuleApi.as_view('field_ass_rule'))
api.add_url_rule('/field_ass_rule/<ass_field_id>', view_func=FieldAssertionRuleApi.as_view('field_ass_rule_detail'))
api.add_url_rule('/field_ass_rule_page', view_func=FieldAssertionRulePageApi.as_view('field_ass_rule_page'))

api.add_url_rule('/case_bind_data', view_func=CaseBindDataApi.as_view('case_bind_data'))
api.add_url_rule('/case_bind_resp_ass', view_func=CaseBindRespAssApi.as_view('case_bind_resp_ass'))
api.add_url_rule('/case_bind_field_ass', view_func=CaseBindFieldAssApi.as_view('case_bind_field_ass'))

api.add_url_rule('/rule_test', view_func=RuleTestApi.as_view('rule_test'))

api.add_url_rule('/case_exec', view_func=CaseExecApi.as_view('case_exec'))
