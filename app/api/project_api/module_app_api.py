# -*- coding: utf-8 -*-
# @Time    : 2022/3/2 6:23 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : module_app_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_project.models import TestModuleApp


class ModuleAppApi(MethodView):
    """
    模块应用 api
    GET: 模块应用详情
    POST: 模块应用新增
    PUT: 模块应用编辑
    DELETE: 模块应用删除
    """

    def get(self, module_id):
        """模块应用详情"""

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')

        return api_result(code=200, message='操作成功', data=query_module.to_json())

    def post(self):
        """模块应用新增"""

        data = request.get_json()
        module_name = data.get('module_name')
        module_type = data.get('module_type')
        module_code = data.get('module_code', f"默认{int(time.time())}")
        module_source = data.get('module_source')
        remark = data.get('remark')

        query_module = TestModuleApp.query.filter_by(module_code=module_code).first()

        if query_module:
            return api_result(code=400, message="应用编号已存在")

        new_module = TestModuleApp(
            module_name=module_name,
            module_type=module_type,
            module_code=module_code,
            module_source=module_source,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_module.save()
        return api_result(code=201, message='操作成功')

    def put(self):
        """模块应用编辑"""

        data = request.get_json()
        module_id = data.get('id')
        module_name = data.get('module_name')
        module_type = data.get('module_type')
        module_code = data.get('module_code', f"默认{int(time.time())}")
        module_source = data.get('module_source')
        remark = data.get('remark')

        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')

        if query_module.module_code != module_code:
            query_module_code = TestModuleApp.query.filter_by(module_code=module_code).all()
            if query_module_code:
                return api_result(code=400, message="应用编号已存在")

        query_module.module_name = module_name
        query_module.module_type = module_type
        query_module.module_code = module_code
        query_module.module_source = module_source
        query_module.remark = remark
        query_module.modifier = g.app_user.username,
        query_module.modifier_id = g.app_user.id
        db.session.commit()
        return api_result(code=203, message='操作成功')

    def delete(self):
        """模块应用删除"""

        data = request.get_json()
        module_id = data.get('id')
        query_module = TestModuleApp.query.get(module_id)
        if not query_module:
            return api_result(code=400, message=f'功能模块或应用不存在:{module_id}')
        query_module.modifier = g.app_user.username,
        query_module.modifier_id = g.app_user.id
        query_module.delete()
        return api_result(code=204, message='操作成功')


class ModuleAppPageApi(MethodView):
    """
    模块应用分页模糊查询 api
    POST: 模块应用新增
    """

    def post(self):
        """模块应用分页模糊查询"""

        data = request.get_json()
        module_id = data.get('id')
        module_name = data.get('module_name')
        creator_id = data.get('creator_id')
        is_deleted = data.get('is_deleted', 0)
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_test_module_app  
        WHERE 
        id = "id" 
        and module_name LIKE"%%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": module_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=TestModuleApp,
            field_list=['module_name'],
            query_list=[module_name],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=200, message="操作成功", data=result_data)
