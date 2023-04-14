# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 8:39 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCaseSet(BaseModel):
    __tablename__ = 'exile5_test_case_set'
    __table_args__ = {'comment': '用户用例收藏'}

    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    scenario_id = db.Column(BIGINT(20, unsigned=True), comment='场景id')
    is_set = db.Column(TINYINT(1, unsigned=True), server_default=text('0'), comment='是否收藏0/1')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseSet 模型对象-> ID:{} user_id:{} case_id:{} scenario_id:{}'.format(
            self.id, self.user_id, self.case_id, self.scenario_id
        )
