# -*- coding: utf-8 -*-
# @Time    : 2022/4/12 9:57 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : task03.py
# @Software: PyCharm

import json
import time

from tasks.celery import cel
from common.libs.db import project_db, R
from common.libs.parse_json_schema import ParseJsonSchema, gen_table_to_hashmap


@cel.task
def execute_pjs_main(**kwargs):
    app_name = kwargs.get('app_name')
    base_url = kwargs.get('base_url')
    query_id = kwargs.get('query_id', [])
    query_all = kwargs.get('query_all', False)
    start_time = time.time()

    """redis模式"""
    gen_result = gen_table_to_hashmap(base_url=base_url, app_name=app_name)
    if not gen_result:
        return f"应用:{app_name} -> gen_table_to_hashmap 错误"

    query_result = json.loads(R.get(app_name))  # dict
    if query_all:
        for key, result in query_result.items():
            pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result, parse_way="redis")
            pjs.main()
        pjs.gen_authorization()
    else:
        if query_id:
            print(query_id)
            for index, i in enumerate(query_id):
                print(i)
                result = query_result.get(i)
                print(result)
                if result:
                    pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result, parse_way="redis")
                    pjs.main()
            pjs.gen_authorization()

        print('query_id 为空')

    """sql模式"""
    # table_name = f"hy_{app_name}_busmodel_api_metadata"
    # if query_all:
    #     sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE template_type='INSERT' ORDER BY id desc LIMIT 50;"""
    #     result_list = project_db.select(sql=sql)
    #     for result in result_list:
    #         pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result, parse_way="sql")
    #         pjs.main()
    #     pjs.gen_authorization()
    # else:
    #     sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE id='{query_id}';"""
    #     result = project_db.select(sql=sql, only=True)
    #     pjs = ParseJsonSchema(app_name=app_name, base_url=base_url, query=result, parse_way="sql")
    #     pjs.main()
    #     pjs.gen_authorization()

    print(f"执行完成: {time.time() - start_time}")
    return f"应用:{app_name} 执行完成"
