# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 2:12 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : __init__.py.py
# @Software: PyCharm


from flask import Blueprint

from .api.index.index import IndexApi
from .api.case_api.case_api import CaseApi, CaseReqDataApi, CaseBindDataApi, CaseBindRespAssApi, CaseBindFieldAssApi, \
    CasePageApi
from .api.case_var_api.case_var_api import CaseVarApi, CaseVarPageApi
from .api.case_ass_rule_api.case_ass_rule_api import RespAssertionRuleApi, FieldAssertionRuleApi, RuleTestApi

api = Blueprint('api', __name__)

api.add_url_rule('/', view_func=IndexApi.as_view('index'))
api.add_url_rule('/case', view_func=CaseApi.as_view('case'))
api.add_url_rule('/case/<case_id>', view_func=CaseApi.as_view('case_detail'))
api.add_url_rule('/case_page', view_func=CasePageApi.as_view('case_page'))

api.add_url_rule('/case_var', view_func=CaseVarApi.as_view('case_var'))
api.add_url_rule('/case_var/<var_id>', view_func=CaseVarApi.as_view('case_var_detail'))
api.add_url_rule('/case_var_page', view_func=CaseVarPageApi.as_view('case_var_page'))

api.add_url_rule('/case_req_data', view_func=CaseReqDataApi.as_view('case_req_data'))
api.add_url_rule('/case_req_data/<req_data_id>', view_func=CaseReqDataApi.as_view('case_req_data_detail'))

api.add_url_rule('/resp_ass_rule', view_func=RespAssertionRuleApi.as_view('resp_ass_rule'))
api.add_url_rule('/resp_ass_rule/<ass_resp_id>', view_func=RespAssertionRuleApi.as_view('resp_ass_rule_detail'))
api.add_url_rule('/field_ass_rule', view_func=FieldAssertionRuleApi.as_view('field_ass_rule'))
api.add_url_rule('/field_ass_rule/<ass_field_id>', view_func=FieldAssertionRuleApi.as_view('field_ass_rule_detail'))

api.add_url_rule('/case_bind_data', view_func=CaseBindDataApi.as_view('case_bind_data'))
api.add_url_rule('/case_bind_resp_ass', view_func=CaseBindRespAssApi.as_view('case_bind_resp_ass'))
api.add_url_rule('/case_bind_field_ass', view_func=CaseBindFieldAssApi.as_view('case_bind_field_ass'))

api.add_url_rule('/rule_test', view_func=RuleTestApi.as_view('rule_test'))
