# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 15:22
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_pc_conf_api.py
# @Software: PyCharm

from all_reference import *
from app.api.project_api.project_api import qp
from app.models.ui_pc_conf.models import UiPcConf


class UiPcConfApi(MethodView):
    """
    Ui服务端ip配置
    GET: UiPc配置详情
    POST: UiPc配置新增
    PUT: UiPc配置编辑
    DELETE: UiPc配置删除
    """

    def get(self, pc_conf_id):
        """UiPc配置详情"""

        query_ui_pc_conf = UiPcConf.query.get(pc_conf_id)
        if not query_ui_pc_conf:
            return api_result(code=NO_DATA, message=f"UI远端配置: {pc_conf_id} 不存在")

        ui_pc_conf = query_ui_pc_conf.to_json()
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=ui_pc_conf)

    def post(self):
        """UiPc配置新增"""

        data = request.get_json()
        project_id = data.get('project_id')
        ui_pc_name = data.get('ui_pc_name')
        ui_pc_ip = data.get('ui_pc_ip')
        remark = data.get('remark')

        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        query_ui_pc_conf = UiPcConf.query.filter_by(project_id=project_id, ui_pc_ip=ui_pc_ip, is_deleted=0).first()
        if query_ui_pc_conf:
            return api_result(code=UNIQUE_ERROR, message=f'UI远端配置ip: {ui_pc_ip} 已经存在')

        new_ui_pc_conf = UiPcConf(
            project_id=project_id,
            ui_pc_name=ui_pc_name,
            ui_pc_ip=ui_pc_ip,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_ui_pc_conf.save()
        return api_result(code=POST_SUCCESS, message=POST_MESSAGE)

    def put(self):
        """UiPc配置编辑"""

        data = request.get_json()
        project_id = data.get('project_id')
        ui_pc_id = data.get('id')
        ui_pc_name = data.get('ui_pc_name')
        ui_pc_ip = data.get('ui_pc_ip')
        remark = data.get('remark')

        if not qp(project_id):
            return api_result(code=NO_DATA, message=f"项目id: {project_id} 不存在")

        query_ui_pc_conf = UiPcConf.query.get(ui_pc_id)
        if not query_ui_pc_conf:
            return api_result(code=NO_DATA, message='UI远端配置不存在')

        if query_ui_pc_conf.ui_pc_ip != ui_pc_ip:
            if UiPcConf.query.filter_by(project_id=project_id, ui_pc_ip=ui_pc_ip, is_deleted=0).all():
                return api_result(code=UNIQUE_ERROR, message=f'UI远端配置ip: {ui_pc_ip} 已经存在')

        query_ui_pc_conf.ui_pc_name = ui_pc_name
        query_ui_pc_conf.ui_pc_ip = ui_pc_ip
        query_ui_pc_conf.remark = remark
        query_ui_pc_conf.modifier = g.app_user.username
        query_ui_pc_conf.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """UiPc配置删除"""

        data = request.get_json()
        pc_conf_id = data.get('id')
        query_ui_pc_conf = UiPcConf.query.get(pc_conf_id)
        if not query_ui_pc_conf:
            return api_result(code=NO_DATA, message=f"UI远端配置: {pc_conf_id} 不存在")

        query_ui_pc_conf.modifier_id = g.app_user.id
        query_ui_pc_conf.modifier = g.app_user.username
        query_ui_pc_conf.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class UiPcConfPageApi(MethodView):
    """
    POST: Ui服务端ip配置分页模糊查询
    """

    def post(self):
        """Ui服务端ip配置分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        ui_pc_id = data.get('id')
        ui_pc_name = data.get('ui_pc_name')
        ui_pc_ip = data.get('ui_pc_ip')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        where_dict = {
            "project_id": project_id,
            "id": ui_pc_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id,
        }

        result_data = general_query(
            model=UiPcConf,
            field_list=['ui_pc_name', 'ui_pc_ip'],
            query_list=[ui_pc_name, ui_pc_ip],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
