# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 8:39 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCase(BaseModel):
    __tablename__ = 'exilic_test_case'
    __table_args__ = {'comment': '测试用例'}

    case_name = db.Column(db.String(255), nullable=False, comment='用户名称')
    request_method = db.Column(db.String(255), nullable=False, comment='请求方式:GET;POST;PUT;DELETE')
    request_url = db.Column(db.String(2048), nullable=False, comment='请求URL')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCase 模型对象-> ID:{} 用例名称:{}'.format(self.id, self.case_name)


class TestCaseData(BaseModel):
    __tablename__ = 'exilic_test_case_data'
    __table_args__ = {'comment': '测试用例参数'}

    data_name = db.Column(db.String(255), nullable=False, comment='用户名称')
    request_params = db.Column(db.JSON, comment='请求参数')
    request_headers = db.Column(db.JSON, comment='headers')
    request_body = db.Column(db.JSON, comment='body')
    request_body_type = db.Column(TINYINT(3, unsigned=True), comment='body请求参数类型:1-FormData;2-JsonData;3-X-FormData')
    var_list = db.Column(db.JSON, comment='引用变量列表')
    update_var_list = db.Column(db.JSON, comment='更新变量列表')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseData 模型对象-> ID:{} 数据名称:{}'.format(self.id, self.data_name)


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
