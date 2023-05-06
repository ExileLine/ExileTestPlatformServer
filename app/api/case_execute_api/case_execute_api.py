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
from app.models.test_logs.models import TestExecuteLogs
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from test.test_async_runner.test_async_runner import test_obj as debug_test_obj
from tasks.execute_case import execute_case


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
                    "data_info":{},
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
                "data_info": case_data_info,
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
                "data_info": case_data_info,
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

        query_ass = TestCaseAssertion.query.filter(
            TestCaseAssertion.assertion_type == "response",
            TestCaseAssertion.is_deleted == 0,
            TestCaseAssertion.id.in_(id_list)
        ).all()

        return [ass.to_json() for ass in query_ass]

    @staticmethod
    def gen_ass_field_ass_info(id_list):
        """

        :return:
        """
        if not id_list:
            return []

        query_ass = TestCaseAssertion.query.filter(
            TestCaseAssertion.assertion_type == "field",
            TestCaseAssertion.is_deleted == 0,
            TestCaseAssertion.id.in_(id_list)
        ).all()

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
                case['case_uuid'] = shortuuid.uuid()
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
        UPDATE exile5_test_case 
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
            C.use_var_list,
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
            exile5_test_case AS A
            INNER JOIN exile5_ass_bind AS B ON A.id = B.case_id
            INNER JOIN exile5_test_case_data AS C ON B.data_id = C.id
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
                    "scenario_uuid": shortuuid.uuid(),
                    "id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": case_list
                }

                scenario_list.append(scenario_obj)
        return scenario_list


class ExecuteQuery:
    """执行数据查询组装"""

    def __init__(self, execute_key: str = None, execute_type: str = None, project_id=None, query_id=None):
        """

        :param execute_key: case,scenario,project_all,project_case,project_scenario,version_all,task_all...
        :param execute_type: case,scenario,project,version,task,module...
        :param project_id: 项目id
        :param query_id: 执行对象的id
        """
        self.execute_key = execute_key
        self.execute_type = execute_type
        self.project_id = project_id
        self.query_id = query_id
        self.query_key = f"{self.execute_type}_id"
        self.query = {self.query_key: self.query_id}  # 拼接查询条件
        self.case_list = []
        self.scenario_list = []
        self.check_execute_result = True  # 检查执行对象结果
        self.error_message = None  # 错误信息

        # 错误信息中文标识
        self.execute_type_to_cn = {
            "case": "用例",
            "scenario": "场景",
            "project": "项目",
            "version": "迭代",
            "task": "任务",
            "module": "模块"
        }

        # 检查执行对象模型字典
        self.execute_mid_model_dict = {
            "case": MidProjectAndCase,
            "scenario": MidProjectScenario,
            "project": TestProject,
            "version": TestProjectVersion,
            "task": TestVersionTask,
            "module": TestModuleApp
        }

        # 使用 execute_key 来获取值
        self.use_func_dict = {
            "case": self.single_case,
            "scenario": self.single_scene,

            "project_all": self.execute_all,
            "project_case": self.execute_all_case,
            "project_scenario": self.execute_all_scenario,

            "version_all": self.execute_all,
            "version_case": self.execute_all_case,
            "version_scenario": self.execute_all_scenario,

            "task_all": self.execute_all,
            "task_case": self.execute_all_case,
            "task_scenario": self.execute_all_scenario,

            "module_all": self.execute_all,
            "module_case": self.execute_all_case,
            "module_scenario": self.execute_all_scenario
        }

        # 使用 execute_type 来获取值
        self.model_dict = {
            "project": {
                "class": TestProject,
                "case": MidProjectAndCase,
                "scenario": MidProjectScenario,
            },
            "version": {
                "class": TestProjectVersion,
                "case": MidVersionCase,
                "scenario": MidVersionScenario,
            },
            "task": {
                "class": TestVersionTask,
                "case": MidTaskCase,
                "scenario": MidTaskScenario,
            },
            "module": {
                "class": TestModuleApp,
                "case": MidModuleCase,
                "scenario": MidModuleScenario,
            }
        }

        # 执行方法
        self.use_func = self.use_func_dict.get(self.execute_key)

    def check_execute(self):
        """检查执行对象"""

        mid_func = self.execute_mid_model_dict.get(self.execute_type)
        print(mid_func)

        check_query = {
            "project_id": self.project_id
        }
        if self.execute_type == "project":
            query_mid = db.session.get(mid_func, self.query_id)
        elif self.execute_type == "task":
            query_mid = db.session.get(mid_func, self.query_id)
            if not query_mid:
                query_mid = None
            else:
                version_id = query_mid.version_id
                check_query["id"] = version_id
                query_version = TestProjectVersion.query.filter_by(**check_query).first()
                if not query_version:
                    query_mid = None

        elif self.execute_type in ("case", "scenario"):
            check_query[self.query_key] = self.query_id
            query_mid = mid_func.query.filter_by(**check_query).first()

        else:
            check_query["id"] = self.query_id
            query_mid = mid_func.query.filter_by(**check_query).first()

        print(check_query)
        print("query_mid", query_mid)
        if not query_mid:
            self.error_message = f'执行失败，{self.execute_type_to_cn.get(self.execute_type)}: {self.query_id} 不存在'
            self.check_execute_result = False

    def gen_execute_case_list(self):
        """
        生成需要执行【用例】数据
        :param query:
        :return:
        """

        model = self.model_dict.get(self.execute_type).get('case')
        query_all_case = model.query.filter_by(**self.query, is_deleted=0).all()
        case_id_list = [obj.case_id for obj in query_all_case]
        query_case_zip_list = QueryExecuteData.query_case_assemble(case_id_list)
        self.case_list = GenExecuteData.main(case_id_list, query_case_zip_list)
        # QueryExecuteData.update_case_total_execution(case_id_list)
        return self.case_list

    def gen_execute_scenario_list(self):
        """
        生成需要执行【场景】数据
        :param query:
        :return:
        """

        model = self.model_dict.get(self.execute_type).get('scenario')
        query_all_scenario = model.query.filter_by(**self.query, is_deleted=0).all()

        scenario_id_list = [obj.scenario_id for obj in query_all_scenario]
        query_scenario_list = TestCaseScenario.query.filter(TestCaseScenario.id.in_(scenario_id_list)).all()
        if query_scenario_list:
            scenario_obj_list = [obj.to_json() for obj in query_scenario_list]
        else:
            scenario_obj_list = []
        self.scenario_list = QueryExecuteData.query_scenario_assemble(scenario_obj_list)
        return self.scenario_list

    def single_case(self):
        """单个用例"""

        case_id = self.query_id
        query_case = TestCase.query.get(case_id)
        if not query_case:
            self.error_message = f'用例id:{case_id}不存在'
            return None

        case_info = query_case.to_json()
        bind_info = MapToJsonObj.gen_bind(case_id)
        result = {
            "case_uuid": shortuuid.uuid(),
            "case_info": case_info,
            "bind_info": bind_info
        }

        is_public = case_info.get('is_public')
        creator_id = case_info.get('creator_id')
        if not is_public and creator_id != g.app_user.id:
            self.error_message = f'执行失败,该用例是私有的,仅创建者执行!'
            return None

        self.case_list = [result]

    def single_scene(self):
        """单个场景"""

        scenario_id = self.query_id
        query_scenario = TestCaseScenario.query.get(scenario_id)
        if not query_scenario:
            self.error_message = f'场景id:{scenario_id}不存在'
            return None

        is_public = query_scenario.is_public
        creator_id = query_scenario.creator_id
        if not is_public and creator_id != g.app_user.id:
            self.error_message = f'执行失败,场景: {query_scenario.scenario_title} 是私有的,仅创建者执行!'
            return None

        scenario_obj = query_scenario.to_json()
        case_list = scenario_obj.get('case_list')

        if not case_list:  # 防止手动修改数据导致,在场景创建的接口中有对应的校验
            return False, f'场景id:{scenario_id}用例为空(错误数据)'

        self.scenario_list = QueryExecuteData.query_scenario_assemble([scenario_obj])
        if not self.scenario_list:
            self.error_message = '场景为空,执行失败!'
            return None

    def execute_all(self):
        """执行所有用例和场景"""

        self.gen_execute_case_list()
        self.gen_execute_scenario_list()

    def execute_all_case(self):
        """
        执行所有用例
        :return:
        """

        self.gen_execute_case_list()

    def execute_all_scenario(self):
        """
        执行所有场景
        :return:
        """

        self.gen_execute_scenario_list()


def create_execute_logs(**kwargs):
    """创建日志数据"""

    creator = kwargs.get("execute_username")
    creator_id = kwargs.get("execute_user_id")
    execute_id = kwargs.get("execute_id")
    project_id = kwargs.get("project_id")
    execute_name = kwargs.get("execute_name")
    execute_key = kwargs.get("execute_key")
    execute_type = kwargs.get("execute_type")
    trigger_type = kwargs.get("trigger_type")

    new_execute_logs = TestExecuteLogs(
        creator=creator,
        creator_id=creator_id,
        execute_id=execute_id,
        project_id=project_id,
        execute_name=execute_name,
        execute_key=execute_key,
        execute_type=execute_type,
        redis_key="等待执行完毕后回写",
        report_url="等待执行完毕后回写",
        execute_status=2,
        trigger_type=trigger_type,
        file_name="等待执行完毕后回写",
    )
    new_execute_logs.save()
    return new_execute_logs.id


class CaseExecuteApi(MethodView):
    """
    执行用例 Api
    POST: 执行用例
    """

    def get(self):
        """调试"""

        execute_logs_id = create_execute_logs(**debug_test_obj)
        debug_test_obj['execute_logs_id'] = execute_logs_id
        results = execute_case.delay(debug_test_obj)
        print(results)
        return api_result(code=SUCCESS, message='GET:操作成功,请前往日志查看执行结果', data=[str(results)])

    def post(self):
        """
        执行
        :return:
        """

        data = request.get_json()
        project_id = data.get('project_id')
        execute_id = data.get('execute_id')
        execute_key = data.get('execute_key')
        execute_name = data.get('execute_name')
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
        trigger_type = data.get('trigger_type', 'user_execute')
        request_timeout = data.get('request_timeout', 20)
        ding_talk_url = ""

        query_project = db.session.get(TestProject, project_id)
        if not query_project:
            return api_result(code=NO_DATA, message=f"项目: {project_id} 不存在")

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

            ding_talk_url = query_dd_push.ding_talk_url

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

        if execute_key not in GlobalsDict.execute_key_tuple():
            return api_result(code=TYPE_ERROR, message=f'执行标识错误:{execute_key}')

        if execute_type not in GlobalsDict.execute_type_tuple():
            return api_result(code=TYPE_ERROR, message=f'执行类型错误:{execute_type}')

        execute_query = ExecuteQuery(
            execute_key=execute_key, execute_type=execute_type, project_id=project_id, query_id=execute_id
        )

        execute_query.check_execute()
        if execute_query.check_execute_result:
            execute_query.use_func()

        if execute_query.error_message:
            return api_result(code=BUSINESS_ERROR, message=execute_query.error_message)

        case_list = execute_query.case_list
        scenario_list = execute_query.scenario_list

        test_obj = {
            "project_id": project_id,
            "execute_id": execute_id,
            "execute_name": execute_name,
            "execute_key": execute_key,
            "execute_type": execute_type,
            "execute_label": execute_label,
            "execute_user_id": g.app_user.id,
            "execute_username": g.app_user.username,
            "base_url": base_url,
            "use_base_url": use_base_url,
            "data_driven": data_driven,
            "case_list": case_list,
            "scenario_list": scenario_list,
            "use_dd_push": use_dd_push,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "use_mail": use_mail,
            "mail_list": mail_list,
            "trigger_type": trigger_type,
            "request_timeout": request_timeout,
        }
        execute_logs_id = create_execute_logs(**test_obj)
        test_obj['execute_logs_id'] = execute_logs_id
        results = execute_case.delay(test_obj)
        print(results)
        return api_result(code=SUCCESS, message='操作成功,请前往日志查看执行结果', data=[str(results)])


if __name__ == '__main__':
    @set_app_context
    def test_check_execute():
        """测试检查执行对象"""

        main = ExecuteQuery(execute_key="case", execute_type="case", project_id=30, query_id=8646)
        # main = ExecuteQuery(execute_key="scenario", execute_type="scenario", project_id=30, query_id=68)
        # main = ExecuteQuery(execute_key="project_all", execute_type="project", project_id=30, query_id=30)
        # main = ExecuteQuery(execute_key="version_all", execute_type="version", project_id=30, query_id=15)
        # main = ExecuteQuery(execute_key="module_all", execute_type="module", project_id=30, query_id=21)
        # main = ExecuteQuery(execute_key="task_all", execute_type="task", project_id=30, query_id=68)
        main.check_execute()
        print(f'错误信息:{main.error_message}')


    @set_app_context
    def test_execute_query():
        """测试查询执行结果集"""

        execute_query = ExecuteQuery(execute_key='project_all', execute_type="project", query_id=30)

        execute_query = ExecuteQuery(execute_key='case', execute_type="case", query_id=8646)
        execute_query.single_case()

        execute_query = ExecuteQuery(execute_key='scenario', execute_type="scenario", query_id=63)
        execute_query.single_scene()

        # print(execute_query.error_message)
        # print(json.dumps(execute_query.case_list, ensure_ascii=False))
        # print(json.dumps(execute_query.scenario_list, ensure_ascii=False))
        # print(len(execute_query.case_list))
        # print(len(execute_query.scenario_list))


    test_check_execute()
