# -*- coding: utf-8 -*-
# @Time    : 2022/1/27 5:41 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class UiAutoFile(BaseModel):
    __tablename__ = 'exile_ui_auto_file'
    __table_args__ = {'comment': 'UI自动化脚本目录'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    title = db.Column(db.String(255), nullable=False, comment='脚本描述')
    file_path = db.Column(db.String(255), nullable=False, comment='存放路径')
    file_name_list = db.Column(db.JSON, nullable=False, comment='文件名称列表')
    test_type = db.Column(db.String(255), comment='测试类型')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'UiAutoFile 模型对象-> ID:{} 脚本描述:{} 文件名称:{} 存放路径:{}'.format(
            self.id, self.title, self.file_name, self.file_path,
        )
