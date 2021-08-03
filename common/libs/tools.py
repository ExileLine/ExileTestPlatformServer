# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 11:29
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : tools.py
# @Software: PyCharm

import json
import decimal
from datetime import datetime

import pymysql
from flask import request
from sqlalchemy import or_
from loguru import logger

from config.config import config_obj

CONFIG_OBJ = config_obj.get('new')
R = CONFIG_OBJ.R
DB = {
    'user': CONFIG_OBJ.MYSQL_USERNAME,
    'password': CONFIG_OBJ.MYSQL_PASSWORD,
    'host': CONFIG_OBJ.MYSQL_HOSTNAME,
    'port': CONFIG_OBJ.MYSQL_PORT,
    'db': CONFIG_OBJ.MYSQL_DATABASE
}


def print_logs():
    """logs"""
    host = request.host
    method = request.method
    path = request.path
    logger.info(host)
    logger.info(method)
    logger.info(path)
    logger.info('=== headers ===')
    headers = {k: v for k, v in request.headers.items()}
    json_format(headers)
    logger.info('=== params ===')
    json_format(request.args.to_dict())
    logger.info('=== data ===')
    json_format(request.form.to_dict())
    logger.info('=== json ===')
    json_format(request.get_json())
    logger.info('=== end print_logs ===')


def check_keys(dic, *keys):
    for k in keys:
        if k not in dic.keys():
            return False
    return True


def json_format(d):
    """json格式打印"""
    try:
        logger.info('\n' + json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
        # print(json.dumps(d, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    except BaseException as e:
        logger.info(d)
        # print(d)


def general_paging_fuzzy_query(q, model, like_params, where_dict, page=1, size=20):
    """
    通用分页模糊查询(单表)
    :param q: 搜索内容
    :param model: 模型
    :param like_params: 模糊查询字段
    :param where_dict: 条件
    :param page: 页码
    :param size: 条数
    :return:
    """
    where_list = []
    if where_dict:
        for k, v in where_dict.items():
            if hasattr(model, k):
                where_list.append(getattr(model, k) == v)

    like_list = []
    for k, v in model.__dict__.items():
        if k in like_params:
            # print(k, type(k), '======', v, type(v))
            like_list.append(v.ilike("%{}%".format(q if q else '')))  # 模糊条件: v -> Model.Column.ilike
    pagination = model.query.filter(or_(*like_list), *where_list).order_by(model.create_time.desc())
    pagination = pagination.paginate(page=int(page), per_page=int(size), error_out=False)

    # result_list = []
    # for i in pagination.items:
    #     obj = i.to_json()
    #     result_list.append(obj)

    result_list = [i.to_json() for i in pagination.items]
    return result_list


class MyPyMysql:
    def __init__(self, host=None, port=None, user=None, password=None, db=None, debug=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.debug = debug

    def db_obj(self):
        """
        返回db对象
        :return:
        """
        try:
            database_obj = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db)
            return database_obj
        except BaseException as e:
            return '连接数据库参数异常{}'.format(str(e) if self.debug else '')

    def create_data(self, sql=None):
        """
        新增
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                print(sql)
                cur.execute(sql)
                db.commit()
                return 'create success'
        except BaseException as e:
            cur.rollback()
            return 'create:出现错误:{}'.format(str(e) if self.debug else '')

    def read_data(self, sql=None):
        """
        查询(废弃,保留实现思想)(使用: MyPyMysql.select 代替之)
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)  # 执行sql语句
                # sql = "select * from gambler where id='YfpgoLZtEGPfMXUvFPffCi'"

                '''
                获取表结构,并且取出字段,生成列表
                '''
                '''获取字段列表'''
                # print(cur.description)
                key_list = [i[0] for i in cur.description]
                # print(key_list)

                '''
                把查询结果集组装成列表
                '''
                results = cur.fetchall()
                # print(results)
                data_list = [i for i in results]
                # print(data_list)

                data_dict = []
                for field in cur.description:
                    data_dict.append(field[0])
                # print(data_dict)
                # print(len(data_dict))

                '''
                将字段与每一条查询数据合并成键值对,并且组装成新的列表
                new_list = []
                for i in data_list:
                    print(list(i))
                    new_list.append(dict(zip(key_list, list(i))))
                '''
                new_list = [dict(zip(key_list, list(i))) for i in data_list]
                # print(new_list)
                return new_list
        except BaseException as e:
            return 'read:出现错误:{}'.format(str(e) if self.debug else '')

    def update_data(self, sql=None):
        """
        更新
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'update success'
        except BaseException as e:
            cur.rollback()
            return 'update:出现错误:{}'.format(str(e) if self.debug else '')

    def del_data(self, sql=None):
        """
        删除
        :param sql:
        :return:
        """
        try:
            db = self.db_obj()
            with db.cursor() as cur:
                cur.execute(sql)
                db.commit()
                return 'del success'
        except BaseException as e:
            cur.rollback()
            return 'del:出现错误:{}'.format(str(e) if self.debug else '')

    def select(self, sql=None, only=None, size=None):
        """
        查询
        :param sql:
        :param only:
        :param size:
        :return:
        """

        def __func(r):
            if isinstance(r, list):
                new_list = []
                for i in r:
                    new_r = {}
                    for k, v in i.items():
                        if isinstance(v, decimal.Decimal):
                            # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                            v = str(v)
                            v = float(v)
                            new_r[k] = v
                        elif isinstance(v, str):
                            try:
                                new_v = json.loads(v)
                                if isinstance(new_v, list) or isinstance(new_v, dict):
                                    new_r[k] = new_v
                                else:
                                    new_r[k] = v
                            except BaseException as e:
                                new_r[k] = v
                                # print(k, v, type(v))
                                # print("select.__func 异常:{}".format(str(e) if self.debug else ''))
                        elif isinstance(v, datetime):
                            new_r[k] = str(v)
                        else:
                            new_r[k] = v
                    new_list.append(new_r)
                return new_list
            elif isinstance(r, dict):
                new_r = {}
                for k, v in r.items():
                    if isinstance(v, decimal.Decimal):
                        # v = float(decimal.Decimal(v).quantize(decimal.Decimal("0.0")))
                        v = str(v)
                        v = float(v)
                        new_r[k] = v
                    elif isinstance(v, str):
                        try:
                            new_v = json.loads(v)
                            if isinstance(new_v, list) or isinstance(new_v, dict):
                                new_r[k] = new_v
                            else:
                                new_r[k] = v
                        except BaseException as e:
                            new_r[k] = v
                    elif isinstance(v, datetime):
                        new_r[k] = str(v)
                    else:
                        new_r[k] = v
                return new_r
            else:
                pass

        try:
            db = self.db_obj()
            with db.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)  # 执行sql语句
                if only and not size:  # 唯一结果返回 json/dict
                    rs = cur.fetchone()
                    result = __func(rs)
                    return result
                if size and not only:  # 按照需要的长度返回
                    rs = cur.fetchmany(size)
                    result = __func(rs)
                    return result
                else:  # 返回结果集返回 list
                    rs = cur.fetchall()
                    result = __func(rs)
                    return result
        except BaseException as e:
            return 'select:出现错误:{}'.format(str(e) if self.debug else '')


project_db = MyPyMysql(**DB, debug=CONFIG_OBJ.DEBUG)

if __name__ == '__main__':
    from app.models.product.models import Product

    sql = "SELECT * FROM ec_crm_admin;"
    result = project_db.select(sql)
    print(result)
