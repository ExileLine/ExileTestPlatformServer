# -*- coding: utf-8 -*-
# @Time    : 2022/4/7 11:37 上午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class SafeScanConf(BaseModel):
    __tablename__ = 'exile_safe_scan_conf'
    __table_args__ = {'comment': '安全扫描配置表'}

    description = db.Column(db.String(255), comment='描述')
    is_global_open = db.Column(TINYINT(1, unsigned=True), comment='是否全局开启')
    safe_scan_url = db.Column(db.String(255), comment='安全扫码url')
    weights = db.Column(BIGINT(20, unsigned=True), comment='权重')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'SafeScanConf 模型对象-> ID:{} 描述:{} url:{}'.format(self.id, self.description, self.safe_scan_url)
