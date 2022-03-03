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
from app.models.test_project.models import TestProject, TestProjectVersion, MidProjectVersionAndCase, TestVersionTask
from app.models.test_env.models import TestEnv
from app.models.test_logs.models import TestLogs
from common.libs.StringIOLog import StringIOLog


# executor = ThreadPoolExecutor(10)


def update_case_total_execution(case_id_list):
    """更新用例执行数"""

    [case.add_total_execution() for case in TestCase.query.filter(TestCase.id.in_(case_id_list)).all()]


class QueryExecuteData:
    """查询执行参数组装"""

    @staticmethod
    def query_only_case(case_id):
        """
        查询单个用例组装
        :param case_id: 用例id
        :return:
        """
        result = query_case_zip(case_id=case_id)
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
            result = query_case_zip(case_id=case_id)
            if result:
                update_case_id.append(case_id)
                send_test_case_list.append(result)

        update_case_total_execution(case_id_list=update_case_id)

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
            return False, f'项目id:{project_id}不存在'

        project_name = TestProject.query.get(project_id).project_name

        case_list = []
        for mid in query_mid_all:
            case_id = mid.case_id
            query_case = TestCase.query.get(case_id)
            query_case.add_total_execution()
            result = query_case_zip(case_id=case_id)
            case_list.append(result)

        return True, {
            "execute_name": f"执行项目【{project_name}】所有用例",
            "send_test_case_list": case_list
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
            return False, f'项目id:{project_id}不存在'

        project_name = TestProject.query.get(project_id).project_name

        scenario_list = []
        for scenario in query_scenario:
            case_list = scenario.get('case_list')
            if case_list:
                sort_case_list = sorted(case_list, key=lambda x: x.get("index"), reverse=True)
                update_case_id = []
                new_case_list = []
                for case in sort_case_list:
                    case_id = case.get('case_id')
                    case_result = query_case_zip(case_id=case_id)
                    if case_result:
                        update_case_id.append(case_id)
                        new_case_list.append(case_result)

                scenario_obj = {
                    "scenario_id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": new_case_list
                }
                scenario_list.append(scenario_obj)

                update_case_total_execution(case_id_list=update_case_id)

        return True, {
            "execute_name": f"执行项目【{project_name}】所有用例",
            "send_test_case_list": scenario_list
        }

    @staticmethod
    def query_version_all(version_id):
        """
        查询版本下所有可执行的用例、场景并组装
        :param version_id: 版本id
        :return:
        """

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

        case_list = []
        for mid in query_mid_all:
            case_id = mid.case_id
            query_case = TestCase.query.get(case_id)
            query_case.add_total_execution()
            result = query_case_zip(case_id=case_id)
            case_list.append(result)

        return True, {
            "execute_name": f"执行【{version_name}】所有用例",
            "send_test_case_list": case_list
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

        scenario_list = []
        for scenario in query_scenario:
            case_list = scenario.get('case_list')
            if case_list:
                sort_case_list = sorted(case_list, key=lambda x: x.get("index"), reverse=True)
                update_case_id = []
                new_case_list = []
                for case in sort_case_list:
                    case_id = case.get('case_id')
                    case_result = query_case_zip(case_id=case_id)
                    if case_result:
                        update_case_id.append(case_id)
                        new_case_list.append(case_result)

                scenario_obj = {
                    "scenario_id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": new_case_list
                }
                scenario_list.append(scenario_obj)

                update_case_total_execution(case_id_list=update_case_id)

        return True, {
            "execute_name": f"执行【{version_name}】所有用例场景",
            "send_test_case_list": scenario_list
        }

    @staticmethod
    def query_task_all(task_id):
        """
        查询任务下所有可执行的用例、场景并组装
        :param task_id: 任务id
        :return:
        """

    @staticmethod
    def query_task_case(task_id):
        """
        查询任务下所有可执行的用例
        :param task_id: 任务id
        :return:
        """
        query_mid_all = MidProjectVersionAndCase.query.filter_by(task_id=task_id, is_deleted=0).all()

        if not query_mid_all:
            return False, f'任务id:{task_id}不存在或可执行用例为空'

        task_name = TestVersionTask.query.get(task_id).task_name

        case_list = []
        for mid in query_mid_all:
            case_id = mid.case_id
            query_case = TestCase.query.get(case_id)
            query_case.add_total_execution()
            result = query_case_zip(case_id=case_id)
            case_list.append(result)

        return True, {
            "execute_name": f"执行【{task_name}】所有用例",
            "send_test_case_list": case_list
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

        scenario_list = []
        for scenario in query_scenario:
            case_list = scenario.get('case_list')
            if case_list:
                sort_case_list = sorted(case_list, key=lambda x: x.get("index"), reverse=True)
                update_case_id = []
                new_case_list = []
                for case in sort_case_list:
                    case_id = case.get('case_id')
                    case_result = query_case_zip(case_id=case_id)
                    if case_result:
                        update_case_id.append(case_id)
                        new_case_list.append(case_result)

                scenario_obj = {
                    "scenario_id": scenario.get('id'),
                    "scenario_title": scenario.get('scenario_title'),
                    "case_list": new_case_list
                }
                scenario_list.append(scenario_obj)

                update_case_total_execution(case_id_list=update_case_id)

        return True, {
            "execute_name": f"执行【{task_name}】所有用例场景",
            "send_test_case_list": scenario_list
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
    "module_all": "",
    "module_case": "",
    "module_scenario": ""
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

        execute_name = result_data.get('execute_name', '')
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
            "case_list": send_test_case_list,
            "data_driven": data_driven,
            "sio": sio
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
