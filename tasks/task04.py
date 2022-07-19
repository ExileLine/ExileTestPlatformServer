# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:57 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : task03.py
# @Software: PyCharm


from tasks.celery import cel
from common.libs.db import project_db
from common.libs.parse_json_schema import ParseJsonSchema


@cel.task
def execute_pjs_main(**kwargs):
    app_name = kwargs.get('app_name')
    base_url = kwargs.get('base_url')
    query_id = kwargs.get('query_id', 0)
    query_all = kwargs.get('query_all', False)

    table_name = f"hy_{app_name}_busmodel_api_metadata"

    if query_all:
        sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE template_type='INSERT' ORDER BY id desc LIMIT 50;"""
        result_list = project_db.select(sql=sql)
        for result in result_list:
            pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result)
            pjs.main()
    else:
        sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE id='{query_id}';"""
        result = project_db.select(sql=sql, only=True)
        pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result)
        pjs.main()

    return f"执行完成:{app_name}"
