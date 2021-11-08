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
    request_base_url = db.Column(db.String(255), nullable=False, comment='请求BaseURL')
    request_url = db.Column(db.String(2048), nullable=False, comment='请求URL')
    is_pass = db.Column(db.Integer, default=0, comment='0-不跳过;1-跳过')
    is_shared = db.Column(db.Integer, default=0, comment='0-仅创建者执行;1-共享执行')
    total_execution = db.Column(db.Integer, default=0, comment='执行次数总计')
    is_public = db.Column(TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def add_total_execution(self):
        """执行次数增加"""
        self.total_execution = self.total_execution + 1
        self.save()

    def __repr__(self):
        return 'TestCase 模型对象-> ID:{} 用例名称:{}'.format(self.id, self.case_name)


class TestCaseData(BaseModel):
    __tablename__ = 'exilic_test_case_data'
    __table_args__ = {'comment': '测试用例参数'}

    data_name = db.Column(db.String(255), nullable=False, comment='数据名称')
    request_params = db.Column(db.JSON, comment='请求参数')
    request_headers = db.Column(db.JSON, comment='headers')
    request_body = db.Column(db.JSON, comment='body')
    request_body_type = db.Column(TINYINT(3, unsigned=True), comment='body请求参数类型:1-FormData;2-JsonData;3-X-FormData')
    var_list = db.Column(db.JSON, comment='引用变量列表')
    update_var_list = db.Column(db.JSON, comment='更新变量列表')
    is_public = db.Column(TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseData 模型对象-> ID:{} 数据名称:{}'.format(self.id, self.data_name)
