# -*- coding: utf-8 -*-
# @Time    : 2022/6/13 20:49
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : postman_import.py
# @Software: PyCharm

import time
import json
import shortuuid

from tasks.celery import cel
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind
from app.models.test_project.models import db, MidProjectAndCase, MidVersionCase, MidModuleCase
from app.models.file_import.models import FileImportHistory
from common.libs.set_app_context import set_app_context


class PostManFileImport:
    """导入postman接口文件"""

    request_body_type_dict = {
        "raw": 2,
        "formdata": 1,
        "urlencoded": 3
    }

    def __init__(self, creator=None, creator_id=None):
        self.case_list = []
        self.query = None
        self.body = None
        self.new_case_ids = []
        self.creator = creator
        self.creator_id = creator_id

    def filter_case(self, item):
        """
        解析出文件中的用例对象
        :param item:
        :return:
        """

        if isinstance(item, list):
            for obj in item:
                if isinstance(obj.get('item'), list):
                    # print(obj.get('name'), len(obj.get('item')))
                    self.filter_case(obj.get('item'))
                else:
                    self.case_list.append(obj)
        return self.case_list

    def gen_request_params(self):
        """生成params"""

        request_params = {}
        if self.query:
            for i in self.query:
                request_params[i.get('key')] = i.get('value')

        return request_params

    def gen_request_body(self):
        """生成body"""

        request_body = {}
        if self.body:
            mode = self.body.get('mode')
            print('mode', mode)
            if mode == "raw":
                print("=== json ===")
                j_s = self.body.get(mode)
                if j_s:
                    request_body = json.loads(j_s)
                else:
                    request_body = {}
            elif mode in ('formdata', 'urlencoded'):
                print(f"=== {mode} ===")
                for i in self.body.get(mode):
                    request_body[i.get('key')] = i.get('value')

            request_body_type = self.request_body_type_dict.get(mode)
        else:
            request_body_type = None

        return request_body, request_body_type

    @set_app_context
    def gen_case(self, project_id, version_id_list, module_id_list, debug=None):
        """
        生成用例
        :param project_id: 项目id
        :param version_id_list: 版本id列表
        :param module_id_list: 模块id列表
        :param debug: 调试
        :return:
        """

        if self.case_list:
            for index, case in enumerate(self.case_list):

                disableBodyPruning = case.get('protocolProfileBehavior', {}).get('disableBodyPruning')
                case_request = case.get('request')
                url = case_request.get('url', {})
                self.query = url.get('query', [])
                path = url.get('path', [])
                method = case_request.get('method', {})
                header = case_request.get('header', [])
                self.body = case_request.get('body', {})

                # 第一部分
                case_name = case.get('name', f'用例名称为空:{shortuuid.uuid()[0:4]}{int(time.time())}')
                request_method = method
                request_url = '/' + '/'.join(path)
                request_base_url = url.get('raw').split(request_url)[0]

                # 第二部分
                request_headers = {}
                if header:
                    for h in header:
                        request_headers[h.get('key')] = h.get('value')

                request_params = self.gen_request_params()
                request_body, request_body_type = self.gen_request_body()

                if debug:
                    print(index, "=" * 100)
                    print(case_name)
                    print('request_method', request_method)
                    print('request_base_url', request_base_url)
                    print('request_url', request_url)
                    print('request_headers', request_headers, type(request_headers))
                    print('request_params', request_params, type(request_params))
                    print('request_body', request_body, type(request_body))
                    print('request_body_type', request_body_type)

                if not debug:
                    new_test_case = TestCase(
                        case_name=case_name,
                        request_method=request_method,
                        request_base_url=request_base_url,
                        request_url=request_url,
                        is_public=1,
                        remark=f'导入{index}',
                        creator=self.creator,
                        creator_id=self.creator_id,
                    )
                    new_test_case.save()
                    case_id = new_test_case.id

                    self.new_case_ids.append(case_id)

                    data_size = len(json.dumps(request_params)) + len(json.dumps(request_headers)) + len(
                        json.dumps(request_body))

                    new_data = TestCaseData(
                        data_name=f"{case_name}-导入的参数",
                        request_params=request_params,
                        request_headers=request_headers,
                        request_body=request_body,
                        request_body_type=request_body_type,
                        update_var_list=[],
                        is_public=1,
                        data_size=data_size,
                        remark=f'导入{index}',
                        creator=self.creator,
                        creator_id=self.creator_id
                    )
                    new_data.save()

                    data_id = new_data.id
                    case_bind = TestCaseDataAssBind(
                        case_id=case_id,
                        data_id=data_id,
                        ass_resp_id_list=[],
                        ass_field_id_list=[],
                        creator=self.creator,
                        creator_id=self.creator_id
                    )
                    case_bind.save()

                    for case_id in self.new_case_ids:
                        mid_pc = MidProjectAndCase(
                            project_id=project_id, case_id=case_id, creator=self.creator,
                            creator_id=self.creator_id
                        )
                        db.session.add(mid_pc)

                    if version_id_list:
                        list(map(lambda version_id: db.session.add(
                            MidVersionCase(version_id=version_id, case_id=case_id, creator=self.creator,
                                              creator_id=self.creator_id, remark="导入生成")), version_id_list))
                    if module_id_list:
                        list(map(lambda module_id: db.session.add(
                            MidModuleCase(module_id=module_id, case_id=case_id, creator=self.creator,
                                             creator_id=self.creator_id, remark="导入生成")), module_id_list))
                    db.session.commit()


@cel.task
def postman_import(creator, creator_id, project_id, version_id_list, module_id_list, file_name, file_type,
                   file_main_content, remark):
    """

    :param creator:
    :param creator_id:
    :param project_id:
    :param version_id_list:
    :param module_id_list:
    :param file_name:
    :param file_type:
    :param file_main_content:
    :param remark:
    :return:
    """
    main = PostManFileImport(creator=creator, creator_id=creator_id)
    main.filter_case(item=file_main_content.get('item', []))
    main.gen_case(project_id=project_id, version_id_list=version_id_list, module_id_list=module_id_list)

    fih = FileImportHistory(
        file_name=file_name,
        file_type=file_type,
        file_main_content=file_main_content,
        creator=creator,
        creator_id=creator_id,
        remark=remark
    )
    fih.save()
    return "导入完成"
