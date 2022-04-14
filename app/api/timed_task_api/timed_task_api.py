# -*- coding: utf-8 -*-
# @Time    : 2022/4/13 21:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : timed_task_api.py
# @Software: PyCharm

import platform

from all_reference import *
from apscheduler.triggers.cron import CronTrigger
from ExtendRegister.apscheduler_register import scheduler

trigger_tuple = ('date', 'interval', 'cron')


def test_date(*args, **kwargs):
    """1"""
    print(args)
    print(kwargs)
    print('test_date...')


def test_interval(*args, **kwargs):
    """1"""
    print(args)
    print(kwargs)
    print('test_interval...')


def test_cron(*args, **kwargs):
    """1"""
    print(args)
    print(kwargs)
    print('test_cron...')


def execute_case_job(*args, **kwargs):
    """1"""
    test_obj_demo = {
        "execute_id": 190,
        "data_driven": False,
        "use_base_url": False,
        "all_case_open": False,
        "all_scenario_open": False,
        "is_dd_push": False,
        "is_send_mail": False,
        "is_all_mail": False,
        "mail_list": [],
        "execute_type": "case",
        "execute_label": "only"
    }
    test_obj = kwargs.get('test_obj')
    if platform.system() == 'Linux':
        url = 'http://0.0.0.0:5000/api/case_exec'
    else:
        url = 'http://0.0.0.0:7272/api/case_exec'

    resp = requests.post(url=url, json=test_obj)
    print(resp.json())


class GenAPSchedulerJob:
    """APScheduler任务"""

    @staticmethod
    def gen_date_job(**kwargs):
        """
        date触发器,最基本的一种调度, 作业任务只会执行一次
        run_date (datetime 或 str) 作业的运行日期或时间
        timezone (datetime.tzinfo 或 str) 指定时区

        {
            "trigger": "date",
            "run_date": "2022-04-14 14:30:00",
            "args": [],
            "kwargs": {}
        }
        :param kwargs:
        :return:
        """

        task_id = f"{shortuuid.uuid()}_{int(time.time())}"
        try:
            scheduler.add_job(
                func=execute_case_job, id=task_id, **kwargs, replace_existing=True, coalesce=True
            )
            return True, task_id
        except BaseException as e:
            return False, str(e)

    @staticmethod
    def gen_interval_job(**kwargs):
        """
        interval固定时间间隔触发, 间隔调度
        weeks (int) – 间隔几周
        days (int) – 间隔几天
        hours (int) – 间隔几小时
        minutes (int) – 间隔几分钟
        seconds (int) – 间隔多少秒
        start_date (datetime|str) – 开始日期
        end_date (datetime|str) – 结束日期
        timezone (datetime.tzinfo|str) – 时区

        {
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 1,
            "start_date": "",
            "end_date": "",
            "args":[],
            "kwargs":{}
        }

        :param kwargs:
        :return:
        """

        task_id = f"{shortuuid.uuid()}_{int(time.time())}"
        try:
            if not kwargs.get('start_date'):
                del kwargs['start_date']
            if not kwargs.get('end_date'):
                del kwargs['end_date']

            seconds = int(kwargs.get('seconds'))
            if seconds <= 0:
                return False, 'seconds(秒) 不能为 0'

            scheduler.add_job(
                func=execute_case_job, id=task_id, **kwargs, replace_existing=True, coalesce=True
            )
            return True, task_id
        except BaseException as e:
            return False, str(e)

    @staticmethod
    def gen_cron_job(**kwargs):
        """
        cron 触发器, 在特定时间周期性地触发，和Linux crontab格式兼容, 它是功能最强大的触发器。
        year (int|str) – 年(4位数字)
        month (int|str) – 月(范围1-12)
        day (int|str) – 日(范围1-31)
        week (int|str) – 周(范围1-53)
        day_of_week (int|str) – 每周内第几天或者星期几(范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
        hour (int|str) – 时(范围0-23)
        minute (int|str) – 分(范围0-59)
        second (int|str) – 秒(范围0-59)
        start_date (datetime|str) – 最早开始日期(包含)
        end_date (datetime|str) – 最晚结束时间(包含)
        timezone (datetime.tzinfo|str) – 指定时区
        jitter (int|None) – 最多延迟作业执行 jitter 秒

        基本传参模式:
            {
                "year": 2022,
                "month": 4,
                "day": 14,
                "week": 18,
                "day_of_week": 5,
                "hour": 14,
                "minute": 3,
                "second": 3,
                "start_date": "",
                "end_date": "",
                "args": [],
                "kwargs": {}
            }

        cron表达传参模式(5位-分时日月周):
            {
                "cron": "* * * * *",
                "start_date": "2022-04-14 15:23:00",
                "end_date": "2032-04-14 15:23:00",
                "args": [1,2,3],
                "kwargs": {
                    "yyx": "123"
                }
            }

        :param kwargs:
        :return:
        """

        task_id = f"{shortuuid.uuid()}_{int(time.time())}"
        try:
            if not kwargs.get('start_date'):
                del kwargs['start_date']
            if not kwargs.get('end_date'):
                del kwargs['end_date']

            # seconds = int(kwargs.get('seconds'))
            # if seconds <= 0:
            #     return False, 'seconds(秒) 不能为 0'

            cron = kwargs.get('cron')
            _args = kwargs.get('args')
            _kwargs = kwargs.get('kwargs')
            scheduler.add_job(
                func=execute_case_job, id=task_id, trigger=CronTrigger.from_crontab(cron),
                args=_args, kwargs=_kwargs,
                replace_existing=True, coalesce=True
            )
            return True, task_id
        except BaseException as e:
            return False, str(e)


job_func_dict = {
    "date": GenAPSchedulerJob.gen_date_job,
    "interval": GenAPSchedulerJob.gen_interval_job,
    "cron": GenAPSchedulerJob.gen_cron_job
}


class APSchedulerTaskApi(MethodView):
    """
    调试APScheduler任务
    GET: 获取APScheduler任务
    POST: 新增APScheduler任务
    PUT: 启动/编辑APScheduler任务
    DELETE: 暂停/删除APScheduler任务
    """

    def get(self, task_id):
        """获取APScheduler任务状态"""

        data = {
            "id": task_id,
            "job_detail": str(scheduler.get_job(task_id)),
        }
        return api_result(code=200, message='操作成功', data=data)

    def post(self):
        """新增APScheduler任务"""

        data = request.get_json()
        trigger = data.get('trigger', '')

        if trigger not in trigger_tuple:
            return api_result(code=400, message=f'触发器类型错误:{trigger}')

        result_bool, result_message = job_func_dict.get(trigger)(**data)

        if not result_bool:
            return api_result(code=400, message=f'新增任务失败:{result_message}')

        return api_result(code=201, message=f'新增任务成功:{result_message}')

    def put(self):
        """启动/编辑APScheduler任务"""

        data = request.get_json()
        action = data.get('action')
        task_id = data.get('task_id')

        if action not in ('start', 'edit'):
            return api_result(code=400, message=f'操作失败:{action}')

        # 启动任务
        if action == 'start':
            try:
                scheduler.resume_job(task_id)
                return api_result(code=204, message=f'启动任务:{task_id}成功')
            except BaseException as e:
                return api_result(code=400, message=f'启动任务:{task_id}失败,{str(e)}')

        # 编辑任务
        if action == 'edit':
            try:
                # TODO
                # task_id = f"{shortuuid.uuid}_{int(time.time())}"
                # seconds = int(data.get('seconds'))
                # scheduler.add_job(func=test_job, id=task_id, trigger='interval', seconds=seconds, replace_existing=True)
                return api_result(code=204, message=f'编辑任务:{task_id}成功')
            except BaseException as e:
                return api_result(code=400, message=f'编辑任务:{task_id}失败,{str(e)}')

    def delete(self):
        """暂停/删除APScheduler任务"""

        data = request.get_json()
        action = data.get('action')
        task_id = data.get('task_id')

        if action not in ('stop', 'del'):
            return api_result(code=400, message=f'操作失败:{action}')

        # 暂停任务
        if action == 'stop':
            try:
                scheduler.pause_job(task_id)
                print(scheduler.get_job(task_id), type(scheduler.get_job(task_id)))
                return api_result(code=204, message=f'暂停任务:{task_id}成功')
            except BaseException as e:
                return api_result(code=400, message=f'暂停任务:{task_id}失败,{str(e)}')

        # 删除任务
        if action == 'del':
            try:
                scheduler.remove_job(task_id)

                return api_result(code=204, message=f'删除任务:{task_id}成功')
            except BaseException as e:
                return api_result(code=400, message=f'删除任务:{task_id}失败,{str(e)}')
