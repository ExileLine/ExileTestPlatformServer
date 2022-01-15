# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 1:22 下午
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : dingding_api.py
# @Software: PyCharm


from all_reference import *
from app.models.push_reminder.models import DingDingConfModel


class DingDingApi(MethodView):
    """
    钉钉 Api
    GET: 钉钉 push 详情
    POST: 钉钉 push 新增
    PUT: 钉钉 push 编辑
    DELETE: 钉钉 push 删除
    """

    def get(self):
        """钉钉 push 详情"""
        return

    def post(self):
        """钉钉 push 新增"""

        data = request.get_json()
        title = data.get('title')
        ding_talk_url = data.get('ding_talk_url')
        at_mobiles = data.get('at_mobiles', [])
        at_user_ids = data.get('at_user_ids', [])
        is_at_all = data.get('at_user_ids', False)

        if not ding_talk_url:
            return api_result(code=400, message='ding_talk_url 不能为空')

        query_dd = DingDingConfModel.query.filter_by(ding_talk_url=ding_talk_url).first()

        if query_dd:
            return api_result(code=400, message='ding_talk_url 已存在')

        new_dd = DingDingConfModel(
            title=title,
            ding_talk_url=ding_talk_url,
            at_mobiles=at_mobiles,
            at_user_ids=at_user_ids,
            is_at_all=bool(is_at_all),
            creator=g.app_user.username,
            creator_id=g.app_user.id
        )
        new_dd.save()

        return api_result(code=201, message='操作成功')

    def put(self):
        """钉钉 push 编辑"""

        data = request.get_json()
        dd_conf_id = data.get('dd_conf_id')
        title = data.get('title')
        ding_talk_url = data.get('ding_talk_url')
        at_mobiles = data.get('at_mobiles', [])
        at_user_ids = data.get('at_user_ids', [])
        is_at_all = data.get('at_user_ids', False)

        query_dd = DingDingConfModel.query.get(dd_conf_id)

        if not query_dd:
            return api_result(code=400, message='钉钉配置id:{}数据不存在'.format(dd_conf_id))

        if query_dd.ding_talk_url != ding_talk_url:
            if DingDingConfModel.query.filter_by(ding_talk_url=ding_talk_url).all():
                return api_result(code=400, message='ding_talk_url:{} 已经存在'.format(ding_talk_url))

        query_dd.title = title
        query_dd.ding_talk_url = ding_talk_url
        query_dd.at_mobiles = at_mobiles
        query_dd.at_user_ids = at_user_ids
        query_dd.is_at_all = bool(is_at_all)
        query_dd.modifier = g.app_user.username
        query_dd.modifier_id = g.app_user.id
        db.session.commit()

        return api_result(code=203, message='编辑成功')

    def delete(self):
        """钉钉 push 删除"""

        data = request.get_json()
        dd_conf_id = data.get('dd_conf_id')

        query_dd = DingDingConfModel.query.get(dd_conf_id)

        if not query_dd:
            return api_result(code=400, message='钉钉配置id:{}数据不存在'.format(dd_conf_id))

        query_dd.modifier = g.app_user.username
        query_dd.modifier_id = g.app_user.id
        query_dd.delete()
        return api_result(code=204, message='删除成功')


class DingDingPushPageApi(MethodView):
    """
    钉钉 push page api
    POST: 钉钉 push 分页模糊查询
    """

    def post(self):
        """钉钉 push 分页模糊查询"""

        data = request.get_json()
        dd_conf_id = data.get('dd_conf_id')
        title = data.get('title')
        ding_talk_url = data.get('ding_talk_url')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ding_ding_conf  
        WHERE 
        id LIKE"%%" 
        and title LIKE"%B1%" 
        and ding_talk_url LIKE"%B1%" 
        and is_deleted=0
        ORDER BY create_timestamp LIMIT 0,20;
        """

        result_data = general_query(
            model=DingDingConfModel,
            field_list=['id', 'title', 'ding_talk_url'],
            query_list=[dd_conf_id, title, ding_talk_url],
            is_deleted=False,
            page=page,
            size=size
        )

        return api_result(code=200, message='操作成功', data=result_data)
