# -*- coding: utf-8 -*-
# @Time    : 2022/5/4 17:45
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : file_import_api.py
# @Software: PyCharm

from all_reference import *
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseDataAssBind
from app.models.test_project.models import TestProject, MidProjectAndCase, TestProjectVersion, TestModuleApp, \
    MidVersionAndCase, MidModuleAndCase
from tasks.postman_import import postman_import


class PostManFileImport:
    """导入postman接口文件"""

    request_body_type_dict = {
        "raw": 2,
        "formdata": 1,
        "urlencoded": 3
    }

    def __init__(self):
        self.case_list = []
        self.query = None
        self.body = None
        self.new_case_ids = []

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
                        is_shared=1,
                        is_public=1,
                        remark=f'导入{index}',
                        creator=g.app_user.username,
                        creator_id=g.app_user.id,
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
                        creator=g.app_user.username,
                        creator_id=g.app_user.id
                    )
                    new_data.save()

                    data_id = new_data.id
                    case_bind = TestCaseDataAssBind(
                        case_id=case_id,
                        data_id=data_id,
                        ass_resp_id_list=[],
                        ass_field_id_list=[],
                        creator=g.app_user.username,
                        creator_id=g.app_user.id
                    )
                    case_bind.save()

                    for case_id in self.new_case_ids:
                        mid_pc = MidProjectAndCase(
                            project_id=project_id, case_id=case_id, creator=g.app_user.username,
                            creator_id=g.app_user.id
                        )
                        db.session.add(mid_pc)

                    if version_id_list:
                        list(map(lambda version_id: db.session.add(
                            MidVersionAndCase(version_id=version_id, case_id=case_id, creator=g.app_user.username,
                                              creator_id=g.app_user.id, remark="导入生成")), version_id_list))
                    if module_id_list:
                        list(map(lambda module_id: db.session.add(
                            MidModuleAndCase(module_id=module_id, case_id=case_id, creator=g.app_user.username,
                                             creator_id=g.app_user.id, remark="导入生成")), module_id_list))
                    db.session.commit()


class InterfaceFileImportApi(MethodView):
    """
    导入接口文档
    POST: 导入
    """

    def post(self):
        """导入"""

        file = request.files.get('file')
        project_id = request.form.get('project_id')
        version_id_list = request.form.get('version_id_list')
        module_id_list = request.form.get('module_id_list')
        import_type = request.form.get('import_type')
        remark = request.form.get('remark')
        file_name = file.filename

        if file_name.split('.')[-1] not in ('json',):
            return api_result(code=400, message="当前仅支持 .json 文件导入")

        file_content = str(file.read(), encoding="utf-8")
        file_content_json = json.loads(file_content)
        version_id_list = json.loads(version_id_list) if version_id_list else []
        module_id_list = json.loads(module_id_list) if module_id_list else []
        print(file)
        print(file_name)
        print(version_id_list, type(version_id_list))
        print(module_id_list, type(module_id_list))

        query_project = TestProject.query.get(project_id)
        if not query_project:
            return api_result(code=400, message=f'项目: {project_id} 不存在')

        if version_id_list:
            query_version_list = TestProjectVersion.query.filter(
                TestProjectVersion.project_id == project_id,
                TestProjectVersion.id.in_(version_id_list)
            ).all()
            print(query_version_list)
            if len(query_version_list) != len(version_id_list):
                return api_result(code=400, message='版本迭代不存在')

        if module_id_list:
            query_module_list = TestModuleApp.query.filter(
                TestModuleApp.project_id == project_id,
                TestModuleApp.id.in_(module_id_list)
            ).all()
            print(query_module_list)
            if len(query_module_list) != len(module_id_list):
                return api_result(code=400, message='模块不存在')

        """
        main = PostManFileImport()
        main.filter_case(item=file_content_json.get('item', []))
        main.gen_case(project_id=project_id, version_id_list=version_id_list, module_id_list=module_id_list)

        fih = FileImportHistory(
            file_name=file_name,
            file_type=import_type,
            file_main_content=file_content_json,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        fih.save()
        """

        postman_import.delay(
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            project_id=project_id,
            version_id_list=version_id_list,
            module_id_list=module_id_list,
            file_name=file_name,
            file_type=import_type,
            file_main_content=file_content_json,
            remark=remark
        )
        return api_result(code=201, message='操作成功')


if __name__ == '__main__':
    ddd = {
        "info": {
            "_postman_id": "9b83fe72-aa8a-438b-9bb8-8f2e3acf6781",
            "name": "zzzzzzz",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "第一层001",
                "item": [
                    {
                        "name": "第二层001",
                        "item": [
                            {
                                "name": "登录111",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            },
                            {
                                "name": "登录222",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            }
                        ]
                    },
                    {
                        "name": "第二层001 C",
                        "item": [
                            {
                                "name": "登录333",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            },
                            {
                                "name": "登录444",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            }
                        ]
                    },
                    {
                        "name": "通过token获取用户111",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "token",
                                    "value": "d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122",
                                    "type": "text"
                                }
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/auth",
                                "host": [
                                    "{{base_url}}"
                                ],
                                "path": [
                                    "api",
                                    "auth"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "通过token获取用户222",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "token",
                                    "value": "d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122",
                                    "type": "text"
                                }
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/auth",
                                "host": [
                                    "{{base_url}}"
                                ],
                                "path": [
                                    "api",
                                    "auth"
                                ]
                            }
                        },
                        "response": []
                    }
                ]
            },
            {
                "name": "第一层002",
                "item": [
                    {
                        "name": "第二层002",
                        "item": [
                            {
                                "name": "登录555",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            },
                            {
                                "name": "登录666",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            }
                        ]
                    },
                    {
                        "name": "第二层 002 C",
                        "item": [
                            {
                                "name": "登录 777",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            },
                            {
                                "name": "登录888",
                                "event": [
                                    {
                                        "listen": "test",
                                        "script": {
                                            "exec": [
                                                "var json_data = JSON.parse(responseBody)",
                                                "",
                                                "var token = json_data.data.token",
                                                "",
                                                "pm.environment.set(\"token\", token)"
                                            ],
                                            "type": "text/javascript"
                                        }
                                    }
                                ],
                                "request": {
                                    "method": "POST",
                                    "header": [],
                                    "body": {
                                        "mode": "raw",
                                        "raw": "{\n    \"username\": \"yyx\",\n    \"password\": \"123456\"\n}",
                                        "options": {
                                            "raw": {
                                                "language": "json"
                                            }
                                        }
                                    },
                                    "url": {
                                        "raw": "{{base_url}}/api/login",
                                        "host": [
                                            "{{base_url}}"
                                        ],
                                        "path": [
                                            "api",
                                            "login"
                                        ]
                                    }
                                },
                                "response": []
                            }
                        ]
                    },
                    {
                        "name": "通过token获取用户333",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "token",
                                    "value": "d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122",
                                    "type": "text"
                                }
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/auth",
                                "host": [
                                    "{{base_url}}"
                                ],
                                "path": [
                                    "api",
                                    "auth"
                                ]
                            }
                        },
                        "response": []
                    },
                    {
                        "name": "通过token获取用户444",
                        "request": {
                            "method": "GET",
                            "header": [
                                {
                                    "key": "token",
                                    "value": "d83cff2cYYxba11YYx11ecYYxb3c3YYxacde48001122",
                                    "type": "text"
                                }
                            ],
                            "url": {
                                "raw": "{{base_url}}/api/auth",
                                "host": [
                                    "{{base_url}}"
                                ],
                                "path": [
                                    "api",
                                    "auth"
                                ]
                            }
                        },
                        "response": []
                    }
                ]
            },
            {
                "name": "第一层003",
                "item": [
                    {
                        "name": "第二层003",
                        "item": []
                    },
                    {
                        "name": "第二层003 C",
                        "item": []
                    }
                ]
            },
            {
                "name": "退出 111",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {
                            "key": "token",
                            "value": "7694a270YYxba08YYx11ebYYx9da4YYxacde48001122",
                            "type": "text",
                            "disabled": True
                        }
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/login",
                        "host": [
                            "{{base_url}}"
                        ],
                        "path": [
                            "api",
                            "login"
                        ]
                    }
                },
                "response": []
            },
            {
                "name": "退出 222",
                "request": {
                    "method": "DELETE",
                    "header": [
                        {
                            "key": "token",
                            "value": "7694a270YYxba08YYx11ebYYx9da4YYxacde48001122",
                            "type": "text",
                            "disabled": True
                        }
                    ],
                    "url": {
                        "raw": "{{base_url}}/api/login",
                        "host": [
                            "{{base_url}}"
                        ],
                        "path": [
                            "api",
                            "login"
                        ]
                    }
                },
                "response": []
            }
        ]
    }
    m = PostManFileImport()
    m.filter_case(ddd.get('item', []))
    m.gen_case(1, [], [], debug=True)
