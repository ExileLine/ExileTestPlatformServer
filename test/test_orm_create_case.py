# -*- coding: utf-8 -*-
# @Time    : 2021/10/1 2:01 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_orm_create_case.py
# @Software: PyCharm

api_list = [
    '/api/case_execute_logs_page',
    '/api/field_ass_rule_page',
    '/api/case_bind_field_ass',
    '/api/case_req_data_page',
    '/api/resp_ass_rule_page',
    '/api/case_bind_resp_ass',
    '/api/case_scenario_page',
    '/api/case_execute_logs',
    '/api/case_logs_page',
    '/api/field_ass_rule',
    '/api/case_bind_data',
    '/api/case_env_page',
    '/api/case_req_data',
    '/api/case_var_page',
    '/api/resp_ass_rule',
    '/api/case_scenario',
    '/api/case_db_page',
    '/api/case_report',
    '/api/user_page',
    '/api/case_page',
    '/api/case_bind',
    '/api/rule_test',
    '/api/case_send',
    '/api/case_exec',
    '/api/case_env',
    '/api/case_var',
    '/api/case_set',
    '/api/tourist',
    '/api/case_db',
    '/api/index',
    '/api/login',
    '/api/case',
    '/api/field_ass_rule/<ass_field_id>',
    '/api/case_req_data/<req_data_id>',
    '/api/resp_ass_rule/<ass_resp_id>',
    '/api/case_scenario/<scenario_id>',
    '/api/case_env/<env_id>',
    '/api/case_var/<var_id>',
    '/api/case_db/<db_id>',
    '/api/case/<case_id>',
    '/static/<filename>'
]
request_method = ["GET", "POST", "PUT", "DELETE"]
if __name__ == '__main__':
    import random
    from common.libs.set_app_context import set_app_context
    from app.models.test_case.models import TestCase, db


    @set_app_context
    def main():
        for index, url in enumerate(api_list, 1):
            new_test_case = TestCase(
                case_name="测试:" + url,
                request_method=random.choice(request_method),
                request_base_url="http://0.0.0.0:7272",
                request_url=url,
                is_shared=True,
                is_public=True,
                remark="脚本生成:{}".format(index),
                creator="脚本生成:{}".format(index),
                creator_id=999999,
                total_execution=random.randint(1, 99)
            )
            db.session.add(new_test_case)
        db.session.commit()


    @set_app_context
    def main1():
        all_case = TestCase.query.all()
        for index, case in enumerate(all_case, 1):
            case.request_method = random.choice(request_method)
            case.modifier = "脚本生成:{}".format(random.randint(1, len(all_case)))
            case.modifier_id = 888888
        db.session.commit()


    # main()
    main1()
