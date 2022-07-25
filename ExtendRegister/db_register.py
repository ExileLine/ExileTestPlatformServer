# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : db_register.py
# @Software: PyCharm


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def register_db(app):
    """db注册"""
    db.init_app(app)
