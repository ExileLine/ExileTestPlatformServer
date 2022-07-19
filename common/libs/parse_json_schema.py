# -*- coding: utf-8 -*-
# @Time    : 2022/7/11 15:25
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : parse_json_schema.py
# @Software: PyCharm

import copy
import json
import random
import string

from common.libs.db import project_db, R
from common.libs.set_app_context import set_app_context
from app.models.test_project.models import TestProject, MidProjectAndCase
from app.models.test_case.models import db, TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseAssResponse, TestCaseDataAssBind
from app.models.test_variable.models import TestVariable

"""
1.创建项目
2.创建用例
3.生成参数
4.生成断言
5.绑定用例
"""

error_list = []


def gen_random_str(length=8):
    """
    生成随机字符串
    :param length:
    :return: 随机字符串
    """
    random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
    return f"随机生成{random_str}"


def gen_random_int(length=8):
    """
    生成随机数字
    :param length:
    :return: 随机数字
    """
    random_int = ''.join(random.choice(string.digits) for _ in range(length))
    return int(random_int)


def gen_random_bool():
    """
    生成随机布尔值
    :return:
    """
    return random.choice([True, False])


type_dict = {
    "string": str,
    "integer": int,
    "object": dict,
    "array": list,
    "boolean": bool
}

type_func_dict = {
    "string": gen_random_str,
    "integer": gen_random_int,
    "boolean": gen_random_bool
}

request_body_type = {
    'json': 2,
    'FormData': 1
}

object_dict = {
    "_page": {
        "from": 1,
        "size": 10
    }
}


class ParseJsonSchema:
    """解析 json_schema"""

    def __init__(self, app_name, base_url, query):
        """

        :param app_name: 应用名称
        :param base_url: ip:port
        :param query:   json_schema数据源
        """

        self.app_name = app_name
        self.base_url = base_url
        if not self.app_name:
            raise ValueError('应用名称为空')
        if not self.base_url:
            raise ValueError('ip:port 为空')

        self.table_prefix = f"hy_{app_name}"
        self.creator_id = query.get('id')
        self.new_case = {
            "case_name": query.get('business_name'),
            "request_method": query.get('request_agreement'),
            "request_base_url": self.base_url,
            "request_url": f"/hy/saas/hy/{self.app_name}/api/{query.get('request_url')}",
            "remark": query.get('business_desc'),
            "creator": "ParseJsonSchema",
            "creator_id": self.creator_id,
            "status": 9
        }
        self.resourceType = ''

        self.business_name = query.get('business_name')
        self.json_schema = query.get('json_schema')

        self.project_id = None
        self.case_id = None
        self.data_list = []
        self.data_id_list = []

        self.ass_success = [
            {
                "rule": "==",
                "assert_key": "code",
                "expect_val": "SA0000",
                "is_expression": 0,
                "python_val_exp": "",
                "expect_val_type": 2,
                "response_source": "response_body"
            }
        ]
        self.ass_fail = [
            {
                "rule": "!=",
                "assert_key": "code",
                "expect_val": "SA0000",
                "is_expression": 0,
                "python_val_exp": "",
                "expect_val_type": 2,
                "response_source": "response_body"
            }
        ]

        self.ass_resp_success_id = None
        self.ass_resp_fail_id = None

    def query_table(self, key=None, table=None, field=None):
        """

        :param key: 当前参数key
        :param table: 表名称
        :param field: 字段名称
        :return:
        """

        if not table:
            return f"表: {table} 不存在无法取值"
        if not field:
            return f"字段: {field} 不存在无法取值"

        print(f"=== key ===\n{key}")
        print(f"=== table ===\n{table}")
        print(f"=== field ===\n{field}")

        table_name = f"{self.table_prefix}_{table}"
        sql = f"""SELECT * FROM `aaaaaaa`.`{table_name}` WHERE '{field}' IS NOT NULL ;"""
        print(f"=== sql ===\n{sql}")

        query_result = project_db.select(sql=sql, only=True)
        print(f"=== query_result ===\n{query_result}")
        if not query_result:
            return f"未找到字典: {table_name} 无法取值"

        res = query_result.get(field)
        print(f"=== res ===\n{res}")
        return res

    @set_app_context
    def gen_project(self):
        """根据 app_name 生成项目"""

        query_project = TestProject.query.filter_by(project_name=self.app_name).first()
        if query_project:
            self.project_id = query_project.id
        else:
            new_project = TestProject(
                project_name=self.app_name,
                remark="自解析",
                creator="ParseJsonSchema"
            )
            new_project.save()
            self.project_id = new_project.id

    @set_app_context
    def gen_case(self):
        """生成用例"""

        query_case = TestCase.query.filter_by(creator_id=self.creator_id).first()
        if query_case:
            self.case_id = query_case.id
            if not MidProjectAndCase.query.filter_by(project_id=self.project_id, case_id=self.case_id).first():
                mid_pc = MidProjectAndCase(
                    project_id=self.project_id, case_id=self.case_id, creator="ParseJsonSchema")
                db.session.add(mid_pc)
                db.session.commit()
        else:
            new_case = TestCase(**self.new_case)
            new_case.save()
            self.case_id = new_case.id
            mid_pc = MidProjectAndCase(
                project_id=self.project_id, case_id=self.case_id, creator="ParseJsonSchema")
            db.session.add(mid_pc)
            db.session.commit()

    @set_app_context
    def gen_resp_ass(self):
        """生成resp断言"""

        assert_description1 = f"断言-{self.app_name}-success"
        assert_description2 = f"断言-{self.app_name}-fail"
        query_resp_ass_success = TestCaseAssResponse.query.filter_by(assert_description=assert_description1).first()
        query_resp_ass_fail = TestCaseAssResponse.query.filter_by(assert_description=assert_description2).first()

        if query_resp_ass_success:
            self.ass_resp_success_id = query_resp_ass_success.id
        else:
            new_ass_resp_success = TestCaseAssResponse(
                assert_description=assert_description1,
                ass_json=self.ass_success,
                creator="ParseJsonSchema",
                remark="自解析通用断言"
            )
            new_ass_resp_success.save()
            self.ass_resp_success_id = new_ass_resp_success.id

        if query_resp_ass_fail:
            self.ass_resp_fail_id = query_resp_ass_fail.id
        else:
            new_ass_resp_fail = TestCaseAssResponse(
                assert_description=assert_description2,
                ass_json=self.ass_fail,
                creator="ParseJsonSchema",
                remark="自解析通用断言"
            )
            new_ass_resp_fail.save()
            self.ass_resp_fail_id = new_ass_resp_fail.id

    def __f1(self, _type, _fieldSize, reverse=False):
        """f1"""

        func = type_func_dict.get(_type)
        if reverse:
            return func(_fieldSize - 3)

        if _fieldSize < 4:
            res = func(_fieldSize)[0:_fieldSize]
        else:
            res = func(_fieldSize - 4)
        return res

    def _gen_object_array(self):
        """1"""

    def reverse_check(self, _dateEngineFieldDataType=None, _type=None, _fieldSize=None):
        """

        :param _dateEngineFieldDataType:
        :param _type:
        :param _fieldSize:
        :return:
        """

        if not _dateEngineFieldDataType:
            return ''

        if _dateEngineFieldDataType == 'NORMAL':
            res = self.__f1(_type, _fieldSize, reverse=True)
        elif _dateEngineFieldDataType in ('DICT', 'QUOTE', 'IMG', 'FK'):
            res = ""
        else:
            raise TypeError(f"_dateEngineFieldDataType: {_dateEngineFieldDataType} {_type} {_fieldSize}")
        return res

    def _gen_res(self, _dateEngineFieldDataType=None, _type=None, key=None, val=None, _fieldSize=None, obj={},
                 required=[]):
        """

        :param _dateEngineFieldDataType:
        :param _type:
        :param key:
        :param val:
        :param _fieldSize:
        :param obj:
        :param required:
        :return:
        """

        if _type in ('object', 'array'):
            res = object_dict.get(key)
            if res:
                return res
            else:
                error_list.append((key, obj))
                return ''

        if not _dateEngineFieldDataType:
            if not _fieldSize:
                if obj.get('enum'):
                    return random.choice(obj.get('enum'))
                elif obj.get('_customName'):
                    return obj.get('_customName')
                else:
                    res = type_func_dict.get(_type)
                    if not res:
                        error_list.append((key, obj))
                        return ''
                    return res()
            return self.__f1(_type, _fieldSize)

        if _dateEngineFieldDataType == 'NORMAL':
            res = self.__f1(_type, _fieldSize)
        elif _dateEngineFieldDataType == 'DICT':
            table = val.get('_associatedReference').get('refTableCode')
            field = val.get('_associatedReference').get('refFieldCode')
            res = self.query_table(key=key, table=table, field=field)
        elif _dateEngineFieldDataType == 'QUOTE':
            table = val.get('_associatedReference').get('tableCode')
            field = val.get('_associatedReference').get('fieldCode')
            res = self.query_table(key=key, table=table, field=field)
        elif _dateEngineFieldDataType in ('IMG', 'FK', 'FILE'):
            return gen_random_str(32)
        else:
            raise TypeError(f"_dateEngineFieldDataType: {key} {val} {_type} {_fieldSize}")

        return res

    @set_app_context
    def gen_data(self):
        """生成参数"""

        if not self.json_schema.get('reqSchema'):
            print('reqSchema 为空')
            return None

        self.resourceType = self.json_schema.get('resourceType')
        reqSchema = self.json_schema.get('reqSchema')
        properties = reqSchema.get('properties')
        required = reqSchema.get('required', [])  # 必传key
        req_type = reqSchema.get('type')
        # print(json.dumps(reqSchema, ensure_ascii=False))
        print(f"=== business_name ===\n{self.business_name}")
        print(f"=== req_type ===\n{req_type}")
        print(f"=== resourceType ===\n{self.resourceType}")
        print(f"=== required ===\n{required}")

        d = {}

        current_required = {}
        for index, key in enumerate(properties.keys()):
            val = properties.get(key)
            _type = val.get('type')
            _fieldSize = val.get('_fieldSize')
            _dateEngineFieldDataType = val.get('_dateEngineFieldDataType')
            print(f'=== index:{index} ===')
            print(f'=== key:{key} ===')
            print(f"=== val ===\n{val}")
            print(f"=== _type ===\n{_type}")
            print(f"=== _fieldSize ===\n{_fieldSize}")
            print(f"=== _dateEngineFieldDataType ===\n{_dateEngineFieldDataType}")

            if key in required:
                current_required[key] = val
            res = self._gen_res(
                _dateEngineFieldDataType=_dateEngineFieldDataType,
                _type=_type,
                key=key,
                val=val,
                _fieldSize=_fieldSize,
                obj=val,
                required=required
            )

            try:
                d[key] = type_dict.get(_type)(res)
            except BaseException as e:
                d[key] = res

        print(json.dumps(d, ensure_ascii=False))
        self.data_list.append(d)

        if required:
            print('=== current_required ===')
            print(required)
            print(current_required)
            for index, key in enumerate(required):  # 边界，类型，None
                d1 = copy.deepcopy(d)
                properties = current_required.get(key)
                print(key)
                print(properties)

                _type = properties.get('type')
                _fieldSize = properties.get('_fieldSize')
                _dateEngineFieldDataType = properties.get('_dateEngineFieldDataType')

                v = self.reverse_check(
                    _dateEngineFieldDataType=_dateEngineFieldDataType,
                    _type=_type,
                    _fieldSize=_fieldSize
                )

                d1[key] = v
                self.data_list.append(d1)

                if v:
                    d2 = copy.deepcopy(d)
                    d2[key] = ""
                    self.data_list.append(d2)

    @set_app_context
    def save_data(self):
        """入库"""

        request_headers = {
            "Authorization": "Bearer hy.entrance.4.f237e323-080a-46a5-9418-f523359d5a52",
            "Content-Type": "application/json;charset=UTF-8"
        }
        for index, d in enumerate(self.data_list):
            new_data = TestCaseData(
                data_name=f"自生成:{self.business_name}_{index}",
                request_params=d,
                request_headers=request_headers,
                request_body=d,
                request_body_type=request_body_type.get(self.resourceType, 1),
                creator="ParseJsonSchema"
            )
            new_data.save()
            self.data_id_list.append(new_data.id)

        print(self.data_id_list)

    @set_app_context
    def bind(self):
        """绑定关系"""

        for index, data_id in enumerate(self.data_id_list):
            if index != 0:
                ass_resp_id_list = []
                ass_field_id_list = [self.ass_resp_fail_id]
            else:
                ass_resp_id_list = [self.ass_resp_success_id]
                ass_field_id_list = []
            case_bind = TestCaseDataAssBind(
                case_id=self.case_id,
                data_id=data_id,
                ass_resp_id_list=ass_resp_id_list,
                ass_field_id_list=ass_field_id_list,
                creator="ParseJsonSchema"
            )
            db.session.add(case_bind)
        db.session.commit()

    def main(self):
        """main"""

        self.gen_project()
        self.gen_case()
        self.gen_resp_ass()
        print(self.project_id)
        print(self.case_id)
        print(self.ass_resp_success_id)
        print(self.ass_resp_fail_id)
        self.gen_data()
        print(error_list)
        self.save_data()
        self.bind()


@set_app_context
def test_reset():
    """1"""

    db.session.query(TestCase).filter(TestCase.creator == 'ParseJsonSchema').delete(synchronize_session=False)
    db.session.query(TestCaseData).filter(TestCaseData.creator == 'ParseJsonSchema').delete(synchronize_session=False)
    db.session.commit()


def test_main(size=None):
    """批量"""

    if size:
        sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE template_type='INSERT' ORDER BY id desc LIMIT {size};"""
    else:
        sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata`;"""

    result_list = project_db.select(sql=sql)
    for result in result_list:
        pjs = ParseJsonSchema(app_name='entrance', base_url='http://192.168.14.160:7090', query=result)
        pjs.main()


def test_one():
    """单个"""

    # sql = """SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE business_name='新增[人脸下发异步结果表]表信息';"""
    sql = """SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE business_name='新增[设备点位表]表信息';"""
    # sql = """SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` WHERE business_name='新增_用户操作日志表';"""
    result = project_db.select(sql=sql, only=True)
    pjs = ParseJsonSchema(app_name='entrance', base_url='http://192.168.14.160:7090', query=result)
    pjs.main()


if __name__ == '__main__':
    """main"""

    # test_reset()
    # test_main()
    test_one()

    print(json.dumps(error_list, ensure_ascii=False))
