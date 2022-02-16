# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 9:49 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestProject(BaseModel):
    __tablename__ = 'exile_test_project'
    __table_args__ = {'comment': '项目表'}

    project_name = db.Column(db.String(128), nullable=False, unique=True, comment='项目名称')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestProject 模型对象-> ID:{} 项目名称:{}'.format(self.id, self.project_name)


class TestProjectVersion(BaseModel):
    __tablename__ = 'exile_test_project_version'
    __table_args__ = {'comment': '项目版本迭代表'}

    version_name = db.Column(db.String(128), nullable=False, unique=True, comment='版本名称')
    version_number = db.Column(db.String(32), nullable=False, unique=True, comment='版本号')
    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestProjectVersion 模型对象-> ID:{} 版本名称:{} 版本号:{}'.format(self.id, self.version_name, self.version_number)


class MidProjectVersionAndCase(BaseModel):
    __tablename__ = 'exile_test_mid_version_case'
    __table_args__ = (
        db.Index('idx_version_case', 'version_id', 'case_id', 'is_deleted'),
        {'comment': '版本迭代用例中间表'}
    )
    version_id = db.Column(BIGINT(20, unsigned=True), comment='版本迭代id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')

    def __repr__(self):
        return 'MidProjectVersionAndCase 模型对象-> ID:{} 版本迭代id:{} 用例id:{}'.format(self.id, self.version_id, self.case_id)
