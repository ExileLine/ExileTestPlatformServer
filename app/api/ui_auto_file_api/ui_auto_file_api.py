# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 4:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ui_auto_file_api.py
# @Software: PyCharm

from all_reference import *
from config.config import get_config
from app.models.ui_auto_file.models import UiAutoFile

conf = get_config()
UPLOAD_PATH = conf.get('base', 'UPLOAD_PATH')


class UiAutoFileApi(MethodView):
    """
    UI自动化测试脚本文件api
    """

    def get(self, file_id):
        """脚本明细"""

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message='文件id:{}不存在'.format(file_id))

        return api_result(code=200, message='操作成功', data=query_file.to_json())

    def post(self):
        """脚本上传"""

        file_list = [f for f in os.listdir(UPLOAD_PATH)]
        file = request.files.get('file')
        title = request.form.get('title')
        remark = request.form.get('remark')

        file_name = file.filename

        if file_name in file_list:
            return api_result(code=400, message=f'文件名称已存在:{filename}')

        file.save(f'{UPLOAD_PATH}/{file_name}')

        new_upload = UiAutoFile(
            title=title,
            file_name=file_name,
            file_path=UPLOAD_PATH,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_upload.save()
        return api_result(code=201, message='操作成功')

    def put(self):
        """编辑脚本"""

        data = request.get_json()
        file_id = data.get('id')
        title = data.get('title')
        remark = data.get('remark')

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message='file_id:不存在')

        query_file.title = title
        query_file.remark = remark
        query_file.modifier = g.app_user.username
        query_file.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=203, message='操作成功')

    def delete(self):
        """删除脚本"""

        data = request.get_json()
        file_id = data.get('id')

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message='file_id:不存在')

        query_file.modifier = g.app_user.username
        query_file.modifier_id = g.app_user.id
        query_file.delete()

        return api_result(code=204, message='操作成功')


class UiAutoFilePageApi(MethodView):
    """
    UI自动化测试脚本文件 page api
    POST: UI自动化测试脚本文件分页模糊查询
    """

    def post(self):
        """UI自动化测试脚本文件分页模糊查询"""

        data = request.get_json()
        file_id = data.get('id')
        title = data.get('title')
        file_name = data.get('file_name')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ui_auto_file  
        WHERE 
        id = "id" 
        and title LIKE"%B1%" 
        and file_name LIKE"%B1%" 
        and is_deleted = 0
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": file_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id,
        }

        result_data = general_query(
            model=UiAutoFile,
            field_list=['title', 'file_name'],
            query_list=[title, file_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)


class UiAutoFileCallApi(MethodView):
    """
    UI自动化测试脚本文件调用执行api
    """

    def post(self):
        """调用执行"""
        return
