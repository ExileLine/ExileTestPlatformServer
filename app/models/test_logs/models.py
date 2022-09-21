# -*- coding: utf-8 -*-
# @Time    : 2021/10/5 12:33 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestExecuteLogs(BaseModel):
    __tablename__ = 'exile_test_execute_logs'
    __table_args__ = {'comment': '用例执行记录表'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    execute_id = db.Column(db.String(255), comment='用例id/场景id/module_code')
    execute_name = db.Column(db.String(255), nullable=False, comment='用例名称/场景名称')
    execute_type = db.Column(db.String(255), nullable=False, comment='执行类型')
    redis_key = db.Column(db.String(255), nullable=False, comment='Redis的key')
    report_url = db.Column(db.String(1024), nullable=False, comment='报告地址')
    file_name = db.Column(db.String(1024), nullable=False, comment='文件名称带后缀如: xxx.html')
    trigger_type = db.Column(db.String(255), default='user_execute', comment='触发类型:user_execute;timed_execute')
    execute_status = db.Column(TINYINT(1, unsigned=True), comment='执行状态')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestExecuteLogs 模型对象-> ID:{} project_id:{} execute_id:{} execute_name:{} execute_type:{} redis_key:{}'.format(
            self.id, self.project_id, self.execute_id, self.execute_name, self.execute_type, self.redis_key
        )


class TestLogs(BaseModel):
    __tablename__ = 'exile_test_logs'
    __table_args__ = {'comment': '日志记录表'}

    log_type = db.Column(db.String(255), nullable=False, comment='类型')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestLogs 模型对象-> ID:{} log_type:{}'.format(self.id, self.log_type)
