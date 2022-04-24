# -*- coding: utf-8 -*-
# @Time    : 2022/4/22 09:54
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class TimedTaskModel(BaseModel):
    __tablename__ = 'exile_timed_task'
    __table_args__ = {'comment': '定时任务'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    task_uuid = db.Column(db.String(1024), comment='任务UUID')
    task_name = db.Column(db.String(255), comment='任务名称')
    task_type = db.Column(db.String(255), comment='任务类型')
    task_details = db.Column(db.JSON, comment='任务明细')
    task_status = db.Column(db.String(255), comment='任务状态')
    execute_type = db.Column(db.String(255), comment='执行类型')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TimedTaskModel 模型对象-> ID:{} 任务UUID:{} 任务名称:{} '.format(
            self.id, self.task_uuid, self.task_name
        )
