# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 7:54 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


# 合并TestCaseAssertion
class TestCaseAssResponse(BaseModel):
    __tablename__ = 'exile_ass_response'
    __table_args__ = {'comment': '断言返回值规则'}

    assert_description = db.Column(db.String(255), nullable=False, comment='断言描述')
    ass_json = db.Column(db.JSON, comment='断言')
    is_public = db.Column(TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseAssResponse 模型对象-> id:{} 断言描述:{} 断言规则:{}'.format(
            self.id, self.assert_description, self.ass_json
        )


# 合并为TestCaseAssertion
class TestCaseAssField(BaseModel):
    __tablename__ = 'exile_ass_field'
    __table_args__ = {'comment': '断言字段规则'}

    assert_description = db.Column(db.String(255), nullable=False, comment='断言描述')
    ass_json = db.Column(db.JSON, comment='断言')
    is_public = db.Column(TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseAssField 模型对象-> id:{} 断言描述:{} 断言规则:{}'.format(
            self.id, self.assert_description, self.ass_json
        )


class TestCaseAssertion(BaseModel):
    __tablename__ = 'exile5_case_assertion'
    __table_args__ = {'comment': '断言规则'}

    hidden_fields = ["_is_public"]
    handle_property = True

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    assert_description = db.Column(db.String(255), nullable=False, comment='断言描述')
    ass_json = db.Column(db.JSON, comment='断言')
    _is_public = db.Column('is_public', TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    assertion_type = db.Column(db.String(64), comment='断言类型:response;field')
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

    def __repr__(self):
        return 'TestCaseAssertion 模型对象-> ID:{} 断言描述:{} 断言类型:{}'.format(
            self.id, self.assert_description, self.assertion_type
        )


class TestCaseDataAssBind(BaseModel):
    __tablename__ = 'exile_ass_bind'
    __table_args__ = (
        db.Index('idx_case_data', 'case_id', 'data_id', 'is_deleted'),
        {'comment': '用例断言关系绑定'}
    )

    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    data_id = db.Column(BIGINT(20, unsigned=True), comment='数据id')
    is_base = db.Column(TINYINT(1, unsigned=True), default=0, comment='基础数据')
    ass_resp_id_list = db.Column(db.JSON, comment='resp断言规则list')
    ass_field_id_list = db.Column(db.JSON, comment='field断言规则list')
    index = db.Column(BIGINT(20, unsigned=True), default=0, comment='排序')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseDataAssBind 模型对象-> ID:{} 数据id:{} resp断言规则list:{} field断言规则list:{}'.format(
            self.id, self.data_id, self.ass_resp_id_list, self.ass_field_id_list
        )
