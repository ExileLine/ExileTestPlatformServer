# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 11:57
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : ui_case_runner.py
# @Software: PyCharm

import json
import time

from common.libs.db import project_db, R
from common.libs.data_dict import GlobalsDict, F
from common.libs.ui_test_runner.ui_case_ctrl import ControlFunction
from common.libs.ui_test_runner.ui_case_logs import UiCaseLogs


class ForLogs:
    """for logs"""

    @staticmethod
    def for_logs_start(d, i):
        """

        :param d: for层数
        :param i: for次数
        :return:
        """

        result = {
            "message": f"=== 第 {d} 层循环，第 {i} 次开始 ==="
        }
        print(result)
        return result

    @staticmethod
    def for_logs_end(d, i):
        """

        :param d: for层数
        :param i: for次数
        :return:
        """

        result = {
            "message": f"=== 第 {d} 层循环，第 {i} 次结束 ==="
        }
        print(result)
        return result


class FunctionOption:
    """控件操作类"""

    @classmethod
    def query_function(cls, business_dict: dict) -> any:
        """
        检验控件名称映射的方法是否在字典中
        :param business_dict: 控件json对象
        :return:
        """

        business_type = business_dict.get('type')
        business_function = business_dict.get('function')
        function_name = ControlFunction.control_dict.get(business_type).get(
            business_function)  # 例子: .get('ui_control').get('open')

        if not function_name:
            print(f"{business_type} 或 {business_function} 不存在")
            return None
        return function_name

    @classmethod
    def getattr_func(cls, o: object, func_name: str) -> any:
        """
        获取实例方法
        :param o: 实例
        :param func_name: 方法名称
        :return:
        """

        f = getattr(o, func_name)
        return f


def for_recursion(action_list: list, data_list: list = None, num: int = 0, deep_num: int = 0, master_function=None,
                  master_function_kw: dict = None, web_driver_example: object = None,
                  logs_example: UiCaseLogs = None) -> None:
    """
    for递归
    :param action_list: 任务列表
    :param data_list: 数据列表
    :param num: 轮次(data_list为空时使用,否则按照数据列表长度作为循序次数)
    :param deep_num: 子循环的轮次
    :param master_function: 主递归函数
    :param master_function_kw: 主递归函数参数
    :param web_driver_example: WebUI实例
    :param logs_example: 日志实例
    :return:
    """

    for i in range(1, num + 1):
        logs_example.logs_add(ForLogs.for_logs_start(deep_num, i))

        for index, ac in enumerate(action_list, 1):
            ac_function = ac.get('function')
            if ac_function == 'for':
                ac_num = ac.get('num')
                ac_action = ac.get('business_list')
                for_recursion(
                    action_list=ac_action,
                    num=ac_num,
                    deep_num=deep_num + 1,
                    master_function=master_function,
                    master_function_kw=master_function_kw,
                    web_driver_example=web_driver_example,
                    logs_example=logs_example
                )
            else:
                ac_type = ac.get('type')
                if ac_type == 'master':
                    master_function([ac], web_driver_example, **master_function_kw)
                else:
                    """
                    selenium等驱动逻辑操作...
                    """
                    res_func = FunctionOption.query_function(business_dict=ac)
                    if not res_func:
                        raise KeyError(f"异常:{ac}")

                    print(">>>", ac)
                    func = FunctionOption.getattr_func(web_driver_example, res_func)
                    func_args = ac.get('args')
                    print(">>> 普通 function 反射执行", func, func_args, '\n')
                    func(**func_args)
                    logs_example.logs_add(ac)

        logs_example.logs_add(ForLogs.for_logs_end(deep_num, i))


def recursion_main(data_list: list, web_driver_example: object = None, logs_example: UiCaseLogs = None):
    """
    主递归
    :param data_list: 执行列表
    :param web_driver_example: webUi实例
    :param logs_example: 日志实例
    :return:
    """

    for data in data_list:
        business_title = data.get('title')
        data_type = data.get('type')
        business_list = data.get('business_list')

        if data_type == "master" and business_list:
            recursion_main(data_list=business_list, web_driver_example=web_driver_example, logs_example=logs_example)
        else:
            res_func = FunctionOption.query_function(business_dict=data)
            if not res_func:
                return False

            function = data.get('function')
            child_business_list = data.get('business_list')

            if function == 'for':
                """
                for function 特殊处理
                """
                for_num = data.get('num')
                for_func_kw = {
                    "action_list": child_business_list,
                    "num": for_num,
                    "deep_num": 1,
                    "master_function": recursion_main,
                    "master_function_kw": {"logs_example": logs_example},
                    "web_driver_example": web_driver_example,
                    "logs_example": logs_example
                }
                for_recursion(**for_func_kw)
            else:
                """
                普通 function 执行
                """
                print(">>>", data)
                func = FunctionOption.getattr_func(web_driver_example, res_func)
                func_args = data.get('args')
                print(">>> 普通 function 反射执行", func, func_args, '\n')
                func(**func_args)

                logs_example.logs_add(data)


class UiCaseRunner:
    """UI用例执行"""

    def __init__(self, data_list: list, web_driver: type, web_driver_kw: dict = None, logs_example: UiCaseLogs = None,
                 is_debug: bool = False):
        """

        :param data_list: 任务列表
        :param web_driver: WebDriver驱动
        :param web_driver_kw: WebDriver构造函数
        :param logs_example: 日志实例
        """
        self.is_debug = is_debug
        self.data_list = data_list
        self.web_driver_kw = web_driver_kw if web_driver_kw else {}
        self.web_driver_example = web_driver(headless=False, **self.web_driver_kw)
        setattr(self.web_driver_example, "snap_var_dict", {})
        self.logs_example = logs_example

    def main(self):
        """main"""

        if self.is_debug:
            recursion_main(
                data_list=self.data_list, web_driver_example=self.web_driver_example, logs_example=self.logs_example
            )
            return True

        else:
            try:
                recursion_main(
                    data_list=self.data_list, web_driver_example=self.web_driver_example, logs_example=self.logs_example
                )
                return True
            except BaseException as e:
                print("=== recursion_main_error ===", str(e))
                return False


class ExecuteUiCase:
    """应用调用UI用例执行"""

    def __init__(self, test_obj: dict = None, web_driver: type = None, is_debug: bool = False):
        self.test_obj = test_obj
        self.web_driver = web_driver
        self.is_debug = is_debug

        self.test_obj = test_obj if test_obj else {}
        self.project_id = test_obj.get('project_id')  # 项目归属id
        self.execute_id = test_obj.get('execute_id')  # 执行名称(用例id,场景id,任务id,模块id...)
        self.execute_name = test_obj.get('execute_name')  # 执行名称(用例名,场景名,任务名,模块名...)
        self.execute_type = test_obj.get('execute_type')  # 执行类型(ui_case,scenario,task,module...)
        self.execute_user_id = test_obj.get('execute_user_id')  # 用户id
        self.execute_username = test_obj.get('execute_username')  # 用户名
        self.execute_is_tourist = test_obj.get('execute_is_tourist')  # 用户是否为游客的标识
        self.trigger_type = test_obj.get('trigger_type')  # 触发执行类型(user_execute,timed_execute...)
        self.execute_logs_id = test_obj.get('execute_logs_id')  # 执行日志id用于执行完毕后回写redis_key等数据
        self.ui_case_list = test_obj.get('ui_case_list')

        self.logs_example = UiCaseLogs()
        self.redis_key = ""  # redis缓存日志的key
        self.execute_status = True  # 执行完全通过标识
        self.start_time = 0
        self.end_time = 0

    def gen_logs(self):
        """
        日志格式化并缓存redis
        :return:
        """

        self.redis_key = f"ui_test_log:{F.gen_datetime(**{'execute': True})}_{F.gen_uuid_short()}"
        ui_case_logs = self.logs_example.get_logs()
        result_summary = self.logs_example.get_test_result()

        return_case_result = {
            "uuid": self.redis_key,
            "execute_user_id": self.execute_user_id,
            "execute_username": self.execute_username,
            "execute_type": self.execute_type,
            "execute_name": self.execute_name,
            "case_logs": [],  # 兼容测试报告数据结构
            "scenario_logs": [],  # 兼容测试报告数据结构
            "ui_case_logs": ui_case_logs,
            "result_summary": result_summary,
        }
        json_str = json.dumps(return_case_result, ensure_ascii=False)
        R.set(self.redis_key, json_str)
        R.expire(self.redis_key, 86400 * 30)

        current_save_dict = GlobalsDict.redis_first_logs_dict(execute_id=self.execute_id)
        save_obj_first = current_save_dict.get(self.execute_type, "未知执行类型")
        R.set(save_obj_first, json_str)
        R.expire(save_obj_first, 86400 * 30)

        if self.is_debug:
            print(json.dumps(return_case_result, ensure_ascii=False))

    def write_back_logs(self, report_url=None, file_name=None):
        """
        回写日志标识
        """

        sql = """UPDATE `ExileTestPlatform5.0`.`exile5_test_execute_logs` SET redis_key='{}', report_url='{}', execute_status={}, file_name='{}', update_time='{}', update_timestamp={} WHERE id={};""".format(
            self.redis_key,
            report_url,
            int(self.execute_status),
            file_name,
            GlobalsDict.gen_datetime(),
            int(time.time()),
            self.execute_logs_id
        )
        project_db.update(sql)

        # self.sio.log(f'=== write_back_logs sql ===\n{sql}')
        # self.sio.log('=== write_back_logs ok ===', status="success")

    def main(self):
        """main"""

        self.start_time = time.time()

        self.logs_example.start_time = self.start_time
        self.logs_example.execute_count = len(self.ui_case_list)

        for index, ui_case in enumerate(self.ui_case_list):
            meta_data = ui_case.get('meta_data')
            new_ucr = UiCaseRunner(
                data_list=meta_data, web_driver=self.web_driver, logs_example=self.logs_example, is_debug=self.is_debug
            )
            execute_result = new_ucr.main()
            if not execute_result:
                d = {
                    "index": index,
                    "error": "UI自动化执行出错"
                }
                self.logs_example.logs_add(d)
                self.logs_example.execute_fail += 1
            else:
                self.logs_example.execute_success += 1

        self.logs_example.end_time = time.time()

        self.gen_logs()
        self.write_back_logs()

        if not self.execute_is_tourist:
            key = f'ui_limit_execution_{self.execute_user_id}_{self.execute_username}'
            R.delete(key)
            print(f"释放游客占用:{key}")
        return 'ok'
