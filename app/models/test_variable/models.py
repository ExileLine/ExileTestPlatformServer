# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:29 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestVariable(BaseModel):
    __tablename__ = 'exile5_test_variable'
    __table_args__ = {'comment': '测试用例变量'}

    hidden_fields = ["_is_source", "_is_expression", "_is_public", "_is_active"]
    handle_property = True

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    var_name = db.Column(db.String(255), nullable=False, comment='变量名称')
    var_init_value = db.Column(db.JSON, nullable=False, comment='初始变量值')
    var_value = db.Column(db.JSON, nullable=False, comment='当前变量值')
    var_type = db.Column(db.String(255), comment='变量值的类型:Str;Int;Json;JsonStr;List;ListStr')
    var_args = db.Column(db.JSON, default={}, comment='函数变量扩展参数')
    var_source = db.Column(db.String(32), comment='值来源:resp_data;resp_header')
    var_get_key = db.Column(db.String(255), comment='值对应的key(用于关系变量获取)')
    expression = db.Column(db.String(255), comment='取值表达式')
    _is_source = db.Column('is_source', TINYINT(1, unsigned=True), default=0, comment='是否关系变量(主要用于前端标识):0-否;1-是')
    _is_expression = db.Column('is_expression', TINYINT(1, unsigned=True), default=0, comment='是否使用取值表达式:0-否;1-是')
    _is_active = db.Column('is_active', TINYINT(1, unsigned=True), default=0, comment='是否每次更新(针对函数变量,在用例场景中):0-否;1-是')
    _is_public = db.Column('is_public', TINYINT(1, unsigned=True), default=0, comment='是否公共使用:0-否;1-是')
    last_func = db.Column(db.String(255), comment='上次最后使用的函数')
    last_func_var = db.Column(db.String(255), comment='上次最后函数使用的值')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    @property
    def is_source(self):
        return bool(self._is_source)

    @is_source.setter
    def is_source(self, value):
        if not isinstance(value, bool):
            self._is_source = False
        else:
            self._is_source = value

    @property
    def is_expression(self):
        return bool(self._is_expression)

    @is_expression.setter
    def is_expression(self, value):
        if not isinstance(value, bool):
            self._is_expression = False
        else:
            self._is_expression = value

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
    def is_active(self):
        return bool(self._is_active)

    @is_active.setter
    def is_active(self, value):
        if not isinstance(value, bool):
            self._is_active = False
        else:
            self._is_active = value

    def __repr__(self):
        return 'TestVariable 模型对象-> ID:{} 变量名称:{} 变量值:{}'.format(self.id, self.var_name, self.var_value)


class TestVariableHistory(BaseModel):
    __tablename__ = 'exile5_test_variable_history'
    __table_args__ = {'comment': '测试用例变量更新历史'}

    var_id = db.Column(BIGINT(20, unsigned=True), comment='变量id')
    update_type = db.Column(db.String(255), comment='更新类型')
    before_var = db.Column(db.JSON, comment='修改前的值')
    after_var = db.Column(db.JSON, comment='修改后的值')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestVariableHistory 模型对象-> ID:{} 变量id:{} 更新类型:{} 修改前的值:{} 修改后的值:{}'.format(
            self.id, self.var_id, self.update_type, self.before_var, self.after_var
        )
