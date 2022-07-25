# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:06 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class TestDatabases(BaseModel):
    __tablename__ = 'exile_test_databases'
    __table_args__ = {'comment': '测试用例-databases'}

    name = db.Column(db.String(255), nullable=False, comment='名称')
    db_type = db.Column(db.String(32), comment='库类型')
    db_connection = db.Column(db.JSON, comment='连接方式:直连,ssh,vpn...')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestDatabases 模型对象-> ID:{} name:{} db_connection:{}'.format(self.id, self.name, self.db_connection)
