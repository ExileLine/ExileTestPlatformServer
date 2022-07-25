# -*- coding: utf-8 -*-
# @Time    : 2022/1/12 11:19 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class MailConfModel(BaseModel):
    __tablename__ = 'exile_mail_conf'
    __table_args__ = {'comment': '邮件推送配置表'}

    mail = db.Column(db.String(255), comment='邮箱')
    mail_user = db.Column(db.String(255), comment='邮箱用户')
    is_send = db.Column(TINYINT(1, unsigned=True), comment='是否为发送账号')
    send_pwd = db.Column(db.String(255), comment='发件邮箱的授权码')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MailConfModel 模型对象-> ID:{} 邮箱:{}'.format(self.id, self.mail)


class DingDingConfModel(BaseModel):
    __tablename__ = 'exile_ding_ding_conf'
    __table_args__ = {'comment': '钉钉推送配置表'}

    title = db.Column(db.String(1024), comment='标题描述(机器人名称)')
    ding_talk_url = db.Column(db.String(1024), comment='DING_TALK_URL')
    at_mobiles = db.Column(db.JSON, comment='AT_MOBILES')
    at_user_ids = db.Column(db.JSON, comment='AT_USER_IDS')
    is_at_all = db.Column(db.Integer, default=0, comment='IS_AT_ALL')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'DingDingConfModel 模型对象-> ID:{} 标题描述:{}'.format(self.id, self.title)
