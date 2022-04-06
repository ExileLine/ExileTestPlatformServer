# -*- coding: utf-8 -*-
# @Time    : 2022/1/15 2:04 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class PlatformConfModel(BaseModel):
    __tablename__ = 'exile_platform_conf'
    __table_args__ = {'comment': '平台配置表'}

    platform_conf_uuid = db.Column(db.String(1024), comment='UUID')
    platform_icon = db.Column(db.String(1024), comment='平台logo链接')
    platform_name = db.Column(db.String(255), comment='平台名称')
    platform_login_msg = db.Column(db.String(255), comment='平台登录页面描述信息')
    server_url = db.Column(db.String(255), comment='测试报告url')
    safe_scan_url = db.Column(db.String(255), comment='安全扫码url')
    weights = db.Column(BIGINT(20, unsigned=True), comment='权重')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'PlatformConfModel 模型对象-> ID:{} 平台名称:{}'.format(self.id, self.platform_name)
