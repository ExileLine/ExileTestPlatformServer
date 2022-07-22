# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 14:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestCiCdMap(BaseModel):
    __tablename__ = 'exile_cicd_map'
    __table_args__ = {'comment': 'CICD映射表'}
    project_id = db.Column(BIGINT(20, unsigned=True), comment='平台项目id')
    project_name = db.Column(db.String(255), comment='项目名')
    app_name = db.Column(db.String(255), comment='应用名')
    branch_name = db.Column(db.String(255), comment='分支名称')
    mirror = db.Column(db.String(255), comment='镜像')
    url = db.Column(db.String(255), comment='URL')
    obj_json = db.Column(db.JSON, comment='整个json')
    version_id = db.Column(BIGINT(20, unsigned=True), comment='平台版本id')
    task_id = db.Column(BIGINT(20, unsigned=True), comment='平台任务id')
    dd_push_id = db.Column(BIGINT(20, unsigned=True), comment='平台钉钉推送id')
    is_set_url = db.Column(BIGINT(20, unsigned=True), default=0, comment='是否使用cicd的url')
    is_active = db.Column(BIGINT(20, unsigned=True), default=1, comment='是否激活')
    scheduling_id = db.Column(BIGINT(20, unsigned=True), comment='ui auto scheduling_id')
    is_safe_scan = db.Column(BIGINT(20, unsigned=True), default=1, comment='是否安全扫描')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestCICD 模型对象-> ID:{} project_id:{} project_name:{} app_name:{} branch_name:{} mirror:{} url:{}'.format(
            self.id, self.project_id, self.project_name, self.app_name, self.branch_name, self.mirror, self.url
        )
