# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 4:02 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestEnv(BaseModel):
    __tablename__ = 'exile_test_env'
    __table_args__ = {'comment': '测试环境'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    env_url = db.Column(db.String(2048), nullable=False, comment='环境url')
    env_name = db.Column(db.String(255), nullable=False, comment='环境名称')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestEnv 模型对象-> ID:{} env_url:{} env_name:{}'.format(self.id, self.env_url, self.env_name)
