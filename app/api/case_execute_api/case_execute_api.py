# -*- coding: utf-8 -*-
# @Time    : 2022/8/11 13:00
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_execute_api.py
# @Software: PyCharm


from all_reference import *
from common.libs.StringIOLog import StringIOLog

from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_case_assert.models import TestCaseAssertion
from app.models.test_project.models import (
    TestProject, TestProjectVersion, TestVersionTask, TestModuleApp,
    MidProjectAndCase, MidVersionCase, MidTaskCase, MidModuleCase,
    MidProjectScenario, MidVersionScenario, MidTaskScenario, MidModuleScenario
)
from app.models.test_env.models import TestEnv
from app.models.push_reminder.models import DingDingConfModel, MailConfModel


class GenExecuteData:
    """生成执行数据结构的用例"""

    @staticmethod
    def gen_structure(before_dict, first):
        """
        组装成执行需要的数据结构
        {
            "case_info":{},
            "bind_info":[
                {
                    "case_data_info":{},
                    "case_resp_ass_info":[],
                    "case_field_ass_info":[]
                }
            ]
        }
        :param before_dict: sql联表查询结果
        :param first: 首次建立
        :return:
        """
        bind = {
            "case_info": {
                "id": "",
                "is_deleted": "",
                "case_name": "2",
                "request_method": "",
                "request_base_url": "",
                "request_url": "",
                "is_shared": "",
                "is_public": "",
                "total_execution": "",
                "creator": "",
                "creator_id": "",
                "create_time": "",
                "create_timestamp": "",
                "modifier": "",
                "modifier_id": "",
                "update_time": "",
                "update_timestamp": "",
                "remark": "",
            },
            "bind_info": []
        }
        case_data_info = {
            "id": "",
            "data_name": "",
            "request_params": "",
            "request_headers": "",
            "request_body": "",
            "request_body_type": "",
            "var_list": "",
            "update_var_list": "",
            "is_deleted": "",
            "is_public": "",
            "creator": "",
            "creator_id": "",
            "create_time": "",
            "create_timestamp": "",
            "modifier": "",
            "modifier_id": "",
            "update_time": "",
            "update_timestamp": "",
            "remark": "",
            "is_before": "",
            "data_before": "",
            "is_after": "",
            "data_after": ""
        }
        case_resp_ass_info = GenExecuteData.gen_ass_resp_ass_info(before_dict.get('ass_resp_id_list', []))
        case_field_ass_info = GenExecuteData.gen_ass_field_ass_info(before_dict.get('ass_field_id_list', []))

        def _func():
            _key = "C."
            case_data_info['id'] = before_dict['data_id']
            case_data_info['is_deleted'] = before_dict[f'{_key}is_deleted']
            case_data_info['is_public'] = before_dict[f'{_key}is_public']
            case_data_info['creator'] = before_dict[f'{_key}creator']
            case_data_info['creator_id'] = before_dict[f'{_key}creator_id']
            case_data_info['create_time'] = before_dict[f'{_key}create_time']
            case_data_info['create_timestamp'] = before_dict[f'{_key}create_timestamp']
            case_data_info['modifier'] = before_dict[f'{_key}modifier']
            case_data_info['modifier_id'] = before_dict[f'{_key}modifier_id']
            case_data_info['update_time'] = before_dict[f'{_key}update_time']
            case_data_info['update_timestamp'] = before_dict[f'{_key}update_timestamp']
            case_data_info['remark'] = before_dict[f'{_key}remark']

        if first:
            for key, val in before_dict.items():
                if key in bind['case_info']:
                    bind['case_info'][key] = val

                if key in case_data_info:
                    case_data_info[key] = val
            _func()
            b = {
                "case_data_info": case_data_info,
                "case_resp_ass_info": case_resp_ass_info,
                "case_field_ass_info": case_field_ass_info
            }
            bind['bind_info'].append(b)
            return bind
        else:

            for key, val in before_dict.items():
                if key in case_data_info:
                    case_data_info[key] = val
            _func()
            b = {
                "case_data_info": case_data_info,
                "case_resp_ass_info": case_resp_ass_info,
                "case_field_ass_info": case_field_ass_info
            }
            return b

    @staticmethod
    def gen_ass_resp_ass_info(id_list):
        """

        :return:
        """
        if not id_list:
            return []

        query_ass = TestCaseAssResponse.query.filter(
            TestCaseAssResponse.is_deleted == 0,
            TestCaseAssResponse.id.in_(id_list)).all()

        return [ass.to_json() for ass in query_ass]

    @staticmethod
    def gen_ass_field_ass_info(id_list):
        """

        :return:
        """
        if not id_list:
            return []

        query_ass = TestCaseAssField.query.filter(
            TestCaseAssField.is_deleted == 0,
            TestCaseAssField.id.in_(id_list)).all()

        return [ass.to_json() for ass in query_ass]

    @staticmethod
    def main(case_id_list=None, query_list=None, case_expand_map=None):
        """

        :param case_id_list: 用例id列表不去重
        :param query_list:  用例查询结果
        :param case_expand_map: 用例扩展参数
        :return:
        """

        case_expand_map = case_expand_map if case_expand_map else {}
        current_dict = {}

        for index, query in enumerate(query_list):
            if query['id'] in current_dict:
                case_data_info = GenExecuteData.gen_structure(before_dict=query, first=False)
                current_dict[query['id']]['bind_info'].append(case_data_info)
            else:
                current_dict[query['id']] = GenExecuteData.gen_structure(before_dict=query, first=True)

        # print(json.dumps(current_dict, ensure_ascii=False))
        # print(case_id_list)

        new_list = []
        for _id in case_id_list:
            if _id in current_dict:
                case = current_dict.get(_id)
                if _id in case_expand_map:
                    case_expand_list = case_expand_map.get(_id)
                    if len(case_expand_list) > 1:
                        cp_case = copy.deepcopy(case)
                        cp_case['case_expand'] = case_expand_list[0]
                        del case_expand_map.get(_id)[0]
                        new_list.append(cp_case)
                    else:
                        case['case_expand'] = case_expand_list[0]
                        new_list.append(case)
                else:
                    new_list.append(case)

        # print(json.dumps(new_list, ensure_ascii=False))
        return new_list


class QueryExecuteData:
    """查询执行参数组装"""

    @staticmethod
    def query_case_assemble(case_id_list):
        """
        用例组装
        :param case_id_list: 用例 id 列表
        :return:
        """

        sql = f"""
            SELECT
                A.id,
                A.is_deleted,
                A.case_name,
                A.request_method,
                A.request_base_url,
                A.request_url,
                A.is_shared,
                A.is_public,
                A.total_execution,
                A.creator,
                A.creator_id,
                A.create_time,
                A.create_timestamp,
                A.modifier,
                A.modifier_id,
                A.update_time,
                A.update_timestamp,
                A.remark,
                C.id AS data_id,
                C.data_name,
                C.request_params,
                C.request_headers,
                C.request_body,
                C.request_body_type,
                C.var_list,
                C.update_var_list,
                C.is_deleted,
                C.is_public,
                C.creator,
                C.creator_id,
                C.create_time,
                C.create_timestamp,
                C.modifier,
                C.modifier_id,
                C.update_time,
                C.update_timestamp,
                C.remark,
                C.is_before,
                C.data_before,
                C.is_after,
                C.data_after,
                B.ass_resp_id_list,
                B.ass_field_id_list
            FROM
                exile_test_case AS A
                INNER JOIN exile_ass_bind AS B ON A.id = B.case_id
                INNER JOIN exile_test_case_data AS C ON B.data_id = C.id
            WHERE
                A.is_deleted = 0
                AND B.is_deleted = 0
                AND C.is_deleted = 0
                {f'AND B.case_id={case_id_list[-1]}' if len(case_id_list) == 1 else f'AND B.case_id in {tuple(case_id_list)}'}
                {'' if len(case_id_list) == 1 else f"ORDER BY FIELD(A.id,{','.join(list(map(str, case_id_list)))})"}
            """
        # print(sql)
        result = project_db.select(sql)
        return result


class ExecuteMain:
    """执行"""

    @classmethod
    def single_use_case(cls):
        """单个用例"""

    @classmethod
    def single_scene(cls):
        """单个场景"""

    @classmethod
    def execute_all(cls):
        """执行所有用例和场景"""

    @classmethod
    def execute_all_use_cases(cls):
        """执行所有用例"""

    @classmethod
    def execute_all_scenarios(cls):
        """执行所有场景"""


execute_func_dict = {
    "case": ExecuteMain.single_use_case,
    "scenario": ExecuteMain.single_scene,

    "project_all": ExecuteMain.execute_all,
    "project_case": ExecuteMain.execute_all_use_cases,
    "project_scenario": ExecuteMain.execute_all_scenarios,

    "version_all": ExecuteMain.execute_all,
    "version_case": ExecuteMain.execute_all_use_cases,
    "version_scenario": ExecuteMain.execute_all_scenarios,

    "task_all": ExecuteMain.execute_all,
    "task_case": ExecuteMain.execute_all_use_cases,
    "task_scenario": ExecuteMain.execute_all_scenarios,

    "module_all": ExecuteMain.execute_all,
    "module_case": ExecuteMain.execute_all_use_cases,
    "module_scenario": ExecuteMain.execute_all_scenarios
}


class CaseExecuteApi(MethodView):
    """
    执行用例 Api
    POST: 执行用例
    """

    def post(self):
        """
        执行
        :return:
        """

        data = request.get_json()

        execute_id = data.get('execute_id')
        execute_type = data.get('execute_type')
        execute_label = data.get('execute_label')
        is_env_cover = data.get('is_env_cover')
        env_url_id = data.get('env_url_id')
        data_driven = data.get('data_driven', False)
        use_dd_push = data.get('use_dd_push', False)
        dd_push_id = data.get('dd_push_id')
        use_mail = data.get('use_mail', False)
        mail_send_all = data.get('mail_send_all', False)
        mail_list = data.get('mail_list', [])

        if is_env_cover:
            query_base_url = TestEnv.query.get(env_url_id)
            if not query_base_url:
                return api_result(code=NO_DATA, message="环境不存在")
            if query_base_url.is_deleted != 0:
                return api_result(code=BUSINESS_ERROR, message=f"环境: {query_base_url.env_name} 被禁用")

            base_url = query_base_url.env_url
            use_base_url = True
        else:
            base_url = ''
            use_base_url = False

        if use_dd_push:
            query_dd_push = DingDingConfModel.query.get(dd_push_id)
            if not query_dd_push:
                return api_result(code=NO_DATA, message="钉钉群不存在")
            if query_dd_push.is_deleted != 0:
                return api_result(code=BUSINESS_ERROR, message=f"钉钉群: {query_dd_push.title} 被禁用")

            ding_talk_url = query_dd.ding_talk_url

        if use_mail:
            if mail_send_all:
                mail_list = [m.mail for m in MailConfModel.query.filter_by(is_deleted=0).all()]
            else:
                mail_list = [m.mail for m in MailConfModel.query.filter(
                    MailConfModel.id.in_(mail_list),
                    MailConfModel.is_deleted == 0
                ).all()]

        if mail_send_all and not mail_list:
            return api_result(code=BUSINESS_ERROR, message="邮件不能为空，或者邮件已禁用")

        if execute_type not in execute_type_tuple:
            return api_result(code=TYPE_ERROR, message='请先选择用例场景')

        # test_obj = {
        #     "execute_id": execute_id,
        #     "execute_name": execute_name,
        #     "execute_type": execute_type,
        #     "execute_label": execute_label,
        #     "execute_user_id": g.app_user.id,
        #     "execute_username": g.app_user.username,
        #     "base_url": base_url,
        #     "use_base_url": use_base_url,
        #     "data_driven": data_driven,
        #     "is_execute_all": is_execute_all,
        #     "case_list": [],
        #     "scenario_list": [],
        #     "is_dd_push": is_dd_push,
        #     "dd_push_id": dd_push_id,
        #     "ding_talk_url": ding_talk_url,
        #     "is_send_mail": is_send_mail,
        #     "mail_list": mail_list,
        #     "trigger_type": trigger_type,
        #     "request_timeout": request_timeout,
        # }
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=[])
