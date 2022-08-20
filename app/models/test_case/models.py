# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 8:39 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCase(BaseModel):
    __tablename__ = 'exile_test_case'
    __table_args__ = {'comment': '测试用例'}

    hidden_fields = ["_is_public", "_is_shared"]
    handle_property = True

    case_name = db.Column(db.String(255), nullable=False, comment='用户名称')
    request_method = db.Column(db.String(255), nullable=False, comment='请求方式:GET;POST;PUT;DELETE...')
    request_base_url = db.Column(db.String(255), nullable=False, comment='请求BaseUrl')
    request_url = db.Column(db.String(2048), nullable=False, comment='请求URL')
    case_status = db.Column(db.String(255), comment='用例周期状态:active;dev;debug;over')
    is_pass = db.Column(TINYINT(1, unsigned=True), default=0, comment='0-不跳过;1-跳过')
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

    @is_public.setter
    def is_public(self, value):
        if not isinstance(value, bool):
            self._is_shared = False
        else:
            self._is_shared = value

    def add_total_execution(self):
        """执行次数增加"""
        self.total_execution = self.total_execution + 1
        self.save()

    def __repr__(self):
        return 'TestCase 模型对象-> ID:{} 用例名称:{}'.format(self.id, self.case_name)


class TestCaseData(BaseModel):
    __tablename__ = 'exile_test_case_data'
    __table_args__ = {'comment': '测试用例参数'}

    hidden_fields = ["_is_public", "_is_before", "_is_after"]
    handle_property = True

    data_name = db.Column(db.String(255), nullable=False, comment='数据名称')
    request_params = db.Column(db.JSON, comment='params')
    request_params_hash = db.Column(db.JSON, comment='params hash')
    request_headers = db.Column(db.JSON, comment='headers')
    request_headers_hash = db.Column(db.JSON, comment='headers hash')
    request_body = db.Column(db.JSON, comment='body')
    request_body_hash = db.Column(db.JSON, comment='body hash')
    request_body_type = db.Column(db.String(32), comment='none;form-data;x-form-data;json;text;html;xml')
    use_var_list = db.Column(db.JSON, comment='引用变量列表')
    update_var_list = db.Column(db.JSON, comment='更新变量列表')
    _is_public = db.Column('is_public', TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    _is_before = db.Column('is_before', TINYINT(1, unsigned=True), default=0, comment='是否使用前置条件 0-否;1-是')
    data_before = db.Column(db.JSON, default=[], comment='前置条件')
    _is_after = db.Column('is_after', TINYINT(1, unsigned=True), default=0, comment='是否使用后置条件 0-否;1-是')
    data_after = db.Column(db.JSON, default=[], comment='后置条件')
    md5 = db.Column(db.String(512), comment='md5')
    data_size = db.Column(BIGINT(20, unsigned=True), default=0, comment='参数字节数')
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
    def is_before(self):
        return bool(self._is_before)

    @is_before.setter
    def is_before(self, value):
        if not isinstance(value, bool):
            self._is_before = False
        else:
            self._is_before = value

    @property
    def is_after(self):
        return bool(self._is_after)

    @is_after.setter
    def is_after(self, value):
        if not isinstance(value, bool):
            self._is_after = False
        else:
            self._is_after = value

    def __repr__(self):
        return 'TestCaseData 模型对象-> ID:{} 数据名称:{}'.format(self.id, self.data_name)
