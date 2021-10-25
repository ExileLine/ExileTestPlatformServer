# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 7:54 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class TestCaseAssResponse(BaseModel):
    __tablename__ = 'exilic_ass_response'
    __table_args__ = {'comment': '断言返回值规则'}

    assert_description = db.Column(db.String(255), nullable=False, comment='断言描述')
    ass_json = db.Column(db.JSON, comment='断言')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseAssResponse 模型对象-> id:{} 断言描述:{} 断言规则:{}'.format(
            self.id, self.assert_description, self.ass_json
        )


class TestCaseAssField(BaseModel):
    __tablename__ = 'exilic_ass_field'
    __table_args__ = {'comment': '断言字段规则'}

    assert_description = db.Column(db.String(255), nullable=False, comment='断言描述')
    ass_json = db.Column(db.JSON, comment='断言')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseAssField 模型对象-> id:{} 断言描述:{} 断言规则:{}'.format(
            self.id, self.assert_description, self.ass_json
        )


class TestCaseDataAssBind(BaseModel):
    __tablename__ = 'exilic_ass_bind'
    __table_args__ = {'comment': '用例断言关系绑定'}

    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    data_id = db.Column(BIGINT(20, unsigned=True), comment='数据id')
    ass_resp_id_list = db.Column(db.JSON, comment='resp断言规则list')
    ass_field_id_list = db.Column(db.JSON, comment='field断言规则list')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseDataAssBind 模型对象-> ID:{} 数据id:{} resp断言规则list:{} field断言规则list:{}'.format(
            self.id, self.data_id, self.ass_resp_id_list, self.ass_field_id_list
        )


class TestCaseBefore(BaseModel):
    __tablename__ = 'exilic_test_case_before'
    __table_args__ = {'comment': '用例前置'}

    before_sql = db.Column(db.String(1024), comment='sql')


class TestCaseAfter(BaseModel):
    __tablename__ = 'exilic_test_case_after'
    __table_args__ = {'comment': '用例后置'}

    after_sql = db.Column(db.String(1024), comment='sql')
