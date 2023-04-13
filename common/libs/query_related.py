# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 3:59 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : query_related.py
# @Software: PyCharm

import sqlalchemy
from sqlalchemy import or_, and_, func
from flask_sqlalchemy.model import DefaultMeta

from common.libs.set_app_context import set_app_context
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind, TestCaseAssertion
from app.models.test_project.models import TestProjectVersion, MidVersionCase, MidModuleCase, TestModuleApp


def page_size(page: int = None, size: int = None, **kwargs) -> (int, int):
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
    def gen_resp_ass_list(ass_resp_id_list):
        """

        :param ass_resp_id_list:
        :return:
        """

        if ass_resp_id_list:
            query_ass_resp = TestCaseAssertion.query.filter(
                TestCaseAssertion.id.in_(ass_resp_id_list),
                TestCaseAssertion.is_deleted == 0,
            ).all()
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
            query_ass_field = TestCaseAssertion.query.filter(
                TestCaseAssertion.id.in_(ass_field_id_list),
                TestCaseAssertion.is_deleted == 0,
            ).all()
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
            data_index = data_obj.get('index')
            ass_resp_id_list = data_obj.get('ass_resp_id_list')
            ass_field_id_list = data_obj.get('ass_field_id_list')

            query_data = TestCaseData.query.get(data_id)
            if query_data:
                case_data_info = query_data.to_json()
                case_resp_ass_info = MapToJsonObj.gen_resp_ass_list(ass_resp_id_list)
                case_field_ass_info = MapToJsonObj.gen_field_ass_list(ass_field_id_list)

                bind_info = {
                    "data_info": case_data_info,
                    "case_resp_ass_info": case_resp_ass_info,
                    "case_field_ass_info": case_field_ass_info,
                }
                if data_index == 1:
                    result.insert(0, bind_info)
                else:
                    result.append(bind_info)
        return result


@set_app_context
def query_case_assemble(case_id):
    """用例组装"""

    query_case = TestCase.query.get(case_id)

    if not query_case:
        return {}

    case_info = query_case.to_json()

    version_id_list = [m.version_id for m in MidVersionCase.query.filter_by(case_id=case_id).all()]
    version_list = [m.to_json() for m in
                    TestProjectVersion.query.filter(TestProjectVersion.id.in_(version_id_list)).all()]

    module_id_list = [m.module_id for m in MidModuleCase.query.filter_by(case_id=case_id).all()]
    module_list = [m.to_json() for m in TestModuleApp.query.filter(TestModuleApp.id.in_(module_id_list)).all()]

    # 参数与响应断言、字段断言组装
    bind_info = MapToJsonObj.gen_bind(case_id)

    case_info["version_list"] = version_list
    case_info["module_list"] = module_list
    result = {
        "case_info": case_info,
        "bind_info": bind_info
    }
    return result


@set_app_context
def general_query(model: type, page: int, size: int, like_rule: str = "and_", field_list: list = [],
                  query_list: list = [], where_dict: dict = {}, in_field_list: list = None, in_value_list: list = None,
                  field_order_by: str = None) -> dict:
    """
    通用分页模糊查询
    :param model: -> DefaultMeta
    :param field_list: 模糊查询的字段列表 如: ['id','username'], 结合如下`query_list`使用
    :param query_list: 模糊查询入参列表,对应表字段的位置 如: ['id','username'] 对应 [1,'yyx']
    :param where_dict: where条件, {"id":1,"username":"yyx"...} 即: select ... where id=1 and username="yyx";
    :param like_rule: like规则,目前仅支持使用其中一个 -> and_; or_;
    :param in_field_list: in语句的字段列表 如: ['id','username'], 结合如下`in_value_list`使用
    :param in_value_list: in语句的入参列表 如: ['id','username'] 即: [[1,2,3],['y1','y2','y3']] select ... where id in (1,2,3) and username in ('y1','y2','y3')";
    :param field_order_by: order_by字段名称
    :param page: 页数 -> {"page":1,"size":20}
    :param size: 条数 -> {"page":1,"size":20}
    :return:

    """

    if not isinstance(model, DefaultMeta):
        raise TypeError('类型错误 -> model 应该是 -> flask_sqlalchemy.model.DefaultMeta')

    if not isinstance(page, int) or not isinstance(size, int):
        raise TypeError('类型错误 -> page 和 size 应该是 -> int')

    if like_rule not in ['and_', 'or_']:
        raise TypeError('参数错误 -> like_rule 应该是 -> and_ 或者 or_')

    if not isinstance(field_list, list):
        raise TypeError('类型错误 -> field_list 应该是 -> list ')

    if not isinstance(query_list, list):
        raise TypeError('类型错误 -> query_list 应该是 -> list')

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
        like_rule_func(*like_list) if like_list else and_(True),  # 模糊查询
        *where_list,  # where 条件
        *in_list  # in 条件
    ).order_by(
        getattr(model, 'update_time').desc() if not field_order_by else getattr(model, field_order_by).desc()
    ).paginate(
        page=int(page),
        per_page=int(size),
        error_out=False
    )
    result_list = [res.to_json() for res in result.items]
    total = result.total
    result_data = {
        'records': result_list,
        'now_page': page,
        'total': total
    }
    return result_data


if __name__ == '__main__':
    class TestGQ:
        """测试通用分页模糊查询"""

        @staticmethod
        def test_where():
            """测试:where"""

            where_dict = {
                "id": 1,
                "is_deleted": 0
            }
            result_data = general_query(
                model=TestCase,
                where_dict=where_dict,
                page=1,
                size=10
            )
            records = result_data.get('records')
            print(records)

        @staticmethod
        def test_in():
            """测试:in"""

            result_data = general_query(
                model=TestCase,
                in_field_list=["id"],
                in_value_list=[[1, 2, 3]],
                where_dict={},
                page=1,
                size=10
            )
            records = result_data.get('records')
            for index, res in enumerate(records, 1):
                print(res)

        @staticmethod
        def test_like():
            """测试:like"""

            result_data = general_query(
                model=TestCase,
                field_list=['case_name'],
                query_list=['okc'],
                page=1,
                size=100
            )
            records = result_data.get('records')
            for index, res in enumerate(records, 1):
                print(res.get('case_name'))

        @staticmethod
        def test_all():
            """测试组合"""

            where_dict = {
                "is_deleted": 0
            }
            result_data = general_query(
                model=TestCase,
                field_list=['case_name'],
                query_list=['okc'],
                where_dict=where_dict,
                in_field_list=["id"],
                in_value_list=[[1, 2, 3, 4]],
                page=1,
                size=100
            )
            records = result_data.get('records')
            for index, res in enumerate(records, 1):
                print(res.get('id'), res.get('case_name'))


    @set_app_context
    def main_test():
        """test"""
        MapToJsonObj.gen_bind(190)


    # TestGQ.test_where()
    # TestGQ.test_in()
    # TestGQ.test_like()
    TestGQ.test_all()
