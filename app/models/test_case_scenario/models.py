# -*- coding: utf-8 -*-
# @Time    : 2021/9/15 5:43 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCaseScenario(BaseModel):
    __tablename__ = 'exilic_test_case_scenario'
    __table_args__ = {'comment': '测试用例场景'}

    scenario_title = db.Column(db.String(256), comment='场景标题')
    case_list = db.Column(db.JSON, comment='用例id列表按传参排序:[1,3,7,2...]')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseScenario 模型对象-> ID:{} 场景标题:{}'.format(self.id, self.scenario_title)
