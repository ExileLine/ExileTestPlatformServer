# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm
import json
import queue
from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from common.libs.StringIOLog import StringIOLog
from app.models.test_case.models import TestCase
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import (
    TestProject, TestProjectVersion, TestVersionTask, TestModuleApp,
    MidProjectAndCase, MidVersionCase, MidTaskCase, MidModuleCase,
    MidProjectScenario, MidVersionScenario, MidTaskScenario, MidModuleScenario
)
from app.models.test_env.models import TestEnv
from app.models.test_logs.models import TestLogs
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from tasks.task03 import execute_main

model_dict = {
    "project": {
        "case": MidProjectAndCase,
        "scenario": MidProjectScenario,
    },
    "version": {
        "case": MidVersionCase,
        "scenario": MidVersionScenario,
    },
    "task": {
        "case": MidTaskCase,
        "scenario": MidTaskScenario,
    },
    "module": {
        "case": MidModuleCase,
        "scenario": MidModuleScenario,
    }
}
key_dict = {
    "project": {
        "class": TestProject,
        "name": "project_name",
        "title": "项目",
    },
    "version": {
        "class": TestProjectVersion,
        "name": "version_name",
        "title": "版本迭代",
    },
    "task": {
        "class": TestVersionTask,
        "name": "task_name",
        "title": "任务",
    },
    "module": {
        "class": TestModuleApp,
        "name": "module_name",
        "title": "模块",
    }
}


def save_test_logs(execute_type):
    tl = TestLogs(
        log_type=execute_type,
        creator=g.app_user.username,
        creator_id=g.app_user.id
    )
    tl.save()


def safe_scan():
    """1"""
    return False


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
    def update_case_total_execution(case_id_list):
        """更新用例执行数"""

        sql = f"""
        UPDATE exile_test_case 
        SET total_execution = total_execution +1 
        WHERE 
        {f'id={case_id_list[-1]}' if len(case_id_list) == 1 else f'id in {tuple(case_id_list)}'}
        """
        project_db.update(sql)
        print(f'共 {len(case_id_list)} 条, 更新用例执行数成功:{case_id_list}')

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

    @staticmethod
    def query_scenario_assemble(query_scenario_result):
        """
        组装用例场景下的用例,返回执行需要的数据格式
        :param query_scenario_result: 查询用例场景结果集
        :return:
        """
        scenario_list = []
        for scenario in query_scenario_result:
            case_list = scenario.get('case_list')
            if case_list:
                sort_case_list = list(filter(lambda x: not x.get('is_active'),
                                             sorted(case_list, key=lambda x: x.get("index"), reverse=True)))

                case_expand_map = {}
                for obj in sort_case_list:
                    case_id = obj.get('case_id')
                    if case_id in case_expand_map:
                        case_expand_map.get(case_id).append(obj)
                    else:
                        case_expand_map[case_id] = [obj]

                case_id_list = [obj.get('case_id') for obj in sort_case_list]
                # QueryExecuteData.update_case_total_execution(case_id_list)
                query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
                case_list = GenExecuteData.main(case_id_list, query_case_zip_list, case_expand_map)

                scenario_obj = {
                    "scenario_id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": case_list
                }

                scenario_list.append(scenario_obj)
        return scenario_list

    @staticmethod
    def gen_execute_case_list(**kwargs):
        """
        生成需要执行【用例】数据
        :param kwargs:
        :return:
        """
        execute_type = kwargs.get('execute_dict_key', '')
        query = kwargs.get('query')
        model = model_dict.get(execute_type).get('case')
        query_pc = model.query.filter_by(**query, is_deleted=0).all()

        if not query_pc:
            return []

        case_id_list = [obj.case_id for obj in query_pc]
        query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
        case_list = GenExecuteData.main(case_id_list, query_case_zip_list)
        # QueryExecuteData.update_case_total_execution(case_id_list)
        return case_list

    @staticmethod
    def gen_execute_scenario_list(**kwargs):
        """
        生成需要执行【场景】数据
        :param kwargs:
        :return:
        """
        execute_type = kwargs.get('execute_dict_key', '')
        query = kwargs.get('query')
        model = model_dict.get(execute_type).get('scenario')
        query_pc = model.query.filter_by(**query, is_deleted=0).all()

        if not query_pc:
            return []

        scenario_id_list = [obj.scenario_id for obj in query_pc]
        query_scenario_list = TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()
        if query_scenario_list:
            scenario_obj_list = [obj.to_json() for obj in query_scenario_list]
        else:
            scenario_obj_list = []
        scenario_list = QueryExecuteData.query_scenario_assemble(scenario_obj_list)
        return scenario_list

    @staticmethod
    def gen_execute_name(**kwargs):
        """
        :param kwargs:
        :return:
        """

        execute_type = kwargs.get('execute_dict_key', '')
        model_id = kwargs.get('model_id')

        model = key_dict.get(execute_type).get('class')
        name = key_dict.get(execute_type).get('name')
        title = key_dict.get(execute_type).get('title')
        query_result = model.query.get(model_id)

        if query_result:
            execute_name = getattr(query_result, name)
            return title, execute_name
        else:
            return False, f'{title}id:{model_id}不存在或可执行用例为空'

    @staticmethod
    def execute_all(**kwargs):
        """
        执行全部用例以及场景
        {
            "execute_dict_key": "project", -> 用于model_dict取值
            "query": {"project_id": "30"}, -> 用于中间表查询取值
            "model_id": 30                 -> 用于对象直接查询
        }
        :param kwargs:
        :return:
        """

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        case_list = QueryExecuteData.gen_execute_case_list(**kwargs)
        scenario_list = QueryExecuteData.gen_execute_scenario_list(**kwargs)
        if not case_list and not scenario_list:
            return False, '用例与场景为空'

        data = {
            "execute_name": f"执行{title}[{execute_name}]所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }
        return True, data

    @staticmethod
    def execute_case(**kwargs):
        """
        执行全部用例
        {
            "execute_dict_key": "project", -> 用于model_dict取值
            "query": {"project_id": "30"}, -> 用于中间表查询取值
            "model_id": 30                 -> 用于对象直接查询
        }
        :param kwargs:
        :return:
        """

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        case_list = QueryExecuteData.gen_execute_case_list(**kwargs)
        if not case_list:
            return False, '用例为空'

        data = {
            "execute_name": f"执行{title}[{execute_name}]所有用例",
            "send_test_case_list": case_list
        }
        return True, data

    @staticmethod
    def execute_scenario(**kwargs):
        """
        执行全部场景
        {
            "execute_dict_key": "project", -> 用于model_dict取值
            "query": {"project_id": "30"}, -> 用于中间表查询取值
            "model_id": 30                 -> 用于对象直接查询
        }
        :param kwargs:
        :return:
        """

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        scenario_list = QueryExecuteData.gen_execute_scenario_list(**kwargs)
        if not scenario_list:
            return False, '场景为空'

        data = {
            "execute_name": f"执行{title}[{execute_name}]所有场景",
            "send_test_case_list": scenario_list
        }
        return True, data

    @staticmethod
    def execute_case_only(**kwargs):
        """
        查询单个用例组装
        :param kwargs: model_id 即 case_id
        :return:
        """

        case_id = kwargs.get('model_id')
        query_case = TestCase.query.get(case_id)
        if not query_case:
            return False, f'用例id:{case_id}不存在'

        case_info = query_case.to_json()

        bind_info = MapToJsonObj.gen_bind(case_id)

        case_info['is_public'] = bool(case_info.get('is_public'))
        case_info['is_shared'] = bool(case_info.get('is_shared'))
        result = {
            "case_info": case_info,
            "bind_info": bind_info
        }

        # query_case.add_total_execution()

        if not bool(case_info.get('is_shared')):
            return False, '执行失败,该用例是私有的,仅创建者执行!'

        execute_name = case_info.get('case_name')

        data = {
            "execute_name": f"执行用例:[{execute_name}]",
            "send_test_case_list": [result]
        }
        return True, data

    @staticmethod
    def execute_scenario_only(**kwargs):
        """
        查询单个场景组装
        :param kwargs: model_id 即 scenario_id
        :return:
        """

        scenario_id = kwargs.get('model_id')
        result = TestCaseScenario.query.get(scenario_id)
        if not result:
            return False, f'场景id:{scenario_id}不存在'

        if not bool(result.is_shared):
            return False, '执行失败,该场景是私有的,仅创建者执行!'

        scenario_obj = result.to_json()
        execute_name = scenario_obj.get('scenario_title')
        case_list = scenario_obj.get('case_list')

        if not case_list:  # 防止手动修改数据导致,在场景创建的接口中有对应的校验
            return False, f'场景id:{scenario_id}用例为空(错误数据)'

        send_test_case_list = QueryExecuteData.query_scenario_assemble([scenario_obj])
        if not send_test_case_list:
            return False, '场景为空'

        data = {
            "execute_name": f"执行场景:[{execute_name}]",
            # "send_test_case_list": send_test_case_list[-1].get("case_list") # 入参 only
            "send_test_case_list": send_test_case_list  # 入参 many
        }
        return True, data

    @staticmethod
    def module_execute_app(**kwargs):
        """
        :param kwargs:
        :return:
        """
        module_code = kwargs.get('query').get('module_code')
        query_app = TestModuleApp.query.filter_by(module_code=module_code).first()
        if query_app:
            module_id = query_app.id
            d = {
                "execute_dict_key": "module",
                "query": {"module_id": module_id},
                "model_id": module_id
            }
            case_list = QueryExecuteData.gen_execute_case_list(**d)
            scenario_list = QueryExecuteData.gen_execute_scenario_list(**d)
            return True, {
                "execute_name": f"发布应用调用【{module_code}】所有用例与场景",
                "is_execute_all": True,
                "execute_dict": {
                    "case_list": case_list,
                    "scenario_list": scenario_list
                }
            }
        else:
            return False, f'应用编号:{module_code}不存在或可执行为空'


execute_func_dict = {
    "case": QueryExecuteData.execute_case_only,
    "scenario": QueryExecuteData.execute_scenario_only,

    "project_all": QueryExecuteData.execute_all,
    "project_case": QueryExecuteData.execute_case,
    "project_scenario": QueryExecuteData.execute_scenario,

    "version_all": QueryExecuteData.execute_all,
    "version_case": QueryExecuteData.execute_case,
    "version_scenario": QueryExecuteData.execute_scenario,

    "task_all": QueryExecuteData.execute_all,
    "task_case": QueryExecuteData.execute_case,
    "task_scenario": QueryExecuteData.execute_scenario,

    "module_all": QueryExecuteData.execute_all,
    "module_case": QueryExecuteData.execute_case,
    "module_scenario": QueryExecuteData.execute_scenario,
    "module_app": QueryExecuteData.module_execute_app
}


class CaseExecApi(MethodView):
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
        data_driven = data.get('data_driven', False)
        base_url_id = data.get('base_url_id')
        use_base_url = data.get('use_base_url', False)
        is_dd_push = data.get('is_dd_push', False)
        dd_push_id = data.get('dd_push_id')
        ding_talk_url = ""
        is_send_mail = data.get('is_send_mail', False)
        is_all_mail = data.get('is_all_mail', False)
        is_safe_scan = data.get('is_safe_scan', False)
        trigger_type = data.get('trigger_type', 'user_execute')
        request_timeout = data.get('request_timeout', 20)

        if not isinstance(request_timeout, int):
            return api_result(code=400, message='请求超时填写错误')

        if is_all_mail:
            mail_list = [m.mail for m in MailConfModel.query.filter_by(is_deleted=0).all()]
        else:
            mail_list = data.get('mail_list', [])
            mail_list = [m.mail for m in MailConfModel.query.filter(
                MailConfModel.id.in_(mail_list),
                MailConfModel.is_deleted == 0
            ).all()]

        if isinstance(use_base_url, bool) and use_base_url:
            query_base_url = TestEnv.query.get(base_url_id)
            if not query_base_url:
                base_url = ''
                use_base_url = False
            else:
                base_url = query_base_url.env_url
                use_base_url = True
        else:
            base_url = ''
            use_base_url = False

        if execute_type not in execute_type_tuple:
            return api_result(code=400, message='请先选择用例场景')

        execute_func = execute_func_dict.get(execute_type)

        __key = execute_type if '_' not in execute_type else execute_type.split("_")[0]
        d = {
            "execute_dict_key": execute_type.split('_')[0],
            "query": {f"{__key}_id" if execute_type != "module_app" else "module_code": execute_id},
            "model_id": execute_id
        }
        result_bool, result_data = execute_func(**d)

        if not result_bool:
            return api_result(code=400, message=result_data)

        if is_dd_push:
            query_dd = DingDingConfModel.query.get(dd_push_id)
            if not query_dd:
                return api_result(code=400, message="钉钉群不存在或被禁用")
            ding_talk_url = query_dd.ding_talk_url

        if is_send_mail and not mail_list:
            return api_result(code=400, message="邮件不能为空，或者邮件已禁用")

        execute_name = result_data.get('execute_name', '')
        is_execute_all = result_data.get('is_execute_all', False)
        execute_dict = result_data.get('execute_dict', {})
        send_test_case_list = result_data.get('send_test_case_list', [])
        sio = StringIOLog()

        safe_scan_obj = {}
        if is_safe_scan:
            safe_scan_obj = safe_scan()
            print(safe_scan_obj)

        test_obj = {
            "execute_id": execute_id,
            "execute_name": execute_name,
            "execute_type": execute_type,
            "execute_label": execute_label,
            "execute_user_id": g.app_user.id,
            "execute_username": g.app_user.username,
            "base_url": base_url,
            "use_base_url": use_base_url,
            "data_driven": data_driven,
            "is_execute_all": is_execute_all,
            "case_list": send_test_case_list,
            "execute_dict": execute_dict,
            # "sio": sio,
            "is_dd_push": is_dd_push,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "is_send_mail": is_send_mail,
            "mail_list": mail_list,
            "trigger_type": trigger_type,
            "request_timeout": request_timeout,

            "is_safe_scan": is_safe_scan,
            "safe_scan_proxies_url": "",
            "call_safe_scan_data": {},
            "safe_scan_report_url": ""
        }
        test_obj.update(safe_scan_obj)
        save_test_logs(execute_type)

        """
        多线程/线程池模式(适用于轻量级,链路短的异步任务)
        main_test = MainTest(test_obj=test_obj)
        thread1 = threading.Thread(target=main_test.main)
        thread1.start()
        return api_result(code=200, message='操作成功,请前往日志查看执行结果')
        """

        """
        Celery异步任务
        """
        results = execute_main.delay(test_obj)
        print(results)
        # print(json.dumps(test_obj, ensure_ascii=False))
        return api_result(code=200, message='操作成功,请前往日志查看执行结果', data=[str(results)])


if __name__ == '__main__':
    from common.libs.set_app_context import set_app_context


    @set_app_context
    def main():
        """测试"""

        # p1 = QueryExecuteData.execute_all(
        #     **{"execute_dict_key": "project", "query": {"project_id": "30"}, "model_id": 30}
        # )
        # print(p1)

        # v1 = QueryExecuteData.execute_all(
        #     **{"execute_dict_key": "version", "query": {"version_id": "9"}, "model_id": 9}
        # )
        # print(v1)

        # t1 = QueryExecuteData.execute_all(
        #     **{"execute_dict_key": "task", "query": {"task_id": "47"}, "model_id": 47}
        # )
        # # 调试生成数据: **{"execute_dict_key": "task", "query": {"task_id": "30"}, "model_id": 30}
        # print(t1)

        # m1 = QueryExecuteData.execute_all(
        #     **{"execute_dict_key": "module", "query": {"module_id": "14"}, "model_id": 14}
        # )
        # print(m1)


    main()
