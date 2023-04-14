# -*- coding: utf-8 -*-
# @Time    : 2022/2/26 1:46 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : version_api.py
# @Software: PyCharm

import random

from all_reference import *
from app.models.test_project.models import TestProject, TestProjectVersion


def gen_icon(n):
    """生成icon标识"""

    if not n:
        return random.randint(1, 4)
    return n


class ProjectVersionApi(MethodView):
    """
    版本迭代 api
    GET: 版本迭代详情
    POST: 版本迭代新增
    PUT: 版本迭代编辑
    DELETE: 版本迭代删除
    """

    def get(self, version_id):
        """版本迭代详情"""

        query_version = TestProjectVersion.query.get(version_id)

        if not query_version:
            return api_result(code=NO_DATA, message=f"迭代id: {version_id} 不存在")

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=query_version.to_json())

    def post(self):
        """版本迭代新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_name = data.get('version_name')
        version_number = data.get('version_number')
        icon = data.get('icon')
        remark = data.get('remark')

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=NO_DATA, message="项目不存在或已禁用")

        query_version = TestProjectVersion.query.filter_by(project_id=project_id, version_name=version_name).first()

        if query_version:
            return api_result(code=UNIQUE_ERROR, message=f"项目: {query_project.project_name} 已经存在 迭代: {version_name}")

        new_version = TestProjectVersion(
            version_name=version_name,
            version_number=version_number,
            project_id=project_id,
            icon=gen_icon(n=icon),
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_version.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    def put(self):
        """版本迭代编辑"""

        data = request.get_json()
        project_id = data.get('project_id')
        version_id = data.get('id')
        version_name = data.get('version_name')
        version_number = data.get('version_number')
        icon = data.get('icon')
        remark = data.get('remark')

        query_project = TestProject.query.get(project_id)

        if not query_project:
            return api_result(code=NO_DATA, message="项目不存在或已禁用")

        query_version = TestProjectVersion.query.get(version_id)

        if not query_version:
            return api_result(code=NO_DATA, message="迭代不存在或已禁用")

        if query_version.project_id != project_id:  # 入参 project_id
            query_version = TestProjectVersion.query.filter_by(project_id=project_id, version_name=version_name).first()
            if query_version.id != version_id:
                return api_result(
                    code=UNIQUE_ERROR,
                    message=f"项目: {query_project.project_name} 中已经存在版本迭代名称: {version_name}"
                )

        query_version.version_name = version_name
        query_version.version_number = version_number
        query_version.project_id = project_id
        query_version.icon = gen_icon(n=icon)
        query_version.remark = remark
        query_version.modifier = g.app_user.username
        query_version.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """版本迭代删除"""

        data = request.get_json()
        version_id = data.get('id')
        query_version = TestProjectVersion.query.get(version_id)

        if not query_version:
            return api_result(code=NO_DATA, message=f"版本迭代id: {version_id} 不存在")

        query_version.modifier = g.app_user.username
        query_version.modifier_id = g.app_user.id
        query_version.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class ProjectVersionPageApi(MethodView):
    """
    project version page api
    POST: 迭代分页模糊查询
    """

    def post(self):
        """迭代分页模糊查询"""

        data = request.get_json()
        version_id = data.get('version_id')
        project_id = data.get('project_id')
        version_name = data.get('version_name')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile5_test_project_version  
        WHERE 
        id = "id" 
        and version_name LIKE"%B1%" 
        and is_deleted = 0
        and project_id = 1
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": version_id,
            "project_id": project_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestProjectVersion,
            field_list=['version_name'],
            query_list=[version_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
