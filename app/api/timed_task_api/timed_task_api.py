# -*- coding: utf-8 -*-
# @Time    : 2022/4/13 21:20
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : timed_task_api.py
# @Software: PyCharm

import platform

from all_reference import *
from config.config import config_obj
from apscheduler.triggers.cron import CronTrigger
from ExtendRegister.apscheduler_register import scheduler
from app.models.timed_task.models import TimedTaskModel
from app.models.test_project.models import TestVersionTask

trigger_tuple = ('date', 'interval', 'cron')


def gen_task_uuid():
    task_id = f"{shortuuid.uuid()[0:10]}_{int(time.time())}"
    return task_id


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
    test_obj['trigger_type'] = 'timed_execute'

    port = config_obj['new'].RUN_PORT

    if platform.system() == 'Linux':
        url = f'http://0.0.0.0:{port}/api/case_exec'
    else:
        url = f'http://0.0.0.0:{port}/api/case_exec'

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

        task_id = gen_task_uuid()
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

        task_id = gen_task_uuid()
        try:
            if 'start_date' in kwargs and not kwargs.get('start_date'):
                del kwargs['start_date']
            if 'end_date' in kwargs and not kwargs.get('end_date'):
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

        task_id = gen_task_uuid()
        try:
            if 'start_date' in kwargs and not kwargs.get('start_date'):
                del kwargs['start_date']
            if 'end_date' in kwargs and not kwargs.get('end_date'):
                del kwargs['end_date']

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


def check_timed_task(task_uuid):
    """检查timed_task"""
    query_timed_task = TimedTaskModel.query.filter_by(task_uuid=task_uuid).first()

    if not query_timed_task:
        return api_result(code=400, message=f'任务: {task_uuid} 不存在')
    else:
        return query_timed_task


class APSchedulerTaskApi(MethodView):
    """
    APScheduler任务
    GET: 获取
    POST: 新增
    PUT: 编辑
    """

    def get(self, timed_task_uuid):
        """获取APScheduler任务状态"""

        query_timed_task = TimedTaskModel.query.get(timed_task_uuid)

        if not query_timed_task:
            return api_result(code=400, message=f'任务:{timed_task_uuid}不存在')

        version_id = None
        execute_type = query_timed_task.execute_type

        if execute_type == "task_all":
            task_details = query_timed_task.task_details
            execute_id = task_details.get('kwargs').get('test_obj').get('execute_id')
            query_version_task = TestVersionTask.query.get(execute_id)
            if query_version_task:
                version_id = query_version_task.version_id

        return api_result(code=200, message=SUCCESS_MESSAGE, data={'version_id': version_id})

    def post(self):
        """新增APScheduler任务"""

        data = request.get_json()
        project_id = data.get('project_id')
        task_name = data.get('task_name', '').strip()
        remark = data.get('remark', '').strip()

        job = data.get('job')
        trigger = job.get('trigger')
        execute_type = job.get('kwargs').get('test_obj').get('execute_type')

        if trigger not in trigger_tuple:
            return api_result(code=400, message=f'触发器类型错误:{trigger}')

        result_bool, result_message = job_func_dict.get(trigger)(**job)

        if not result_bool:
            return api_result(code=400, message=f'新增任务失败:{result_message}')

        new_timed_task = TimedTaskModel(
            project_id=project_id,
            task_uuid=result_message,
            task_name=task_name,
            task_details=job,
            task_status='wait_start',
            task_type=trigger,
            execute_type=execute_type,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_timed_task.save()

        return api_result(code=201, message=f'新增任务成功', data={
            "id": result_message,
            "父进程id": os.getppid(),
            "子进程id": os.getpid(),
            "线程id": threading.get_ident(),
        })

    def put(self):
        """启动/编辑APScheduler任务"""

        data = request.get_json()
        task_uuid = data.get('task_uuid')
        task_name = data.get('task_name')
        remark = data.get('remark')
        job = data.get('job')
        trigger = job.get('trigger')
        execute_type = job.get('kwargs').get('test_obj').get('execute_type')

        if trigger not in trigger_tuple:
            return api_result(code=400, message=f'触发器类型错误:{trigger}')

        result_bool, result_message = job_func_dict.get(trigger)(**job)

        if not result_bool:
            return api_result(code=400, message=f'任务重建失败:{result_message}')

        try:
            scheduler.remove_job(task_uuid)
        except BaseException as e:
            pass

        query_timed_task = check_timed_task(task_uuid)
        query_timed_task.task_uuid = result_message
        query_timed_task.task_name = task_name
        query_timed_task.task_details = job
        query_timed_task.task_status = 'stop'
        query_timed_task.task_type = trigger
        query_timed_task.execute_type = execute_type
        query_timed_task.modifier = g.app_user.username,
        query_timed_task.modifier_id = g.app_user.id,
        query_timed_task.remark = remark
        db.session.commit()
        scheduler.pause_job(result_message)
        return api_result(code=204, message=f'编辑任务:{task_uuid}成功')


class APSchedulerTaskStatusApi(MethodView):
    """
    APScheduler任务状态
    POST: 启动
    PUT: 暂停
    DELETE: 删除
    """

    def post(self):
        """启动"""

        data = request.get_json()
        task_uuid = data.get('task_uuid')
        query_timed_task = check_timed_task(task_uuid)
        try:
            scheduler.resume_job(task_uuid)
            query_timed_task.task_status = 'wait_start'
            db.session.commit()
            return api_result(code=204, message=f'启动任务:{task_uuid}成功1')
        except BaseException as e:
            result_bool, result_message = job_func_dict.get(query_timed_task.task_type)(**query_timed_task.task_details)
            if not result_bool:
                return api_result(code=400, message=f'启动任务:{task_uuid}失败,{result_message}')
            query_timed_task.task_status = 'wait_start'
            db.session.commit()
            return api_result(code=204, message=f'启动任务:{result_message}成功2')

    def put(self):
        """暂停"""

        data = request.get_json()
        task_uuid = data.get('task_uuid')
        query_timed_task = check_timed_task(task_uuid)
        try:
            scheduler.pause_job(task_uuid)
        except BaseException as e:
            query_timed_task.status = 88
        query_timed_task.task_status = 'stop'
        db.session.commit()
        return api_result(code=204, message=f'暂停任务:{task_uuid}成功')

    def delete(self):
        """删除"""

        data = request.get_json()
        task_uuid = data.get('task_uuid')
        query_timed_task = check_timed_task(task_uuid)
        try:
            scheduler.remove_job(task_uuid)
        except BaseException as e:
            query_timed_task.status = 99
        query_timed_task.task_status = 'deleted'
        query_timed_task.is_deleted = query_timed_task.id
        db.session.commit()
        return api_result(code=204, message=f'删除任务:{task_uuid}成功')


class APSchedulerTaskPageApi(MethodView):
    """
    APScheduler task page api
    POST: 定时任务分页模糊查询
    """

    def post(self):
        """定时任务分页模糊查询"""

        data = request.get_json()
        project_id = data.get('project_id')
        creator_id = data.get('creator_id')
        task_name = data.get('task_name', '')
        task_type = data.get('task_type', '')
        is_deleted = data.get('is_deleted', False)
        page = data.get('page')
        size = data.get('size')
        limit = page_size(page=page, size=size)

        sql = f"""
        SELECT
            A.id,
            A.task_uuid,
            A.task_name,
            A.task_type,
            A.task_details,
            A.task_status,
            A.creator,
            A.create_time,
            A.modifier,
            A.update_time,
            FROM_UNIXTIME(B.next_run_time) as next_run_time,
            A.remark
        FROM
            exile5_timed_task A
            LEFT JOIN APSchedulerJobs.apscheduler_jobs B ON A.task_uuid = B.id
        WHERE
            A.project_id = {project_id}
            AND A.is_deleted=0
            {f'AND A.creator_id={creator_id}' if creator_id else ''}
            {f"AND A.task_type='{task_type}'" if task_type else ''}
            AND A.task_name LIKE "%{task_name}%"
        ORDER BY 
        A.create_time DESC
        LIMIT {limit[0]},{limit[1]};
        """

        sql_count = f"""
        SELECT
            COUNT(*)
        FROM
            exile5_timed_task A
            LEFT JOIN APSchedulerJobs.apscheduler_jobs B ON A.task_uuid = B.id
        WHERE
            A.project_id = {project_id}
            AND A.is_deleted=0
            {f'AND A.creator_id={creator_id}' if creator_id else ''}
            {f"AND A.task_type='{task_type}'" if task_type else ''}
            AND A.task_name LIKE "%{task_name}%";
        """

        result_list = project_db.select(sql)
        result_count = project_db.select(sql_count)

        result_data = {
            'records': result_list if result_list else [],
            'now_page': page,
            'total': result_count[0].get('COUNT(*)')
        }

        return api_result(code=200, message=SUCCESS_MESSAGE, data=result_data)
