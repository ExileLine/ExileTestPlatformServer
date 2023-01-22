# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 10:16 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : project_api.py
# @Software: PyCharm


from all_reference import *
from app.models.test_project.models import TestProject, TestProjectVersion


def qp(project_id):
    """查询项目"""

    query_project = TestProject.query.get(project_id)
    if not query_project:
        return False
    return True


class ProjectApi(MethodView):
    """
    项目管理 api
    GET: 项目详情
    POST: 项目新增
    PUT: 项目编辑
    DELETE: 项目删除
    """

    def get(self, project_id):
        """项目详情"""

        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        query_version_list = TestProjectVersion.query.filter_by(project_id=project_id).all()
        version_list = [version.to_json() for version in query_version_list]

        result = {
            "project_obj": query_project.to_json(),
            "version_list": version_list
        }

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result)

    def post(self):
        """项目新增"""

        data = request.get_json()
        project_name = data.get('project_name')
        remark = data.get('remark')

        if not project_name:
            return api_result(code=REQUIRED, message="项目名称不能为空")

        query_project = TestProject.query.filter_by(project_name=project_name).first()

        if query_project:
            return api_result(code=UNIQUE_ERROR, message=f"项目: {project_name} 已经存在")

        new_project = TestProject(
            project_name=project_name,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_project.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    def put(self):
        """项目编辑"""

        data = request.get_json()
        project_id = data.get('id')
        project_name = data.get('project_name')
        remark = data.get('remark')

        query_project = TestProject.query.get(project_id)
        if not query_project:
        # if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        if query_project.project_name != project_name:
            if TestProject.query.filter_by(project_name=project_name).all():
                return api_result(code=UNIQUE_ERROR, message=f'项目名称: {project_name} 已经存在')

        query_project.project_name = project_name
        query_project.remark = remark
        query_project.modifier = g.app_user.username
        query_project.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """项目删除"""

        data = request.get_json()
        project_id = data.get('id')

        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        query_project.modifier = g.app_user.username
        query_project.modifier_id = g.app_user.id
        query_project.delete()
        return api_result(code=DEL_SUCCESS, message='删除成功')


class ProjectPageApi(MethodView):
    """
    项目分页模糊查询 api
    POST: 项目分页模糊查询
    """

    def post(self):
        """项目分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        project_name = data.get('project_name')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_project  
        WHERE 
        id = "id" 
        and project_name LIKE"%B1%" 
        and is_deleted = 0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "is_deleted": is_deleted
        }

        result_data = general_query(
            model=TestProject,
            field_list=['project_name'],
            query_list=[project_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
