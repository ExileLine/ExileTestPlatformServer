# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:59 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : query_related.py
# @Software: PyCharm

import sqlalchemy
from flask_sqlalchemy.model import DefaultMeta

from common.libs.db import project_db
from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind, TestCaseAssResponse, TestCaseAssField
from app.models.test_project.models import TestProjectVersion, MidProjectVersionAndCase, MidProjectVersionAndScenario


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


class MapToJsonObj:
    """模型转Json"""

    @staticmethod
    def gen_module_id(q_type, q_value):
        """

        :param q_type:
        :param q_value:
        :return:
        """

        query_module = None
        if q_type == 'case':
            query_module = MidProjectVersionAndCase.query.filter(
                MidProjectVersionAndCase.case_id == q_value,
                MidProjectVersionAndCase.module_id != None,
                MidProjectVersionAndCase.module_id != 0,
            ).all()
        if q_type == 'scenario':
            query_module = MidProjectVersionAndScenario.query.filter(
                MidProjectVersionAndScenario.scenario_id == q_value,
                MidProjectVersionAndScenario.module_id != None,
                MidProjectVersionAndScenario.module_id != 0,
            ).all()
        if query_module:
            return query_module[-1].module_id
        else:
            return ''

    @staticmethod
    def gen_case_version_list(case_id):
        """

        :param case_id: 用例id
        :return:
        """
        sql = f"""
        SELECT DISTINCT
            A.id,
            A.version_name,
            A.version_number,
            A.project_id,
            A.creator,
            A.creator_id,
            A.modifier,
            A.creator_id,
            A.create_time,
            A.create_timestamp,
            A.update_time,
            A.create_timestamp,
            A.remark,
            A.is_deleted
        FROM
            exile_test_project_version AS A
            INNER JOIN exile_test_mid_version_case AS B ON A.id = B.version_id
        WHERE
            A.is_deleted = 0
            AND B.case_id = {case_id};
        """
        query_result = project_db.select(sql)
        return query_result

    @staticmethod
    def gen_scenario_version_list(scenario_id):
        """

        :param scenario_id:
        :return:
        """
        sql = f"""
        SELECT DISTINCT
            A.id,
            A.version_name,
            A.version_number,
            A.project_id,
            A.creator,
            A.creator_id,
            A.modifier,
            A.creator_id,
            A.create_time,
            A.create_timestamp,
            A.update_time,
            A.create_timestamp,
            A.remark,
            A.is_deleted
        FROM
            exile_test_project_version AS A
            INNER JOIN exile_test_mid_version_scenario AS B ON A.id = B.version_id
        WHERE
            A.is_deleted = 0
            AND B.scenario_id = {scenario_id};
        """
        query_result = project_db.select(sql)
        return query_result

    @staticmethod
    def gen_resp_ass_list(ass_resp_id_list):
        """

        :param ass_resp_id_list:
        :return:
        """

        if ass_resp_id_list:
            query_ass_resp = TestCaseAssResponse.query.filter(TestCaseAssResponse.id.in_(ass_resp_id_list)).all()
            ass_resp_obj_list = [ass.to_json() for ass in query_ass_resp]
            return ass_resp_obj_list
        else:
            return []

    @staticmethod
    def gen_field_ass_list(ass_field_id_list):
        """

        :param ass_field_id_list:
        :return:
        """

        if ass_field_id_list:
            query_ass_field = TestCaseAssField.query.filter(TestCaseAssField.id.in_(ass_field_id_list)).all()
            ass_field_obj_list = [ass.to_json() for ass in query_ass_field]
            return ass_field_obj_list
        else:
            return []

    @staticmethod
    def gen_bind(case_id):
        """

        :param case_id:
        :return:
        """
        query_mid = TestCaseDataAssBind.query.filter_by(case_id=case_id).all()
        query_mid_obj_list = [obj.to_json() for obj in query_mid]

        result = []
        for data_obj in query_mid_obj_list:
            data_id = data_obj.get('data_id')
            ass_resp_id_list = data_obj.get('ass_resp_id_list')
            ass_field_id_list = data_obj.get('ass_field_id_list')

            query_data = TestCaseData.query.get(data_id)
            if query_data:
                case_data_info = query_data.to_json()
                case_resp_ass_info = MapToJsonObj.gen_resp_ass_list(ass_resp_id_list)
                case_field_ass_info = MapToJsonObj.gen_field_ass_list(ass_field_id_list)

                bind_info = {
                    "case_data_info": case_data_info,
                    "case_resp_ass_info": case_resp_ass_info,
                    "case_field_ass_info": case_field_ass_info,
                }
                result.append(bind_info)
        return result


@set_app_context
def query_case_assemble(case_id):
    """用例组装"""

    query_case = TestCase.query.get(case_id)

    if not query_case:
        return {}

    case_info = query_case.to_json()

    # 版本组装
    version_obj_list = MapToJsonObj.gen_case_version_list(case_id)

    # 模块
    module_id = MapToJsonObj.gen_module_id('case', case_id)

    # 参数与响应断言、字段断言组装
    bind_info = MapToJsonObj.gen_bind(case_id)

    case_info["version_id_list"] = version_obj_list
    case_info["module_id"] = module_id
    case_info['is_public'] = bool(case_info.get('is_public'))
    case_info['is_shared'] = bool(case_info.get('is_shared'))
    result = {
        "case_info": case_info,
        "bind_info": bind_info
    }
    return result


# 待删除
@set_app_context
def query_case_zip(case_id):
    """组装查询用例"""

    # TODO 后面需要优化这个查询

    query_case = TestCase.query.get(case_id)

    if not query_case:
        return False

    query_mid = MidProjectVersionAndCase.query.filter_by(case_id=case_id, is_deleted=0).all()

    version_id_list = [mid.version_id for mid in query_mid]
    version_model_list = TestProjectVersion.query.filter(
        TestProjectVersion.id.in_(version_id_list),
        TestProjectVersion.is_deleted == 0).all()
    version_obj_list = [v.to_json() for v in version_model_list]

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
def general_query(model, page, size, like_rule="and_", field_list=[], query_list=[], where_dict={}, in_field_list=None,
                  in_value_list=None):
    """
    通用分页模糊查询
    :param model: -> DefaultMeta
    :param field_list: -> list -> 模糊查询的字段列表 如: ['id','username']
    :param query_list: -> list -> 模糊查询入参列表,对应表字段的位置 如: ['id','username'] 对应 [1,'yyx']
    :param where_dict: -> dict -> {"id":1 ...}
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

    # 忽略null或空字符串的查询
    where_list = [getattr(model, key) == val for key, val in where_dict.items() if val or isinstance(val, int)]

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

        where_dict = {
            "id": 1,
            "is_deleted": 0
        }

        result_data = general_query(
            model=TestCase,
            field_list=['case_name'],
            query_list=[''],
            where_dict=where_dict,
            page=1,
            size=10
        )
        print(result_data)


    def test_query_variable():
        from app.models.test_variable.models import TestVariable

        where_dict = {
            "id": 1,
            "is_deleted": 0
        }

        result_data = general_query(
            model=TestVariable,
            field_list=['var_name'],
            query_list=[''],
            where_dict=where_dict,
            page=1,
            size=20
        )
        print(result_data)


    # test_query_case()
    # query_case_zip(case_id=14)
    # query_case_assemble(185)

    @set_app_context
    def main_test():
        """test"""
        MapToJsonObj.gen_bind(190)
        print(MapToJsonObj.gen_module_id('case', 190))

    # main_test()
