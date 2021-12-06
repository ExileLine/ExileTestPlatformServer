# -*- coding: utf-8 -*-
# @Time    : 2019-05-16 17:06
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : BaseModel.py
# @Software: PyCharm

import json
import decimal
import time
from datetime import datetime

from flask import g
from sqlalchemy import text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT

from ExtendRegister.db_register import db


class BaseModel(db.Model):
    """
    id:id
    create_timestamp:创建时间戳
    create_time:创建时间DateTime
    update_timestamp:更新时间戳
    update_time:更新时间DateTime
    is_deleted:是否删除
    status:状态
    """

    hidden_fields = []  # 不需要返回的字段与值

    __abstract__ = True

    id = db.Column(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True, comment='id')
    create_time = db.Column(db.DateTime, server_default=db.func.now(), comment='创建时间(结构化时间)')
    create_timestamp = db.Column(BIGINT(20, unsigned=True), default=int(time.time()), comment='创建时间(时间戳)')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间(结构化时间)')
    update_timestamp = db.Column(BIGINT(20, unsigned=True), onupdate=int(time.time()), comment='更新时间(时间戳)')
    is_deleted = db.Column(BIGINT(20, unsigned=True), default=0, comment='0正常;其他:已删除')
    status = db.Column(TINYINT(3, unsigned=True), server_default=text('1'), comment='状态')

    def keys(self):
        """
        返回所有字段对象
        :return:
        """
        return self.__table__.columns

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self, hidden_fields=None):
        """
        Json序列化
        :param hidden_fields: 覆盖类属性 hidden_fields
        :return:
        """
        hf = hidden_fields if hidden_fields and isinstance(hidden_fields, list) else self.hidden_fields

        model_json = {}
        __dict = self.__dict__

        for column in __dict.keys():
            if column not in hf:  # 不需要返回的字段与值
                if hasattr(self, column):
                    field = getattr(self, column)
                    if isinstance(field, decimal.Decimal):  # Decimal -> float
                        field = round(float(field), 2)
                    elif isinstance(field, datetime):  # datetime -> str
                        field = str(field)
                    model_json[column] = field

        del model_json['_sa_instance_state']

        return model_json

    def save(self):
        """
        新增
        :return:
        """
        try:
            db.session.add(self)
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            raise TypeError('save error {}'.format(str(e)))

    @staticmethod
    def save_all(model_list):
        """
        批量新增
        :param model_list:
        :return:
        """
        try:
            db.session.add_all(model_list)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise TypeError('save_all error {}'.format(str(e)))

    def update(self, *args, **kwargs):
        """
        更新
        :param args: 不需要更新的字段列表 demo -> update(*["password"]) ...
        :param kwargs: {字段:值} demo -> update(**{"name":"yyx"}) ...
        :return:
        """
        if args:
            args = list(args) + ['id', 'create_time']
        else:
            args = ['id', 'create_time']

        for attr, value in kwargs.items():
            # print(self, "【{}:{}】-【{}:{}】".format(attr, type(attr), value, type(value)))
            if attr in self.__dict__.keys():
                if attr not in args:
                    new_value = json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value)
                    setattr(self, attr, new_value)
            else:
                pass
        try:
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            raise TypeError('update error {}'.format(str(e)))

    def delete(self):
        """
        逻辑删除
        :return:
        """
        try:
            self.is_deleted = 2
            db.session.commit()
        except BaseException as e:
            db.session.rollback()
            raise TypeError('delete error {}'.format(str(e)))


class BusinessModel:
    """
    业务通用字段
    """
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def create_rich(self, creator=None, creator_id=None, remark=None, is_commit=None):
        """写入操作字段补充"""
        self.creator = creator if creator else g.app_user.username
        self.creator_id = creator_id if creator_id else g.app_user.id
        self.remark = remark
        if is_commit:
            try:
                db.session.add(self)
                db.session.commit()
            except BaseException as e:
                db.session.rollback()
                raise TypeError('create_rich error {}'.format(str(e)))

    def update_rich(self, modifier=None, modifier_id=None, remark=None, is_commit=None):
        """更新操作字段补充"""
        self.creator = modifier if modifier else g.app_user.username
        self.creator_id = modifier_id if modifier_id else g.app_user.id
        self.remark = remark
        if is_commit:
            try:
                db.session.commit()
            except BaseException as e:
                db.session.rollback()
                raise TypeError('update_rich error {}'.format(str(e)))
