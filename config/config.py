# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 4:02 PM
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : config.py

import os
import configparser
from datetime import timedelta

import redis
from flask_apscheduler.auth import HTTPBasicAuth
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.redis import RedisJobStore

PROJECT_NAME = 'ExileTestPlatformServer'


def get_config():
    """获取配置文件"""
    conf = configparser.ConfigParser()
    flask_env = os.environ.get('FLASK_ENV')
    base_path = os.getcwd().split(PROJECT_NAME)[0] + '{}/config/'.format(PROJECT_NAME)

    default_env = {
        'config_path': base_path + 'dev.ini',
        'msg': '本地配置文件:{}'.format(base_path + 'dev.ini'),
    }

    env_path_dict = {
        'default': default_env,
        'production': {
            'config_path': base_path + 'pro.ini',
            'msg': 'prod配置文件:{}'.format(base_path + 'pro.ini')
        },
    }
    env_obj = env_path_dict.get(flask_env, default_env)
    msg = env_obj.get('msg')
    config_path = env_obj.get('config_path')
    print(msg)
    conf.read(config_path)
    return conf


class BaseConfig:
    """配置基类"""
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'ShaHeTop-Almighty-ares'  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = True
    # SERVER_NAME = 'example.com'
    RUN_HOST = '0.0.0.0'
    RUN_PORT = 9999

    @staticmethod
    def init_app(app):
        pass


class NewConfig(BaseConfig):
    """区分配置文件"""

    conf = get_config()  # 根据环境变量获取对应的配置文件

    # base
    SECRET_KEY = conf.get('base', 'SECRET_KEY')  # session加密
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)  # 设置session过期时间
    DEBUG = conf.getboolean('base', 'DEBUG')
    RUN_HOST = conf.get('base', 'RUN_HOST')
    RUN_PORT = conf.getint('base', 'RUN_PORT')

    # mysql
    MYSQL_USERNAME = conf.get('mysql', 'USERNAME')
    MYSQL_PASSWORD = conf.get('mysql', 'PASSWORD')
    MYSQL_HOSTNAME = conf.get('mysql', 'HOSTNAME')
    MYSQL_PORT = conf.getint('mysql', 'PORT')
    MYSQL_DATABASE = conf.get('mysql', 'DATABASE')
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        MYSQL_USERNAME,
        MYSQL_PASSWORD,
        MYSQL_HOSTNAME,
        MYSQL_PORT,
        MYSQL_DATABASE
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_MAX_OVERFLOW = 10

    # redis
    REDIS_HOST = conf.get('redis', 'REDIS_HOST')
    REDIS_PORT = conf.get('redis', 'REDIS_PORT')
    REDIS_PWD = conf.get('redis', 'REDIS_PWD')
    DECODE_RESPONSES = conf.getboolean('redis', 'DECODE_RESPONSES')
    REDIS_DB = conf.getint('redis', 'REDIS_DB')
    redis_obj = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'password': REDIS_PWD,
        'decode_responses': DECODE_RESPONSES,
        'db': REDIS_DB
    }
    POOL = redis.ConnectionPool(**redis_obj)
    R = redis.Redis(connection_pool=POOL)

    # apscheduler
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'  # 配置时区
    SCHEDULER_API_ENABLED = True  # 新增Api
    SCHEDULER_API_PREFIX = "/api/scheduler"  # Api前缀
    SCHEDULER_AUTH = HTTPBasicAuth()  # 鉴权
    SCHEDULER_DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
        MYSQL_USERNAME,
        MYSQL_PASSWORD,
        MYSQL_HOSTNAME,
        MYSQL_PORT,
        'APSchedulerJobs'
    )
    SCHEDULER_REDIS_URI = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'password': REDIS_PWD,
        'db': 4
    }

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SCHEDULER_DB_URI)
        # 'default': RedisJobStore(**SCHEDULER_REDIS_URI)
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }


config_obj = {
    'production': None,
    'development': None,
    'default': NewConfig,
    'new': NewConfig
}

if __name__ == '__main__':
    print(config_obj['default'].DB_URI)

    print(config_obj['default'].DB_URI)
    print(config_obj['new'].DB_URI)
    print(config_obj['default'].R)
    print(config_obj['new'].R)

    print(config_obj['new'].RUN_HOST)
    print(config_obj['new'].RUN_PORT)
    print(config_obj['new'].DEBUG)
    os.environ['yyx'] = 'yyyyyyyyyyyyyyy'
    print(os.environ)
