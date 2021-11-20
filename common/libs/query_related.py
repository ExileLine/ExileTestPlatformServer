# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:59 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : query_related.py
# @Software: PyCharm


from sqlalchemy import or_, and_
from flask_sqlalchemy.model import DefaultMeta

from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind, TestCaseAssResponse, TestCaseAssField


def page_size(page=None, size=None, **kwargs):
    """

    :param page: -> int
    :param size: -> int
    :param kwargs: {"page":1,"size":20}
    :return:
    """
    page = page if page and isinstance(page, int) else int(kwargs.get('page', 0))
    size = size if size and isinstance(size, int) else int(kwargs.get('size', 10))
    page = (page - 1) * size if page != 0 else 0
    return page, size


@set_app_context
def query_case_zip(case_id):
    """组装查询用例"""

    query_case = TestCase.query.get(case_id)

    if not query_case:
        return False

    query_binds = TestCaseDataAssBind.query.filter_by(case_id=case_id, is_deleted=0).all()

    bind_info_list = []

    case_info = query_case.to_json()
    case_info['is_public'] = bool(case_info.get('is_public'))
    case_info['is_shared'] = bool(case_info.get('is_shared'))
    result_data = {
        "case_info": case_info,
        "bind_info": bind_info_list
    }

    if not query_binds:
        return result_data

    for bind in query_binds:
        data_id = bind.data_id
        if not data_id:
            continue
        ass_resp_ids = [] if not bind.ass_resp_id_list else bind.ass_resp_id_list
        ass_field_ids = [] if not bind.ass_field_id_list else bind.ass_field_id_list

        query_data = TestCaseData.query.get(data_id)
        query_ass_resp = TestCaseAssResponse.query.filter(TestCaseAssResponse.id.in_(ass_resp_ids)).all()
        query_ass_field = TestCaseAssField.query.filter(TestCaseAssField.id.in_(ass_field_ids)).all()

        case_data_info = query_data.to_json()
        case_resp_ass_info = [resp.to_json() for resp in query_ass_resp] if query_ass_resp else []
        case_field_ass_info = [field.to_json() for field in query_ass_field] if query_ass_field else []

        bind_info = {
            "case_data_info": case_data_info,
            "case_resp_ass_info": case_resp_ass_info,
            "case_field_ass_info": case_field_ass_info
        }
        bind_info_list.append(bind_info)

    return result_data


@set_app_context
def general_query(model, field_list, query_list, is_deleted, page, size):
    """
    通用分页模糊查询
    :param model: -> DefaultMeta
    :param field_list: -> list
    :param query_list: -> list
    :param is_deleted: -> int
    :param page: {"page":1,"size":20}
    :param size: {"page":1,"size":20}
    :return:

    """

    if not isinstance(model, DefaultMeta):
        raise TypeError('model need to be flask_sqlalchemy.model.DefaultMeta type and cannot be empty')

    if not isinstance(field_list, list) or not field_list:
        raise TypeError('field_list need to be list type and cannot be empty')

    if not isinstance(query_list, list) or not query_list:
        raise TypeError('query_list need to be list type and cannot be empty')

    if not isinstance(page, int) or not isinstance(size, int):
        raise TypeError('page or size need to be int type and cannot be empty')

    if not isinstance(is_deleted, bool):
        raise TypeError('is_deleted need to be bool type and cannot be empty')

    like_list = []
    for index, field in enumerate(field_list):
        query_var = query_list[index]
        _like = getattr(model, str(field)).ilike("%{}%".format(query_var if query_var else ''))
        like_list.append(_like)

    where_list = []
    where_list.append(getattr(model, 'is_deleted') != 0) if is_deleted else where_list.append(
        getattr(model, 'is_deleted') == 0)

    result = getattr(model, 'query').filter(
        and_(*like_list),
        *where_list
    ).order_by(
        getattr(model, 'create_time').desc()
    ).paginate(
        page=int(page),
        per_page=int(size),
        error_out=False
    )
    result_list = []
    total = result.total
    for res in result.items:
        case_var_json = res.to_json(*['_password']) if model.__tablename__ == 'exile_auth_admin' else res.to_json()
        result_list.append(case_var_json)

    result_data = {
        'records': result_list,
        'now_page': page,
        'total': total
    }
    return result_data


if __name__ == '__main__':
    def test_query_case():
        from app.models.test_case.models import TestCase
        result_data = general_query(
            model=TestCase,
            field_list=['id', 'case_name'],
            query_list=['', ''],
            is_deleted=False,
            page=1,
            size=10
        )
        print(result_data)


    def test_query_variable():
        from app.models.test_variable.models import TestVariable

        result_data = general_query(
            model=TestVariable,
            field_list=['id', 'var_name'],
            query_list=['', ''],
            is_deleted=False,
            page=1,
            size=20
        )
        print(result_data)

    # print(query_case_zip(case_id=14))
    # test_query_case()
