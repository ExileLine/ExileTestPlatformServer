# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 8:39 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCaseSet(BaseModel):
    __tablename__ = 'exilic_test_case_set'
    __table_args__ = {'comment': '用户用例收藏'}

    user_id = db.Column(BIGINT(20, unsigned=True), comment='用户id')
    case_id_list = db.Column(db.JSON, comment='用例id列表')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCaseSet 模型对象-> ID:{} user_id:{} case_id_list:{}'.format(self.id, self.user_id, self.case_id_list)
