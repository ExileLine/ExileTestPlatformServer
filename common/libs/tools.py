# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 11:29
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : tools.py
# @Software: PyCharm

from sqlalchemy import or_


def general_paging_fuzzy_query(q, model, like_params, where_dict, page=1, size=20):
    """
    通用分页模糊查询(单表)
    :param q: 搜索内容
    :param model: 模型
    :param like_params: 模糊查询字段
    :param where_dict: 条件
    :param page: 页码
    :param size: 条数
    :return:
    """
    where_list = []
    if where_dict:
        for k, v in where_dict.items():
            if hasattr(model, k):
                where_list.append(getattr(model, k) == v)

    like_list = []
    for k, v in model.__dict__.items():
        if k in like_params:
            # print(k, type(k), '======', v, type(v))
            like_list.append(v.ilike("%{}%".format(q if q else '')))  # 模糊条件: v -> Model.Column.ilike
    pagination = model.query.filter(or_(*like_list), *where_list).order_by(model.create_time.desc())
    pagination = pagination.paginate(page=int(page), per_page=int(size), error_out=False)

    # result_list = []
    # for i in pagination.items:
    #     obj = i.to_json()
    #     result_list.append(obj)

    result_list = [i.to_json() for i in pagination.items]
    return result_list
