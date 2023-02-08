# -*- coding: utf-8 -*-
# @Time    : 2023/2/8 15:25
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class UiTestCase(BaseModel):
    __tablename__ = 'exile_ui_test_case'
    __table_args__ = {'comment': 'UI测试用例'}

    hidden_fields = ["_is_public", "_is_shared"]
    handle_property = True

    case_name = db.Column(db.String(255), nullable=False, comment='用例名称')
    _is_shared = db.Column('is_shared', TINYINT(1, unsigned=True), default=1, comment='0-仅创建者执行;1-共享执行')
    _is_public = db.Column('is_public', TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    total_execution = db.Column(BIGINT(20, unsigned=True), default=0, comment='执行次数总计')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

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
