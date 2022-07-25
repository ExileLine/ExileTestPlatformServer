# -*- coding: utf-8 -*-
# @Time    : 2022/4/7 11:44 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : safe_scan_conf_api.py
# @Software: PyCharm

from all_reference import *
from app.models.safe_scan_conf.models import SafeScanConf


class SafeScanConfApi(MethodView):
    """
    安全扫描Api
    GET: 获取安全扫描配置
    POST: 新增安全扫描配置
    PUT: 编辑安全扫描配置
    DELETE: 禁用安全扫描配置
    """

    def get(self, safe_id):
        """获取安全扫描配置"""

        query_safe_scan = SafeScanConf.query.get(safe_id)
        if not query_safe_scan:
            return api_result(code=400, message=f'安全扫描配置:{safe_id}不存在')
        return api_result(code=200, message='操作成功', data=query_safe_scan.to_json())

    def post(self):
        """新增安全扫描配置"""

        data = request.get_json()
        description = data.get('description').strip()
        is_global_open = data.get('is_global_open', False)
        safe_scan_url = data.get('safe_scan_url').strip()
        weights = data.get('weights', 0)
        remark = data.get('remark')

        if not description:
            return api_result(code=400, message='描述不能为空')

        if not safe_scan_url:
            return api_result(code=400, message='安全代理url不能为空')

        query_safe_scan = SafeScanConf.query.filter(
            or_(SafeScanConf.safe_scan_url == safe_scan_url, SafeScanConf.weights == weights)).all()

        if query_safe_scan:
            return api_result(code=400, message=f'{safe_scan_url} 已存在，或权重：{weights} 不唯一')

        new_safe_scan = SafeScanConf(
            description=description,
            is_global_open=bool(is_global_open),
            safe_scan_url=safe_scan_url,
            weights=weights,
            remark=remark,
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )

        new_safe_scan.save()
        return api_result(code=201, message='操作成功')

    def put(self):
        """编辑安全扫描配置"""

        data = request.get_json()
        safe_id = data.get('id')
        description = data.get('description').strip()
        is_global_open = data.get('is_global_open', False)
        safe_scan_url = data.get('safe_scan_url').strip()
        weights = data.get('weights', 0)
        remark = data.get('remark')
        is_deleted = data.get('is_deleted', 0)

        if not description:
            return api_result(code=400, message='描述不能为空')

        if not safe_scan_url:
            return api_result(code=400, message='安全代理url不能为空')

        query_safe_scan = SafeScanConf.query.get(safe_id)

        if not query_safe_scan:
            return api_result(code=400, message=f'安全扫描配置:{safe_id}不存在')

        if query_safe_scan.safe_scan_url != safe_scan_url:
            if SafeScanConf.query.filter_by(safe_scan_url=safe_scan_url).all():
                return api_result(code=400, message=f'安全代理url: {safe_scan_url} 已经存在')
        if query_safe_scan.weights != weights:
            if SafeScanConf.query.filter_by(weights=weights).all():
                return api_result(code=400, message=f'权重: {weights} 已经存在')

        query_safe_scan.description = description
        query_safe_scan.is_global_open = is_global_open
        query_safe_scan.safe_scan_url = safe_scan_url
        query_safe_scan.weights = weights
        query_safe_scan.remark = remark
        query_safe_scan.is_deleted = is_deleted
        query_safe_scan.modifier = g.app_user.username
        query_safe_scan.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """禁用安全扫描配置"""

        data = request.get_json()
        safe_id = data.get('id')

        query_safe_scan = SafeScanConf.query.get(safe_id)

        if not query_safe_scan:
            return api_result(code=400, message=f'安全扫描配置:{safe_id}不存在')

        query_safe_scan.modifier = g.app_user.username
        query_safe_scan.modifier_id = g.app_user.id
        query_safe_scan.delete()
        return api_result(code=204, message='删除成功')


class SafeScanConfPageApi(MethodView):
    """
    安全扫描配置 page api
    POST: 安全扫描配置分页模糊查询
    """

    def post(self):
        """安全扫描配置分页模糊查询"""

        data = request.get_json()
        safe_id = data.get('id')
        description = data.get('description')
        safe_scan_url = data.get('safe_scan_url')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_safe_scan_conf  
        WHERE 
        id = "id" 
        and description LIKE"%B1%" 
        and safe_scan_url LIKE"%B1%" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": safe_id
        }

        result_data = general_query(
            model=SafeScanConf,
            field_list=['description', 'safe_scan_url'],
            query_list=[description, safe_scan_url],
            where_dict=where_dict,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)
