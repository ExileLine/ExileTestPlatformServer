# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 15:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : case_cicd_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_cicd.models import TestCiCdMap
from app.models.push_reminder.models import DingDingConfModel
from .case_exec_api import QueryExecuteData
from tasks.task03 import execute_main


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
        mirror = data.get('mirror')
        url = data.get('url')

        query_cicd = TestCiCdMap.query.filter_by(app_name=app_name, is_deleted=0).first()
        if query_cicd:
            return api_result(code=400, message='应用名已存在')

        if not version_id or not task_id:
            return api_result(code=400, message='版本任务不能为空')

        new_cicd = TestCiCdMap(
            project_id=project_id,
            version_id=version_id,
            task_id=task_id,
            dd_push_id=dd_push_id,
            project_name=project_name,
            app_name=app_name,
            mirror=mirror,
            url=url,
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
        mirror = data.get('mirror')
        url = data.get('url')

        query_cicd = TestCiCdMap.query.get(cicd_id)
        if not query_cicd:
            return api_result(code=400, message='CICD配置不存在')

        if not version_id or not task_id:
            return api_result(code=400, message='版本任务不能为空')

        if query_cicd.app_name != app_name:
            if TestCiCdMap.query.filter_by(app_name=app_name, is_deleted=0).all():
                return api_result(code=400, message=f'应用名已存在:{app_name} 已经存在')

        query_cicd.project_name = project_name
        query_cicd.app_name = app_name
        query_cicd.mirror = mirror
        query_cicd.url = url
        query_cicd.version_id = version_id
        query_cicd.task_id = task_id
        query_cicd.dd_push_id = dd_push_id
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
            field_list=['project_name', 'app_name', 'mirror'],
            query_list=[project_name, app_name, mirror],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=200, message='操作成功', data=result_data)


class CaseCICDApi(MethodView):
    """
    CICD Api
    """

    def post(self):
        """提交代码调用"""

        token = request.headers.get('token', '')
        data = request.get_json()
        project_name = data.get('project_name')
        app_name = data.get('app_name')
        mirror = data.get('mirror')
        url = data.get('url')

        if R.get('cicd_token') != token:
            return api_result(code=400, message='鉴权失效')

        query_cicd_map = TestCiCdMap.query.filter_by(app_name=app_name, is_deleted=0).first()
        if not query_cicd_map:
            return api_result(code=400, message=f'应用: {app_name} 不存在')

        dd_push_id = query_cicd_map.dd_push_id
        query_dd = DingDingConfModel.query.get(dd_push_id)
        if not query_dd:
            return api_result(code=400, message=f'钉钉群id: {dd_push_id} 不存在')
        ding_talk_url = query_dd.ding_talk_url

        task_id = query_cicd_map.task_id
        result_bool, result_data = QueryExecuteData.execute_all(
            **{"execute_dict_key": "task", "query": {"task_id": task_id}, "model_id": task_id}
        )
        print(result_bool)
        print(result_data)

        test_obj = {
            "execute_id": task_id,
            "execute_name": f'CICD-{result_data.get("execute_name")}',
            "execute_type": "task_all",
            "execute_label": "all",
            "execute_user_id": 9999999999,
            "execute_username": "CICD",
            "use_base_url": False,
            "is_execute_all": result_data.get('is_execute_all'),
            # "case_list": send_test_case_list,
            "execute_dict": result_data.get('execute_dict'),
            "is_dd_push": True,
            "dd_push_id": dd_push_id,
            "ding_talk_url": ding_talk_url,
            "trigger_type": "CICD_execute"
        }
        results = execute_main.delay(test_obj)
        print(results)
        return api_result(code=200, message='操作成功', data=[str(results)])