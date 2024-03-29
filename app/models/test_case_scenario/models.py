# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:43 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCaseScenario(BaseModel):
    __tablename__ = 'exile5_test_case_scenario'
    __table_args__ = {'comment': '测试用例场景'}

    hidden_fields = ["_is_public", "_is_shared"]
    handle_property = True

    scenario_title = db.Column(db.String(256), comment='场景标题')
    case_list = db.Column(db.JSON, comment='用例id列表按传参排序:[1,3,7,2...]')
    _is_shared = db.Column("is_shared", TINYINT(1, unsigned=True), default=1, comment='0-仅创建者执行;1-共享执行')
    _is_public = db.Column("is_public", TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
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

    def add_total_execution(self):
        """执行次数增加"""
        self.total_execution = self.total_execution + 1
        self.save()

    def __repr__(self):
        return 'TestCaseScenario 模型对象-> ID:{} 场景标题:{}'.format(self.id, self.scenario_title)
