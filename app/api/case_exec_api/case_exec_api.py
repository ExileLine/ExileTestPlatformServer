# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm

from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseAssField, TestCaseDataAssBind
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, TestVersionTask, \
    TestModuleApp
from app.models.test_env.models import TestEnv
from app.models.test_logs.models import TestLogs
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from common.libs.StringIOLog import StringIOLog
from common.libs.set_app_context import set_app_context


# executor = ThreadPoolExecutor(200)


@set_app_context
def save_test_logs(execute_type):
    tl = TestLogs(
        log_type=execute_type,
        creator=g.app_user.username,
        creator_id=g.app_user.id
    )
    tl.save()


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
            "remark": ""
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
    def main(query_list):
        """main"""

        current_dict = {}

        for query in query_list:
            if query['id'] in current_dict:
                case_data_info = GenExecuteData.gen_structure(before_dict=query, first=False)
                current_dict[query['id']][-1]['bind_info'].append(case_data_info)
            else:
                current_dict[query['id']] = [GenExecuteData.gen_structure(before_dict=query, first=True)]

        # print(json.dumps(current_dict, ensure_ascii=False))

        result_list = []
        for obj in current_dict.values():
            result_list += obj

        # print(json.dumps(result_list, ensure_ascii=False))
        return result_list


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
            ORDER BY A.id;
	    """
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
                case_id_list = [obj.get('case_id') for obj in sort_case_list]
                QueryExecuteData.update_case_total_execution(case_id_list)
                query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
                case_list = GenExecuteData.main(query_case_zip_list)

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
        生成需要执行的用例数据
        PS:每次只能选择其中一个 key:val 作为查询参数
        {
            "project_id": 3
            # "version_id": 4,
            # "task_id": 30,
            # "module_id": 30,
        }
        :param kwargs:
        :return:
        """

        query_case = MidProjectVersionAndCase.query.filter_by(**kwargs, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()

        case_id_list = [obj.case_id for obj in query_case]
        if not case_id_list:
            return []

        query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
        case_list = GenExecuteData.main(query_case_zip_list)
        QueryExecuteData.update_case_total_execution(case_id_list)
        return case_list

    @staticmethod
    def gen_execute_scenario_list(**kwargs):
        """
        生成需要执行的场景数据
        PS:每次只能选择其中一个 key:val 作为查询参数
        {
            "project_id": 3
            # "version_id": 4,
            # "task_id": 30,
            # "module_id": 30,
        }
        :param kwargs:
        :return:
        """
        t = [(k, v) for k, v in kwargs.items()]
        k = t[-1][0]
        v = t[-1][1]
        sql = f"""
            SELECT
                A.id,
                A.scenario_title,
                A.case_list
            FROM
                exile_test_case_scenario A
            WHERE
                EXISTS (
                    SELECT
                        B.id, B.scenario_id, B.version_id
                    FROM
                        exile_test_mid_version_scenario B
                    WHERE
                        B.scenario_id = A.id
                        AND B.is_deleted = 0
                        AND {k}={v})
                    AND A.is_deleted = 0;
            """
        query_scenario = project_db.select(sql)
        scenario_list = QueryExecuteData.query_scenario_assemble(query_scenario if query_scenario else [])
        return scenario_list

    @staticmethod
    def gen_execute_name(**kwargs):
        """
        只能接受一个键值对
        支持键: project_id, version_id, task_id, module_id
        :param kwargs: 如:{"project_id": "1"}
        :return:
        """

        kv_to_tuple = [(k, v) for k, v in kwargs.items()]
        id_key = kv_to_tuple[-1][0]
        id_val = kv_to_tuple[-1][1]

        key_dict = {
            "project_id": {
                "class": TestProject,
                "name": "project_name",
                "title": "项目",
            },
            "version_id": {
                "class": TestProjectVersion,
                "name": "version_name",
                "title": "版本迭代",
            },
            "task_id": {
                "class": TestVersionTask,
                "name": "task_name",
                "title": "任务",
            },
            "module_id": {
                "class": TestModuleApp,
                "name": "module_name",
                "title": "模块",
            }
        }

        model = key_dict.get(id_key).get('class')
        name = key_dict.get(id_key).get('name')
        title = key_dict.get(id_key).get('title')
        query_result = model.query.get(id_val)
        if query_result:
            execute_name = getattr(query_result, name)
            return title, execute_name
        else:
            return False, f'{title}id:{id_val}不存在或可执行用例为空'

    @staticmethod
    def execute_all(**kwargs):
        """执行全部用例以及场景"""

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        case_list = QueryExecuteData.gen_execute_case_list(**kwargs)
        scenario_list = QueryExecuteData.gen_execute_scenario_list(**kwargs)
        if not case_list and not scenario_list:
            return False, '用例与场景为空'

        data = {
            "execute_name": f"执行{title}({execute_name})所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }
        return True, data

    @staticmethod
    def execute_case(**kwargs):
        """执行全部用例"""

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        case_list = QueryExecuteData.gen_execute_case_list(**kwargs)
        if not case_list:
            return False, '用例为空'

        data = {
            "execute_name": f"执行{title}({execute_name})所有用例",
            "send_test_case_list": case_list
        }
        return True, data

    @staticmethod
    def execute_scenario(**kwargs):
        """执行全部场景"""

        title, execute_name = QueryExecuteData.gen_execute_name(**kwargs)
        if not title:
            return title, execute_name

        scenario_list = QueryExecuteData.gen_execute_scenario_list(**kwargs)
        if not scenario_list:
            return False, '场景为空'

        data = {
            "execute_name": f"执行{title}({execute_name})所有场景",
            "send_test_case_list": scenario_list
        }
        return True, data

    @staticmethod
    def execute_case_only(case_id):
        """
        查询单个用例组装
        :param case_id: 用例id
        :return:
        """

        query_case = TestCase.query.get(case_id)
        if not query_case:
            return False, f'用例id:{case_id}不存在'

        case_info = query_case.to_json()

        query_case_mid = TestCaseDataAssBind.query.filter_by(case_id=case_id).all()
        bind_info = list(map(MapToJsonObj.gen_bind_info, query_case_mid))

        case_info['is_public'] = bool(case_info.get('is_public'))
        case_info['is_shared'] = bool(case_info.get('is_shared'))
        result = {
            "case_info": case_info,
            "bind_info": bind_info
        }

        query_case.add_total_execution()

        if not query_case:
            return False, f'用例id:{case_id}不存在'

        if not bool(case_info.get('is_shared')):
            return False, '执行失败,该用例是私有的,仅创建者执行!'

        execute_name = case_info.get('case_name')

        data = {
            "execute_name": f"执行用例:({execute_name})",
            "send_test_case_list": [result]
        }
        return True, data

    @staticmethod
    def execute_scenario_only(scenario_id):
        """
        查询单个场景组装
        :param scenario_id: 场景id
        :return:
        """

        result = TestCaseScenario.query.get(scenario_id)
        if not result:
            return False, f'场景id:{scenario_id}不存在'

        if not bool(result.is_shared):
            return False, '执行失败,该场景是私有的,仅创建者执行!'

        execute_name = result.to_json().get('scenario_title')
        case_list = result.to_json().get('case_list')

        if not case_list:  # 防止手动修改数据导致,在场景创建的接口中有对应的校验
            return False, f'场景id:{scenario_id}用例为空(错误数据)'

        send_test_case_list = QueryExecuteData.query_scenario_assemble([result.to_json()])
        if not send_test_case_list:
            return False, '场景为空'

        data = {
            "execute_name": f"执行场景:({execute_name})",
            "send_test_case_list": send_test_case_list[-1].get("case_list")
        }
        return True, data

    @staticmethod
    def module_execute_app(module_code):
        """

        :param module_code: 应用编号
        :return:
        """

        query_app = TestModuleApp.query.filter_by(module_code=module_code).first()
        if query_app:
            case_list = list(map(query_case_assemble, query_app.case_list))
            query_scenario_list = TestCaseScenario.query.filter(TestCaseScenario.id.in_(query_app.scenario_list)).all()
            scenario_list = QueryExecuteData.query_scenario_assemble([s.to_json() for s in query_scenario_list])

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

    @staticmethod
    def module_execute_all(module_id):
        """
        执行模块下的所有用例与场景
        :param module_id:
        :return:
        """

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return False, f"模块:{module_id}不存在"

        execute_name = query_module.module_name
        case_id_list = query_module.case_list
        scenario_id_list = query_module.scenario_list

        if not case_id_list and not scenario_id_list:
            return False, '用例与场景为空'

        query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
        case_list = GenExecuteData.main(query_case_zip_list)
        QueryExecuteData.update_case_total_execution(case_id_list)
        scenario_list = QueryExecuteData.query_scenario_assemble(
            [scenario.to_json() for scenario in
             TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()]
        )

        data = {
            "execute_name": f"执行模块({execute_name})所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }
        return True, data

    @staticmethod
    def module_execute_case(module_id):
        """
        执行模块下的所有用例
        :param module_id:
        :return:
        """

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return False, f"模块:{module_id}不存在"

        execute_name = query_module.module_name
        case_id_list = query_module.case_list
        if not case_id_list:
            return False, '用例为空'

        query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
        case_list = GenExecuteData.main(query_case_zip_list)
        QueryExecuteData.update_case_total_execution(case_id_list)

        data = {
            "execute_name": f"执行模块({execute_name})所有用例",
            "send_test_case_list": case_list
        }
        return True, data

    @staticmethod
    def module_execute_scenario(module_id):
        """
        执行模块下的所有场景
        :param module_id:
        :return:
        """

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return False, f"模块:{module_id}不存在"

        execute_name = query_module.module_name
        scenario_id_list = query_module.scenario_list
        if not scenario_id_list:
            return False, '场景为空'

        scenario_list = QueryExecuteData.query_scenario_assemble(
            [scenario.to_json() for scenario in
             TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()]
        )

        data = {
            "execute_name": f"执行模块({execute_name})所有用例",
            "send_test_case_list": scenario_list
        }
        return True, data


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

    "module_app": QueryExecuteData.module_execute_app,
    "module_all": QueryExecuteData.module_execute_all,
    "module_case": QueryExecuteData.module_execute_case,
    "module_scenario": QueryExecuteData.module_execute_scenario
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
        # mail_list = data.get('mail_list')
        mail_list = [m.mail for m in MailConfModel.query.all()]

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
            return api_result(code=400, message=f'execute_type:{execute_type}不存在')

        execute_func = execute_func_dict.get(execute_type)

        __key = execute_type if '_' not in execute_type else execute_type.split("_")[0]
        result_bool, result_data = execute_func(
            **{f"{__key}_id" if execute_type != "module_app" else "module_code": execute_id})

        if not result_bool:
            return api_result(code=400, message=result_data)

        if is_dd_push:
            query_dd = DingDingConfModel.query.get(dd_push_id)
            if not query_dd:
                return api_result(code=400, message="钉钉群不存在或被禁用")
            ding_talk_url = query_dd.ding_talk_url

        if is_send_mail and not mail_list:
            return api_result(code=400, message="邮件不能为空")

        execute_name = result_data.get('execute_name', '')
        is_execute_all = result_data.get('is_execute_all', False)
        execute_dict = result_data.get('execute_dict', {})
        send_test_case_list = result_data.get('send_test_case_list', [])
        sio = StringIOLog()

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
            "sio": sio,
            "is_dd_push": is_dd_push,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "is_send_mail": is_send_mail,
            "mail_list": mail_list
        }
        main_test = MainTest(test_obj=test_obj)

        # executor.submit(main_test.main)
        thread1 = threading.Thread(target=main_test.main)
        thread1.start()
        return api_result(code=200, message='操作成功,请前往日志查看执行结果', data=[time.time()])


if __name__ == '__main__':
    from common.libs.set_app_context import set_app_context


    @set_app_context
    def main():
        """测试"""

        # res = QueryExecuteData.execute_scenario_only(42)
        # res = QueryExecuteData.execute_all(**{"project_id": "30"})
        # res = QueryExecuteData.execute_all(**{"version_id": "6"})
        # res = QueryExecuteData.execute_all(**{"task_id": "45"})
        # res = QueryExecuteData.execute_case(**{"task_id": "45"})
        # res = QueryExecuteData.execute_scenario(**{"task_id": "45"})
        # res = QueryExecuteData.execute_all(**{"module_id": "3"})
        # print(res)


    @set_app_context
    def test_func():
        """测试"""
        print(QueryExecuteData.gen_execute_name(**{"project_id": "1"}))
        print(QueryExecuteData.gen_execute_name(**{"version_id": "6"}))
        print(QueryExecuteData.gen_execute_name(**{"task_id": "45"}))
        print(QueryExecuteData.gen_execute_name(**{"module_id": "3"}))


    # main()
    # test_func()
