# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 4:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ui_auto_file_api.py
# @Software: PyCharm

from flask import current_app

from all_reference import *
from app.models.ui_auto_file.models import UiAutoFile


def check_files(path, new_folder, new_files):
    for root, folder, file in os.walk(path):
        if root == path:
            print(f"root:{root}")
            print(f"folder:{folder}")
            print(f"file:{file}")
            if new_folder not in folder:
                os.mkdir(f'{root}/{new_folder}')
                return True, 'pass'
            else:
                user_dir = list(os.walk(f"{root}/{new_folder}"))[0]
                print(user_dir)
                user_files = user_dir[2]
                print(user_files)
                for index, f in enumerate(new_files):
                    if f in user_files:
                        return False, f'文件: {f} 已经存在'
                return True, 'pass'
        else:
            return False, f"路径: {root} 错误"


class UiAutoFileApi(MethodView):
    """
    UI自动化测试脚本文件api
    """

    def get(self, file_id):
        """脚本明细"""

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message=f'文件id:{file_id}不存在')

        return api_result(code=200, message='操作成功', data=query_file.to_json())

    def post(self):
        """脚本上传"""

        # file = request.files.get('file')  # 单个文件
        file_list = request.files.getlist('file')  # 多个文件
        title = request.form.get('title')
        remark = request.form.get('remark')
        upload_path = current_app.config.get("UPLOAD_PATH")

        if not file_list:
            return api_result(code=400, message='文件不能为空')

        if len(file_list) > 9:
            return api_result(code=400, message='单次文件上传不能多于9个')

        new_files = [f.filename for f in file_list]
        print(new_files)
        _bool, _message = check_files(path=upload_path, new_folder=g.app_user.username, new_files=new_files)
        print(_bool, _message)

        if not _bool:
            return api_result(code=400, message=f'{_message}')

        for file in file_list:
            file_name = file.filename
            save_path = f'{upload_path}/{g.app_user.username}/{file_name}'
            file.save(save_path)
            new_upload = UiAutoFile(
                title=title,
                file_name=file_name,
                file_path=save_path,
                remark=remark,
                creator=g.app_user.username,
                creator_id=g.app_user.id,
            )
            db.session.add(new_upload)
        db.session.commit()

        return api_result(code=201, message='操作成功')

    def put(self):
        """编辑脚本"""

        file = request.files.get('file')
        file_id = request.form.get('id')
        title = request.form.get('title')
        remark = request.form.get('remark')
        upload_path = current_app.config.get("UPLOAD_PATH")

        if not file:
            return api_result(code=400, message='文件不能为空')

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message=f'file_id: {file_id} 不存在')

        if query_file.creator_id != g.app_user.id:
            return api_result(code=400, message='只允许创建者编辑')

        if file:
            file_name = file.filename
            save_path = f'{upload_path}/{g.app_user.username}/{file_name}'
            query_file.file_name = file_name
            query_file.file_path = save_path
            try:
                os.remove(query_file.file_path)
                file.save(save_path)
            except BaseException as e:
                file.save(save_path)

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
            return api_result(code=400, message=f'file_id: {file_id} 不存在')

        if query_file.creator_id != g.app_user.id:
            return api_result(code=400, message='只允许创建者删除')

        query_file.modifier = g.app_user.username
        query_file.modifier_id = g.app_user.id
        query_file.delete()
        os.remove(query_file.file_path)

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
            "is_deleted": 0,
            "creator_id": creator_id
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


class UiAutoFileCallAioApi(MethodView):
    """
    UI自动化测试脚本文件调用执行api
    """

    def post(self):
        """调用执行"""
        return
