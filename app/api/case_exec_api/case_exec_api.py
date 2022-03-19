# -*- coding: utf-8 -*-
# @Time    : 2021/8/30 9:15 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_exec_api.py
# @Software: PyCharm
from concurrent.futures import ThreadPoolExecutor

from all_reference import *
from app.models.test_case.models import TestCase
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, TestVersionTask, \
    TestModuleApp
from app.models.test_env.models import TestEnv
from app.models.test_logs.models import TestLogs
from app.models.push_reminder.models import DingDingConfModel, MailConfModel
from common.libs.StringIOLog import StringIOLog


# executor = ThreadPoolExecutor(10)


def update_case_total_execution(case_id_list):
    """更新用例执行数"""

    for case in TestCase.query.filter(TestCase.id.in_(case_id_list)).all():
        case.total_execution = case.total_execution + 1
    db.session.commit()


class QueryExecuteData:
    """查询执行参数组装"""

    @staticmethod
    def gen_exec_case_list(query_case_result):
        """
        组装用例,返回执行需要的数据格式
        :param query_case_result: 查询用例结果集
        :return:
        """

        case_list = []
        for mid in query_case_result:
            case_id = mid.case_id
            result = query_case_assemble(case_id=case_id)
            case_list.append(result)

        return case_list

    @staticmethod
    def gen_exec_scenario_list(query_scenario_result):
        """
        组装用例场景下的用例,返回执行需要的数据格式
        :param query_scenario_result: 查询用例场景结果集
        :return:
        """
        scenario_list = []
        for scenario in query_scenario_result:
            case_list = scenario.get('case_list')
            if case_list:
                sort_case_list = sorted(case_list, key=lambda x: x.get("index"), reverse=True)
                case_id_list = [obj.get('case_id') for obj in sort_case_list]

                update_case_total_execution(case_id_list)

                scenario_obj = {
                    "scenario_id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": list(map(query_case_assemble, case_id_list))
                }

                scenario_list.append(scenario_obj)

        return scenario_list

    @staticmethod
    def query_only_case(case_id):
        """
        查询单个用例组装
        :param case_id: 用例id
        :return:
        """

        result = query_case_assemble(case_id=case_id)
        if not result:
            return False, f'用例id:{case_id}不存在'

        if not bool(result.get('case_info').get('is_shared')):
            return False, '执行失败,该用例是私有的,仅创建者执行!'

        execute_name = result.get('case_info').get('case_name')
        TestCase.query.get(case_id).add_total_execution()
        case_list = [result]

        return True, {
            "execute_name": execute_name,
            "send_test_case_list": case_list
        }

    @staticmethod
    def query_only_scenario(scenario_id):
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

        sort_case_list = sorted(case_list, key=lambda x: x.get("index"), reverse=True)
        update_case_id = []
        send_test_case_list = []

        for case in sort_case_list:
            case_id = case.get('case_id')
            result = query_case_assemble(case_id=case_id)
            if result:
                update_case_id.append(case_id)
                send_test_case_list.append(result)

        return True, {
            "execute_name": execute_name,
            "send_test_case_list": send_test_case_list
        }

    @staticmethod
    def query_project_all(project_id):
        """
        查询项目下所有可执行的用例、场景并组装
        :param project_id:项目id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(project_id=project_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()
        case_id_list = [obj[0] for obj in query_mid_all]

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
                    AND B.project_id = {project_id})
                AND A.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_mid_all and not query_scenario:
            return False, f'项目id:{project_id}不存在或可执行为空'

        case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)
        scenario_list = QueryExecuteData.gen_exec_scenario_list(query_scenario)
        project_name = TestProject.query.get(project_id).project_name

        return True, {
            "execute_name": f"执行项目【{project_name}】所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }

    @staticmethod
    def query_project_case(project_id):
        """
        查询项目下所有可执行的用例并组装
        :param project_id: 项目id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(project_id=project_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()

        if not query_mid_all:
            return False, f'项目id:{project_id}不存在可执行用例为空'

        project_name = TestProject.query.get(project_id).project_name

        case_id_list = [obj[0] for obj in query_mid_all]
        send_test_case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)

        return True, {
            "execute_name": f"执行项目【{project_name}】所有用例",
            "send_test_case_list": send_test_case_list
        }

    @staticmethod
    def query_project_scenario(project_id):
        """
        查询项目下所有可执行的场景并组装
        :param project_id: 项目id
        :return:
        """

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
                    AND B.project_id = {project_id})
                AND A.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_scenario:
            return False, f'项目id:{project_id}不存在可执行场景为空'

        project_name = TestProject.query.get(project_id).project_name

        return True, {
            "execute_name": f"执行项目【{project_name}】所有用例场景",
            "send_test_case_list": QueryExecuteData.gen_exec_scenario_list(query_scenario)
        }

    @staticmethod
    def query_version_all(version_id):
        """
        查询版本下所有可执行的用例、场景并组装
        :param version_id: 版本id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(version_id=version_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()  # 去重防止脏数据
        case_id_list = [obj[0] for obj in query_mid_all]

        sql = f"""
            SELECT
                B.id,
                B.scenario_title,
                B.case_list
            FROM
                exile_test_mid_version_scenario AS A
                INNER JOIN exile_test_case_scenario AS B ON A.scenario_id = B.id
            WHERE
                A.version_id = {version_id}
                AND A.is_deleted = 0
                AND B.is_deleted = 0;
            """

        query_scenario = project_db.select(sql)

        if not query_mid_all and not query_scenario:
            return False, f'版本迭代id:{version_id}不存在或可执行为空'

        case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)
        scenario_list = QueryExecuteData.gen_exec_scenario_list(query_scenario)
        version_name = TestProjectVersion.query.get(version_id).version_name

        return True, {
            "execute_name": f"版本迭代【{version_name}】所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }

    @staticmethod
    def query_version_case(version_id):
        """
        查询版本下所有可执行的用例并组装
        :param version_id: 版本id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(version_id=version_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()  # 去重防止脏数据

        if not query_mid_all:
            return False, f'版本迭代id:{version_id}不存在或可执行用例为空'

        version_name = TestProjectVersion.query.get(version_id).version_name

        case_id_list = [obj[0] for obj in query_mid_all]
        send_test_case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)

        return True, {
            "execute_name": f"执行版本迭代【{version_name}】所有用例",
            "send_test_case_list": send_test_case_list
        }

    @staticmethod
    def query_version_scenario(version_id):
        """
        查询版本下所有可执行的场景并组装
        :param version_id: 版本id
        :return:
        """

        sql = f"""
            SELECT
                B.id,
                B.scenario_title,
                B.case_list
            FROM
                exile_test_mid_version_scenario AS A
                INNER JOIN exile_test_case_scenario AS B ON A.scenario_id = B.id
            WHERE
                A.version_id = {version_id}
                AND A.is_deleted = 0
                AND B.is_deleted = 0;
            """

        query_scenario = project_db.select(sql)

        if not query_scenario:
            return False, f'版本迭代id:{version_id}不存在或可执行场景为空'

        version_name = TestProjectVersion.query.get(version_id).version_name

        return True, {
            "execute_name": f"执行版本迭代【{version_name}】所有用例场景",
            "send_test_case_list": QueryExecuteData.gen_exec_scenario_list(query_scenario)
        }

    @staticmethod
    def query_task_all(task_id):
        """
        查询任务下所有可执行的用例、场景并组装
        :param task_id: 任务id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(task_id=task_id, is_deleted=0).all()
        case_id_list = [obj.case_id for obj in query_mid_all]

        sql = f"""
        SELECT
            B.id,
            B.scenario_title,
            B.case_list
        FROM
            exile_test_mid_version_scenario AS A
            INNER JOIN exile_test_case_scenario AS B ON A.scenario_id = B.id
        WHERE
            task_id = {task_id}
            AND A.is_deleted = 0
            AND B.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_mid_all and not query_scenario:
            return False, f'任务id:{task_id}不存在或可执行为空'

        case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)
        scenario_list = QueryExecuteData.gen_exec_scenario_list(query_scenario)
        task_name = TestVersionTask.query.get(task_id).task_name

        return True, {
            "execute_name": f"执行任务【{task_name}】所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }

    @staticmethod
    def query_task_case(task_id):
        """
        查询任务下所有可执行的用例并组装
        :param task_id: 任务id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(task_id=task_id, is_deleted=0).all()

        if not query_mid_all:
            return False, f'任务id:{task_id}不存在或可执行用例为空'

        task_name = TestVersionTask.query.get(task_id).task_name

        case_id_list = [obj.case_id for obj in query_mid_all]
        send_test_case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)

        return True, {
            "execute_name": f"执行任务【{task_name}】所有用例",
            "send_test_case_list": send_test_case_list
        }

    @staticmethod
    def query_task_scenario(task_id):
        """
        查询任务下所有可执行的场景并组装
        :param task_id: 任务id
        :return:
        """

        sql = f"""
        SELECT
            B.id,
            B.scenario_title,
            B.case_list
        FROM
            exile_test_mid_version_scenario AS A
            INNER JOIN exile_test_case_scenario AS B ON A.scenario_id = B.id
        WHERE
            task_id = {task_id}
            AND A.is_deleted = 0
            AND B.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_scenario:
            return False, f'任务id:{task_id}不存在或可执行场景为空'

        task_name = TestVersionTask.query.get(task_id).task_name

        return True, {
            "execute_name": f"执行任务【{task_name}】所有用例场景",
            "send_test_case_list": QueryExecuteData.gen_exec_scenario_list(query_scenario)
        }

    @staticmethod
    def query_module_app(module_code):
        """

        :param module_code: 应用编号
        :return:
        """

        query_app = TestModuleApp.query.filter_by(module_code=module_code).first()
        if query_app:
            case_list = list(map(query_case_assemble, query_app.case_list))
            query_scenario_list = TestCaseScenario.query.filter(TestCaseScenario.id.in_(query_app.scenario_list)).all()
            scenario_list = QueryExecuteData.gen_exec_scenario_list([s.to_json() for s in query_scenario_list])

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
    def query_module_all(module_id):
        """
        查询功能模块应用下所有可执行的用例、场景并组装
        :param module_id: 功能模块应用id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(module_id=module_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()
        case_id_list = [obj[0] for obj in query_mid_all]

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
                    AND B.module_id = {module_id})
                AND A.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_mid_all and not query_scenario:
            return False, f'功能模块应用id:{module_id}不存在或可执行为空'

        case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)
        scenario_list = QueryExecuteData.gen_exec_scenario_list(query_scenario)
        module_name = TestModuleApp.query.get(module_id).module_name

        return True, {
            "execute_name": f"执行模块应用【{module_name}】所有用例与场景",
            "is_execute_all": True,
            "execute_dict": {
                "case_list": case_list,
                "scenario_list": scenario_list
            }
        }

    @staticmethod
    def query_module_case(module_id):
        """
        查询功能模块应用下所有可执行的用例并组装
        :param module_id: 功能模块应用id
        :return:
        """

        query_mid_all = MidProjectVersionAndCase.query.filter_by(module_id=module_id, is_deleted=0).with_entities(
            MidProjectVersionAndCase.case_id).distinct().all()

        if not query_mid_all:
            return False, f'功能模块应用id:{module_id}不存在或可执行用例为空'

        module_name = TestModuleApp.query.get(module_id).module_name
        case_id_list = [obj[0] for obj in query_mid_all]
        send_test_case_list = list(map(query_case_assemble, case_id_list))
        update_case_total_execution(case_id_list)

        return True, {
            "execute_name": f"执行模块应用【{module_name}】所有用例",
            "send_test_case_list": send_test_case_list
        }

    @staticmethod
    def query_module_scenario(module_id):
        """
        查询功能模块应用下所有可执行的场景并组装
        :param module_id: 功能模块应用id
        :return:
        """

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
                    AND B.module_id = {module_id})
                AND A.is_deleted = 0;
        """

        query_scenario = project_db.select(sql)

        if not query_scenario:
            return False, f'功能模块应用id:{module_id}不存在'

        module_name = TestModuleApp.query.get(module_id).module_name

        return True, {
            "execute_name": f"执行模块应用【{module_name}】所有用例场景",
            "send_test_case_list": QueryExecuteData.gen_exec_scenario_list(query_scenario)
        }


execute_func_dict = {
    "case": QueryExecuteData.query_only_case,
    "scenario": QueryExecuteData.query_only_scenario,
    "project_all": QueryExecuteData.query_project_all,
    "project_case": QueryExecuteData.query_project_case,
    "project_scenario": QueryExecuteData.query_project_scenario,
    "version_all": QueryExecuteData.query_version_all,
    "version_case": QueryExecuteData.query_version_case,
    "version_scenario": QueryExecuteData.query_version_scenario,
    "task_all": QueryExecuteData.query_task_all,
    "task_case": QueryExecuteData.query_task_case,
    "task_scenario": QueryExecuteData.query_task_scenario,
    "module_app": QueryExecuteData.query_module_app,
    "module_all": QueryExecuteData.query_module_all,
    "module_case": QueryExecuteData.query_module_case,
    "module_scenario": QueryExecuteData.query_module_scenario
}


class CaseReqTestApi(MethodView):
    """
    test send
    """

    def post(self):
        data = request.get_json()
        method = data.get('method')
        base_url = data.get('base_url')
        url = data.get('url')
        headers = data.get('headers', {})
        req_type = data.get('req_type')
        body = data.get('body', {})

        send = {
            "url": base_url + url if base_url else url,
            "headers": headers,
            req_type: body
        }

        if req_type not in ["params", "data", "json"]:
            return api_result(code=400, message='req_type 应该为:{}'.format(["params", "data", "json"]))

        try:
            if hasattr(requests, method):
                response = getattr(requests, method)(**send, verify=False)
                data = {
                    "response": response.json(),
                    "response_headers": dict(response.headers)
                }
                return api_result(code=200, message='操作成功', data=data)
            else:
                return api_result(code=400, message='请求方式:{}不存在'.format(method))
        except BaseException as e:
            return api_result(code=400, message='请求方式失败:{}'.format(str(e)))


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
        result = execute_func(execute_id)
        result_bool = result[0]
        result_data = result[1]
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
        thread = threading.Thread(target=main_test.main)
        thread.start()

        tl = TestLogs(
            log_type=execute_type,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        tl.save()

        return api_result(code=200, message='操作成功,请前往日志查看执行结果', data=send_test_case_list)
