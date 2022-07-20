# -*- coding: utf-8 -*-
# @Time    : 2022/7/11 15:25
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : parse_json_schema.py
# @Software: PyCharm

import copy
import datetime
import json
import random
import string

import requests

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
    "number": int,
    "object": dict,
    "array": list,
    "boolean": bool,
    "null": lambda x: None
}

type_func_dict = {
    "string": gen_random_str,
    "integer": gen_random_int,
    "number": gen_random_int,
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


def gen_table_to_hashmap(base_url, app_name):
    """

    :param base_url:
    :param app_name:
    :return:
    """

    url = f"{base_url}/hy/saas/hy/{app_name}/business/__system_upload__"
    json_data = {
        "businesscode": "__system_upload__",
        "steps": [
            {
                "function": {
                    "code": "TABLE_SELECT",
                    "params": {
                        "table": "busmodel_api_metadata",
                        "condition": {}
                    }
                }
            }
        ]
    }

    print('=== gen_table_to_hashmap ===')
    print(url)
    print(json_data)

    try:
        query_redis = R.get(app_name)
        if query_redis:
            # json_result = json.loads(query_redis)
            print('query_redis is true')
            return True

        resp = requests.post(url=url, json=json_data, verify=False)
        resp_json = resp.json()
        resp_code = resp_json.get("code")
        table_list = resp_json.get("result").get('data')
        d = {}
        if resp_code == "SA0000" and table_list:
            print(datetime.datetime.now())
            for table in table_list:
                d[table.get("id")] = table
            R.set(app_name, json.dumps(d, ensure_ascii=False))
            print(datetime.datetime.now())
            return True
        else:
            print(f"错误resp_code:{resp_code}")
            return False
    except BaseException as e:
        print(f"异常:{str(e)}")
        return False


class ParseJsonSchema:
    """解析 json_schema"""

    def __init__(self, app_name, base_url, query, parse_way):
        """

        :param app_name: 应用名称
        :param base_url: ip:port
        :param query:   json_schema数据源
        :param parse_way: 解析方式
        """

        self.parse_way = parse_way
        if self.parse_way not in ('sql', 'redis'):
            raise ValueError("parse_way 应该为 sql 或者 redis")
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

        if isinstance(self.json_schema, str):
            self.json_schema = json.loads(query.get('json_schema'))

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

        self.query_table_url = f"{base_url}/hy/saas/hy/{app_name}/business/__system_upload__"
        self.authorization = f"{self.app_name}_Authorization"

        self.tb_dict = {
            "sql": self.query_table,
            "redis": self.req_table
        }

    def req_table(self, key=None, table=None, field=None):
        """

        :param key: 当前参数key
        :param table: 表名称
        :param field: 字段名称
        :return:
        """

        if not table:
            return f"参数{key}: table为空无法取值"
        if not field:
            return f"参数{key}: field为空无法取值"

        print(f"=== key ===\n{key}")
        print(f"=== table ===\n{table}")
        print(f"=== field ===\n{field}")

        url = self.query_table_url
        json_data = {
            "businesscode": "__system_upload__",
            "steps": [
                {
                    "function": {
                        "code": "TABLE_SELECT",
                        "params": {
                            "table": table,
                            "condition": {}
                        }
                    }
                }
            ]
        }
        resp = requests.post(url=url, json=json_data, verify=False)
        resp_json = resp.json()
        resp_code = resp_json.get("code")
        table_list = resp_json.get("result").get('data')
        print('=== table_list ===')
        print(table_list)
        if table_list:
            for table in table_list:
                if table.get(field):
                    return table.get(field)
        else:
            return f"未找到字典: {table} 无法取值"

    def query_table(self, key=None, table=None, field=None):
        """

        :param key: 当前参数key
        :param table: 表名称
        :param field: 字段名称
        :return:
        """

        if not table:
            return f"参数{key}: table为空无法取值"
        if not field:
            return f"参数{key}: field为空无法取值"

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

        try:
            func = type_func_dict.get(_type)
            if reverse:
                return func(_fieldSize - 3)

            if _fieldSize < 4:
                res = func(_fieldSize)[0:_fieldSize]
            else:
                res = func(_fieldSize - 4)
            return res
        except BaseException as e:
            return type_func_dict.get(_type)()

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

        if _type in ('object', 'array', 'null'):
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
        elif _dateEngineFieldDataType in ('DICT', 'QUOTE'):
            table = val.get('_associatedReference').get('refTableCode')
            field = val.get('_associatedReference').get('refFieldCode')
            # res = self.query_table(key=key, table=table, field=field)
            res = self.tb_dict.get(self.parse_way)(key=key, table=table, field=field)
        elif _dateEngineFieldDataType in ('IMG', 'FK', 'FILE', 'VIDEO', 'AUDIO'):
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
        print(f"=== id ===\n{self.creator_id}")
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
            "Authorization": "${%s}" % (self.authorization),
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

    @set_app_context
    def gen_authorization(self):
        """生成authorization存入变量"""

        url = f'{self.base_url[0:-5]}:6060/login'
        data = {
            "username": "admin",
            "password": "n8+wekN7GQenwWyUBPVDnA==",
            "pwd_encryption_type": "2",
            "client_type": "4",
            "lessee_code": "hy",
            "app_code": f"{self.app_name}",
            "client_id": "client_hy_web",
            "client_secret": "hy123456"
        }
        print(url)
        print(json.dumps(data, ensure_ascii=False))
        resp = requests.post(url=url, data=data)
        access_token = resp.json().get('access_token')
        if access_token:
            print(access_token)
            query_var = TestVariable.query.filter_by(var_name=self.authorization).first()
            if query_var:
                query_var.var_value = f"Bearer {access_token}"
                db.session.commit()
                print(f"更新:{self.authorization}")
            else:
                new_var = TestVariable(
                    var_name=self.authorization,
                    var_value=f"Bearer {access_token}",
                    var_type=1,
                    var_source="resp_data",
                    var_get_key="access_token",
                    expression="",
                    is_public=1,
                    creator="ParseJsonSchema"
                )
                new_var.save()
                print(f"新增:{self.authorization}")

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
        # self.gen_authorization()


def test_gen_table_to_hashmap():
    """1"""

    gen_table_to_hashmap(
        base_url="http://192.168.14.160:7090",
        app_name="auto"
    )
    print(json.loads(R.get('auto')).get('1386513301277650943'))
    # print(json.loads(R.get('entrance')))


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
        sql = f"""SELECT * FROM `aaaaaaa`.`hy_entrance_busmodel_api_metadata` LIMIT 200;"""

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
    pjs = ParseJsonSchema(app_name='entrance', base_url='http://192.168.14.160:7090', query=result, parse_way="sql")
    pjs.main()


def test_002():
    """1"""

    result = json.loads(R.get('auto')).get('1546763642459009024')
    pjs = ParseJsonSchema(app_name='auto', base_url='http://192.168.14.160:7090', query=result, parse_way='redis')
    pjs.main()
    pjs.gen_authorization()


def test_003():
    """1"""

    result_list = []
    obj = json.loads(R.get('auto'))
    for index, i in enumerate(obj.keys()):
        if index <= 100:
            result_list.append(obj.get(i))
        else:
            break
    for result in result_list:
        pjs = ParseJsonSchema(app_name='auto', base_url='http://192.168.14.160:7090', query=result, parse_way='redis')
        pjs.main()
    pjs.gen_authorization()


def test_004():
    """1"""

    query_result = json.loads(R.get('auto'))
    for key, result in query_result.items():
        pjs = ParseJsonSchema(app_name='auto', base_url='http://192.168.14.160:7090', query=result, parse_way="redis")
        pjs.main()
    pjs.gen_authorization()


def a():
    pjs = ParseJsonSchema(app_name='entrance', base_url='http://192.168.14.160:7090', query={}, parse_way="redis")
    pjs.gen_authorization()


if __name__ == '__main__':
    """main"""
    """
    auto测试id
    1437630647572246528
    
    门禁
    1547415022785933300
    """
    a()

    # test_reset()

    # test_main()
    # test_one()

    # test_002()
    # test_003()
    # test_004()
