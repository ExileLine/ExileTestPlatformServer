# -*- coding: utf-8 -*-
# @Time    : 2021/9/4 3:06 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class TestMysql(BaseModel):
    __tablename__ = 'exilic_test_mysql'
    __table_args__ = {'comment': '测试用例-mysql'}

    name = db.Column(db.String(255), nullable=False, comment='名称')
    db_host = db.Column(db.String(2048), nullable=False, comment='host')
    db_port = db.Column(TINYINT(1, unsigned=True), comment='port')
    db_user = db.Column(db.String(255), comment='user')
    db_password = db.Column(db.String(255), comment='password')
    connection_method = db.Column(db.String(255), comment='连接方式:直连,ssh,vpn...')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestMysql 模型对象-> ID:{} name:{}'.format(self.id, self.name)


class TestRedis(BaseModel):
    __tablename__ = 'exilic_test_redis'
    __table_args__ = {'comment': '测试用例-redis'}

    name = db.Column(db.String(255), nullable=False, comment='名称')
    db_host = db.Column(db.String(2048), nullable=False, comment='host')
    db_port = db.Column(TINYINT(1, unsigned=True), comment='port')
    db_user = db.Column(db.String(255), comment='user')
    db_password = db.Column(db.String(255), comment='password')
    redis_db = db.Column(TINYINT(1, unsigned=True), comment='db编号')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestRedis 模型对象-> ID:{} name:{}'.format(self.id, self.name)
