# -*- coding: utf-8 -*-
# @Time    : 2022/5/5 09:42
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm

from common.libs.BaseModel import *


class FileImportHistory(BaseModel):
    __tablename__ = 'exile_file_import_history'
    __table_args__ = {'comment': '接口导入记录表'}

    file_name = db.Column(db.String(255), nullable=False, comment='文件名称')
    file_type = db.Column(db.String(255), nullable=False, comment='文件类型')
    file_main_content = db.Column(db.JSON, nullable=False, comment='文件主要内容')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'FileImportHistory 模型对象-> ID:{} 文件名称:{} 文件类型:{}'.format(
            self.id, self.file_name, self.file_type
        )
