# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 15:19
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : case_cicd_api.py
# @Software: PyCharm

from flask import current_app

from all_reference import *
from app.models.test_cicd.models import TestCiCdMap
from app.models.push_reminder.models import DingDingConfModel
from .case_exec_api import QueryExecuteData
from tasks.task03 import execute_main
from app.api.case_exec_api.case_exec_api import safe_scan


def call_ui_auto(scheduling_id):
    """调用UI自动化"""

    try:
        RUN_HOST = current_app.config.get("RUN_HOST")
        url = f"http://{RUN_HOST}:8000/api/v1/monitor/job/execution"
        headers = {
            "Content-Type": "application/json"
        }
        json_data = {
            "schedulingId": scheduling_id,
        }
        send = {
            "url": url,
            "headers": headers,
            "json": json_data
        }
        resp = requests.post(**send)
        resp_json = resp.json()
        return resp_json
    except BaseException as e:
        return {"ui auto error": str(e)}


class CaseCICDMapApi(MethodView):
    """
    CICD映射Api
    """

    def post(self):
        """新增cicd映射"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_id = data.get('version_id')
        task_id = data.get('task_id')
        dd_push_id = data.get('dd_push_id')
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        branch_name = data.get('branch_name')
        mirror = data.get('mirror')
        url = data.get('url')
        is_set_url = data.get('is_set_url')
        is_active = data.get('is_active', 1)
        is_safe_scan = data.get('is_safe_scan', 0)
        scheduling_id = data.get('scheduling_id')

        query_cicd = TestCiCdMap.query.filter_by(app_name=app_name, branch_name=branch_name, is_deleted=0).first()
        if query_cicd:
            return api_result(code=400, message=f'应用名:{app_name} 已经存在分支: {branch_name}')

        if not version_id or not task_id:
            return api_result(code=400, message='版本任务不能为空')

        new_cicd = TestCiCdMap(
            project_id=project_id,
            version_id=version_id,
            task_id=task_id,
            dd_push_id=dd_push_id,
            project_name=project_name,
            app_name=app_name,
            branch_name=branch_name,
            mirror=mirror,
            url=url,
            is_set_url=is_set_url,
            is_active=is_active,
            is_safe_scan=is_safe_scan,
            scheduling_id=scheduling_id if scheduling_id else None,
            obj_json=data,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_cicd.save()
        return api_result(code=200, message='操作成功')

    def put(self):
        """编辑cicd映射"""

        data = request.get_json()
        cicd_id = data.get('id')
        version_id = data.get('version_id')
        task_id = data.get('task_id')
        dd_push_id = data.get('dd_push_id')
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        branch_name = data.get('branch_name')
        mirror = data.get('mirror')
        url = data.get('url')
        is_set_url = data.get('is_set_url')
        is_active = data.get('is_active', 1)
        is_safe_scan = data.get('is_safe_scan', 0)
        scheduling_id = data.get('scheduling_id')

        query_cicd = TestCiCdMap.query.get(cicd_id)
        if not query_cicd:
            return api_result(code=400, message='CICD配置不存在')

        if not version_id or not task_id:
            return api_result(code=400, message='版本任务不能为空')

        check_cicd = TestCiCdMap.query.filter_by(app_name=app_name, branch_name=branch_name, is_deleted=0).first()
        if check_cicd and query_cicd.id != check_cicd.id:
            return api_result(code=400, message=f'应用名:{app_name} 已经存在分支: {branch_name}')

        query_cicd.project_name = project_name
        query_cicd.app_name = app_name
        query_cicd.branch_name = branch_name
        query_cicd.mirror = mirror
        query_cicd.url = url
        query_cicd.is_set_url = is_set_url
        query_cicd.is_active = is_active
        query_cicd.is_safe_scan = is_safe_scan
        query_cicd.version_id = version_id
        query_cicd.task_id = task_id
        query_cicd.dd_push_id = dd_push_id
        query_cicd.scheduling_id = scheduling_id if scheduling_id else None
        query_cicd.obj_json = data
        query_cicd.modifier = g.app_user.username
        query_cicd.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=203, message='操作成功')

    def delete(self):
        """删除cicd映射"""

        data = request.get_json()
        cicd_id = data.get('id')
        query_cicd = TestCiCdMap.query.get(cicd_id)
        if not query_cicd:
            return api_result(code=400, message='CICD配置不存在')

        query_cicd.modifier = g.app_user.username
        query_cicd.modifier_id = g.app_user.id
        query_cicd.delete()
        return api_result(code=204, message='删除成功')


class CaseCICDMapPageApi(MethodView):
    """
    CICD映射分页模糊查询Api
    """

    def post(self):
        """CICD映射分页模糊查询"""

        data = request.get_json()
        cicd_id = data.get('id')
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        branch_name = data.get('branch_name')
        mirror = data.get('mirror')
        url = data.get('url')
        page = data.get('page')
        size = data.get('size')

        where_dict = {
            "id": cicd_id,
            "is_deleted": 0
        }

        result_data = general_query(
            model=TestCiCdMap,
            field_list=['app_name', 'branch_name'],
            query_list=[app_name, branch_name],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)


class CaseCICDApi(MethodView):
    """
    CICD Api
    """

    def get(self, cicd_id):
        """手动触发"""

        result = TestCiCdMap.query.get(cicd_id)

        if not result:
            return api_result(code=400, message=f'CICD_id:{cicd_id}不存在')

        RUN_HOST = current_app.config.get("RUN_HOST")
        RUN_PORT = current_app.config.get("RUN_PORT")
        url = f"http://{RUN_HOST}:{RUN_PORT}/api/open_cicd"
        headers = {
            "token": R.get('cicd_token')
        }
        json_data = {
            "project_name": result.project_name,
            "app_name": result.app_name,
            "branch_name": result.branch_name,
            "mirror": result.mirror,
            "url": result.url
        }
        send = {
            "url": url,
            "headers": headers,
            "json": json_data
        }
        resp = requests.post(**send)
        resp_json = resp.json()
        send['resp_json'] = resp_json
        R.set(f'test_cicd_{g.app_user.username}_{int(time.time())}', json.dumps(send))
        return api_result(code=200, message='操作成功')

    def post(self):
        """提交代码调用"""

        token = request.headers.get('token', '')
        data = request.get_json()
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        branch_name = data.get('branch_name')
        mirror = data.get('mirror')
        url = data.get('url')

        if R.get('cicd_token') != token:
            return api_result(code=400, message='鉴权失效')

        # query_cicd_map = TestCiCdMap.query.filter_by(app_name=app_name, branch_name=branch_name, is_deleted=0).first()
        query_cicd_map = TestCiCdMap.query.filter_by(app_name=app_name, is_deleted=0).first()
        if not query_cicd_map:
            return api_result(code=400, message=f'应用: {app_name} 不存在')

        if not query_cicd_map.is_active:
            return api_result(code=200, message=f'调用成功，应用: {app_name} CICD配置未开启')

        dd_push_id = query_cicd_map.dd_push_id
        query_dd = DingDingConfModel.query.get(dd_push_id)
        if not query_dd:
            return api_result(code=400, message=f'钉钉群id: {dd_push_id} 不存在')
        ding_talk_url = query_dd.ding_talk_url

        if query_cicd_map.is_set_url:
            use_base_url = True
            base_url = query_cicd_map.url
        else:
            use_base_url = False
            base_url = ""

        task_id = query_cicd_map.task_id
        result_bool, result_data = QueryExecuteData.execute_all(
            **{"execute_dict_key": "task", "query": {"task_id": task_id}, "model_id": task_id}
        )
        # print(result_bool)
        # print(result_data)

        safe_scan_obj = {}
        is_safe_scan = query_cicd_map.is_safe_scan
        if is_safe_scan:
            safe_scan_obj = safe_scan()
            print(safe_scan_obj)

        test_obj = {
            "execute_id": task_id,
            "execute_name": f'CICD-{result_data.get("execute_name")}',
            "execute_type": "task_all",
            "execute_label": "all",
            "execute_user_id": 9999999999,
            "execute_username": "CICD",
            "use_base_url": use_base_url,
            "base_url": base_url,
            "is_execute_all": result_data.get('is_execute_all'),
            # "case_list": send_test_case_list,
            "execute_dict": result_data.get('execute_dict'),
            "is_dd_push": True,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "trigger_type": "CICD_execute",
            "request_timeout": 20,

            "is_safe_scan": is_safe_scan,
            "safe_scan_proxies_url": "",
            "call_safe_scan_data": {},
            "safe_scan_report_url": ""
        }

        test_obj.update(safe_scan_obj)
        api_auto_results = execute_main.delay(test_obj)
        print(api_auto_results)

        if not query_cicd_map.scheduling_id:
            ui_auto_result = {"message": "scheduling_id 为空"}
        else:
            ui_auto_result = call_ui_auto(scheduling_id=query_cicd_map.scheduling_id)

        d = {
            "api_auto": {"celery_id": str(api_auto_results)},
            "ui_auto": ui_auto_result,
        }
        return api_result(code=200, message='操作成功', data=d)
