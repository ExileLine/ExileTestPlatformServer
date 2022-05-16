# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 4:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : ui_auto_file_api.py
# @Software: PyCharm

import os
import time
import psutil
import zipfile

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


def gen_execute_cmd(file_path, user):
    """
    生成执行脚本命令
    :param file_path: 文件路径
    :param user: 用户名
    :return:
    """
    user_cmd = f"""/usr/local/bin/node ./node_modules/.bin/cross-env MACACA_REPORTER_DIR={file_path}/{user} /usr/local/bin/node ./node_modules/.bin/macaca-mocha-parallel-tests "{user}/**/*.spec.js" --reporter macaca-reporter --reporter-options reportJSONFilename=index,processAlwaysExitWithZero=true --max-parallel 5 --bail"""
    print(user_cmd)
    return user_cmd


def zip_file(filedir):
    """
    压缩文件夹至同名zip文件
    """
    file_news = filedir + '.zip'
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(filedir):
        fpath = dirpath.replace(filedir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()


class UiAutoFileUploadApi(MethodView):
    """
    UI自动化测试脚本文件上传api
    """

    def post(self):
        """脚本上传"""

        file_list = request.files.getlist('file')  # 多个文件
        upload_path = current_app.config.get("UPLOAD_PATH")
        file_path = f'{upload_path}/{g.app_user.username}'

        if len(file_list) > 9:
            return api_result(code=400, message='单次文件上传不能多于9个')

        if not os.path.exists(file_path):
            os.mkdir(file_path)

        result_file_list = []
        for file in file_list:
            file_name = file.filename
            save_path = f'{file_path}/{file_name}'
            if os.path.exists(save_path):
                file_name = f"{file_name.split('.spec.js')[0]}_{time.strftime('%Y-%m-%d_%H_%M_%S')}.spec.js"
                file.save(f"{file_path}/{file_name}")
            else:
                file.save(save_path)
            result_file_list.append(file_name)
        return api_result(code=201, message='操作成功', data=result_file_list)


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

        upload_path = current_app.config.get("UPLOAD_PATH")
        data = request.get_json()
        project_id = data.get('project_id')
        file_name_list = data.get('file_name_list')
        title = data.get('title')
        test_type = data.get('test_type')
        remark = data.get('remark')

        if not file_name_list:
            return api_result(code=400, message='文件不能为空')

        if len(file_name_list) > 9:
            return api_result(code=400, message='单次文件上传不能多于9个')

        file_path = f'{upload_path}/{g.app_user.username}'
        new_upload = UiAutoFile(
            project_id=project_id,
            title=title,
            file_name_list=file_name_list,
            file_path=file_path,
            test_type=test_type,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
        )
        new_upload.save()

        return api_result(code=201, message='操作成功')

    def put(self):
        """编辑脚本"""

        data = request.get_json()
        file_name_list = data.get('file_name_list')
        file_id = data.get('id')
        title = data.get('title')
        test_type = data.get('test_type')
        remark = data.get('remark')

        query_file = UiAutoFile.query.get(file_id)

        if not query_file:
            return api_result(code=400, message=f'file_id: {file_id} 不存在')

        if query_file.creator_id != g.app_user.id:
            return api_result(code=400, message='只允许创建者编辑')

        if not file_name_list:
            return api_result(code=400, message='文件不能为空')

        if len(file_name_list) > 9:
            return api_result(code=400, message='单次文件上传不能多于9个')

        query_file.title = title
        query_file.file_name_list = file_name_list
        query_file.test_type = test_type
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
        # os.remove(query_file.file_path)

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
        project_id = data.get('project_id')
        title = data.get('title')
        test_type = data.get('test_type')
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ui_auto_file  
        WHERE 
        id = "id" 
        and project_id = project_id
        and title LIKE"%B1%" 
        and file_name LIKE"%B1%" 
        and is_deleted = 0
        and creator_id = 1
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": file_id,
            "project_id": project_id,
            "is_deleted": 0,
            "test_type": test_type,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=UiAutoFile,
            field_list=['title'],
            query_list=[title],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)


class UiAutoFileCallAioApi(MethodView):
    """
    UI自动化测试脚本文件调用Aio服务api
    """

    def get(self):
        """测试调用Aio服务"""

        url = current_app.config.get("AIO_SERVER")
        resp = requests.get(url=url)
        return api_result(code=200, message='操作成功', data=resp.json())

    def post(self):
        """调用Aio服务"""

        upload_path = current_app.config.get("UPLOAD_PATH")
        url = current_app.config.get("AIO_SERVER")
        user = g.app_user.username

        kv = f'user:{user}'
        user_token = R.hget(kv, 'token')
        headers = {
            "token": user_token
        }
        execute_command = gen_execute_cmd(file_path=upload_path, user=user)
        json_data = {
            "execute_user": user,
            "execute_path": upload_path,
            "execute_command": execute_command
        }
        send = {
            "url": url,
            "headers": headers,
            "json": json_data
        }
        thread = threading.Thread(target=requests.post, kwargs=send)
        thread.start()
        return api_result(code=200, message='操作成功', data=json_data)


if __name__ == '__main__':
    # filename = "/Users/yangyuexiong/Desktop/ExileTestPlatformServer/app/api/ui_auto_file_api/reports"
    # zip_file(filename)          # 压缩
    # unzip(filename + '.zip')  # 解压
    print(psutil.virtual_memory().free)
    print(psutil.virtual_memory().free / 1024 / 1024)
