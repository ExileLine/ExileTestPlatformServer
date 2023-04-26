# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 15:29
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class UiPcConf(BaseModel):
    __tablename__ = 'exile5_ui_pc_conf'
    __table_args__ = {'comment': 'UI远端ip配置'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    ui_pc_name = db.Column(db.String(255), nullable=False, comment='远端名称')
    ui_pc_ip = db.Column(db.String(2048), nullable=False, comment='远端ip')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'UiPcConf 模型对象-> ID:{} env_url:{} ui_pc_name:{}'.format(self.id, self.ui_pc_name, self.ui_pc_ip)
