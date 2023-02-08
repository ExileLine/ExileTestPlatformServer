# -*- coding: utf-8 -*-
# @Time    : 2023/2/8 15:25
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class UiTestCase(BaseModel):
    __tablename__ = 'exile5_ui_test_case'
    __table_args__ = {'comment': 'UI测试用例'}

    hidden_fields = ["_is_public", "_is_shared"]
    handle_property = True

    case_name = db.Column(db.String(255), nullable=False, comment='用例名称')
    case_status = db.Column(db.String(255), comment='用例周期状态:active;dev;debug;over')
    _is_shared = db.Column('is_shared', TINYINT(1, unsigned=True), default=1, comment='0-仅创建者执行;1-共享执行')
    _is_public = db.Column('is_public', TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    total_execution = db.Column(BIGINT(20, unsigned=True), default=0, comment='执行次数总计')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')
    meta_data = db.Column(db.JSON, comment='业务树')

    @property
    def is_public(self):
        return bool(self._is_public)

    @is_public.setter
    def is_public(self, value):
        if not isinstance(value, bool):
            self._is_public = False
        else:
            self._is_public = value

    @property
    def is_shared(self):
        return bool(self._is_shared)

    @is_shared.setter
    def is_shared(self, value):
        if not isinstance(value, bool):
            self._is_shared = False
        else:
            self._is_shared = value

    def __repr__(self):
        return 'UiTestCase 模型对象-> ID:{} 用例名称:{}'.format(self.id, self.case_name)


class MidProjectAndUiCase(BaseModel):
    __tablename__ = 'exile5_test_mid_project_ui_case'
    __table_args__ = (
        db.Index('idx_project_ui_case', 'project_id', 'case_id'),
        {'comment': '项目-UI用例中间表'}
    )
    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidProjectAndUiCase 模型对象-> ID:{} 项目id:{} 用例id:{}'.format(
            self.id, self.project_id, self.case_id
        )


class MidVersionUiCase(BaseModel):
    __tablename__ = 'exile5_test_mid_version_ui_case'
    __table_args__ = (
        db.Index('idx_version_ui_case', 'version_id', 'case_id'),
        {'comment': '版本迭代-UI用例中间表'}
    )
    version_id = db.Column(BIGINT(20, unsigned=True), comment='迭代id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidVersionUiCase 模型对象-> ID:{} 迭代id:{} 用例id:{}'.format(
            self.id, self.version_id, self.case_id
        )


class MidTaskUiCase(BaseModel):
    __tablename__ = 'exile5_test_mid_task_ui_case'
    __table_args__ = (
        db.Index('idx_task_ui_case', 'task_id', 'case_id'),
        {'comment': '任务-UI用例中间表'}
    )
    task_id = db.Column(BIGINT(20, unsigned=True), comment='任务id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidTaskUiCase 模型对象-> ID:{} 任务id:{} 用例id:{}'.format(
            self.id, self.task_id, self.case_id
        )


class MidModuleUiCase(BaseModel):
    __tablename__ = 'exile5_test_mid_module_ui_case'
    __table_args__ = (
        db.Index('idx_module_ui_case', 'module_id', 'case_id'),
        {'comment': '模块-UI用例中间表'}
    )
    module_id = db.Column(BIGINT(20, unsigned=True), comment='模块id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidModuleUiCase 模型对象-> ID:{} 模块id:{} 用例id:{}'.format(
            self.id, self.module_id, self.case_id
        )
