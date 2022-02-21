# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:59 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : query_related.py
# @Software: PyCharm

import sqlalchemy
from flask_sqlalchemy.model import DefaultMeta

from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind, TestCaseAssResponse, TestCaseAssField
from app.models.test_project.models import TestProjectVersion, MidProjectVersionAndCase


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

    # TODO 后面需要优化这个查询

    query_case = TestCase.query.get(case_id)

    query_mid = MidProjectVersionAndCase.query.filter_by(case_id=case_id, is_deleted=0).all()

    version_id_list = [mid.version_id for mid in query_mid]
    version_model_list = TestProjectVersion.query.filter(
        TestProjectVersion.id.in_(version_id_list),
        TestProjectVersion.is_deleted == 0).all()
    version_obj_list = [v.to_json() for v in version_model_list]

    if not query_case:
        return False

    query_binds = TestCaseDataAssBind.query.filter_by(case_id=case_id, is_deleted=0).all()

    bind_info_list = []

    case_info = query_case.to_json()
    case_info['is_public'] = bool(case_info.get('is_public'))
    case_info['is_shared'] = bool(case_info.get('is_shared'))
    case_info["version_id_list"] = version_obj_list

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
def general_query(model, is_deleted, page, size, pass_is_deleted=False, like_rule="and_", field_list=[],
                  query_list=[], in_field_list=None, in_value_list=None):
    """
    通用分页模糊查询
    :param model: -> DefaultMeta
    :param field_list: -> list -> 模糊查询的字段列表 如: ['id','username']
    :param query_list: -> list -> 模糊查询入参列表,对应表字段的位置 如: ['id','username'] 对应 [1,'yyx']
    :param is_deleted: -> int  -> 是否逻辑删除
    :param pass_is_deleted: -> bool -> 如果为 True 则省略 is_deleted
    :param like_rule: -> str -> and;or; -> like规则目前仅支持使用其中一个
    :param in_field_list: -> list -> in的字段列表 如: ['id','username']
    :param in_value_list: -> list -> in的入参列表 如: ['id','username'] 对应 [[1,2,3],['y1','y2','y3']] => model.id.in_([1, 2, 3])
    :param page: {"page":1,"size":20}
    :param size: {"page":1,"size":20}
    :return:

    """

    if like_rule not in ['and_', 'or_']:
        raise TypeError('参数错误 -> like_rule 应该是 -> and_ 或者 or_')

    if not isinstance(model, DefaultMeta):
        raise TypeError('类型错误 -> model 应该是 -> flask_sqlalchemy.model.DefaultMeta')

    if not isinstance(field_list, list):
        raise TypeError('类型错误 -> field_list 应该是 -> list ')

    if not isinstance(query_list, list):
        raise TypeError('类型错误 -> query_list 应该是 -> list')

    if not isinstance(page, int) or not isinstance(size, int):
        raise TypeError('类型错误 -> page 和 size 应该是 -> int')

    if not isinstance(is_deleted, bool):
        raise TypeError('类型错误 -> is_deleted 应该是 -> bool')

    in_list = []

    if in_field_list and isinstance(in_field_list, list) and in_value_list and isinstance(in_value_list, list):
        for i in in_value_list:
            if not isinstance(i, list) or not i:
                raise TypeError('类型错误 -> in_value_list 里面的值应该是 -> list 而且不能为空')

        for index, field in enumerate(in_field_list):
            in_list.append(getattr(model, str(field)).in_(in_value_list[index]))

    like_rule_func = getattr(sqlalchemy, like_rule)

    like_list = []
    for index, field in enumerate(field_list):
        query_var = query_list[index]
        _like = getattr(model, str(field)).ilike("%{}%".format(query_var if query_var else ''))
        like_list.append(_like)

    where_list = []

    if not pass_is_deleted:
        where_list.append(getattr(model, 'is_deleted') != 0) if is_deleted else where_list.append(
            getattr(model, 'is_deleted') == 0)

    result = getattr(model, 'query').filter(
        like_rule_func(*like_list),
        *where_list,
        *in_list
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
        case_var_json = res.to_json()
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
