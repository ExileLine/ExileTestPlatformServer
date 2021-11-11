# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 9:29 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestVariable(BaseModel):
    __tablename__ = 'exile_test_variable'
    __table_args__ = {'comment': '测试用例变量'}

    var_name = db.Column(db.String(255), nullable=False, comment='变量名称')
    var_value = db.Column(db.JSON, nullable=False, comment='变量值')
    var_type = db.Column(TINYINT(3, unsigned=True), comment='变量值的类型:Str;Int;Json;JsonStr;List;ListStr')
    var_source = db.Column(TINYINT(3, unsigned=True), comment='值来源:1-resp_data;2-resp_header')
    var_get_key = db.Column(db.String(255), comment='值对应的key(用于关系变量获取)')
    expression = db.Column(db.String(255), comment='取值表达式')
    is_expression = db.Column(TINYINT(1, unsigned=True), default=0, comment='是否使用取值表达式:0-否;1-是')
    last_func = db.Column(db.String(255), comment='上次最后使用的函数')
    last_func_var = db.Column(db.String(255), comment='上次最后函数使用的值')
    is_public = db.Column(TINYINT(1, unsigned=True), default=1, comment='是否公共使用:0-否;1-是')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestVariable 模型对象-> ID:{} 变量名称:{} 变量值:{}'.format(self.id, self.var_name, self.var_value)
