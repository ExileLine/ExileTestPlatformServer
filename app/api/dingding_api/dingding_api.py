# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 1:22 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : dingding_api.py
# @Software: PyCharm


from all_reference import *
from app.models.push_reminder.models import DingDingConfModel


class DingDingPushConfApi(MethodView):
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
        is_at_all = data.get('is_at_all', False)
        remark = data.get('remark')

        if not ding_talk_url:
            return api_result(code=NO_DATA, message='ding_talk_url 不能为空')

        query_dd = DingDingConfModel.query.filter_by(ding_talk_url=ding_talk_url).first()

        if query_dd:
            return api_result(code=UNIQUE_ERROR, message=f'ding_talk_url: {ding_talk_url} 已存在')

        new_dd = DingDingConfModel(
            title=title,
            ding_talk_url=ding_talk_url,
            at_mobiles=at_mobiles,
            at_user_ids=at_user_ids,
            is_at_all=is_at_all,
            creator=g.app_user.username,
            creator_id=g.app_user.id,
            remark=remark
        )
        new_dd.save()

        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE)

    def put(self):
        """钉钉 push 编辑"""

        data = request.get_json()
        dd_conf_id = data.get('id')
        title = data.get('title')
        ding_talk_url = data.get('ding_talk_url')
        at_mobiles = data.get('at_mobiles', [])
        at_user_ids = data.get('at_user_ids', [])
        is_at_all = data.get('is_at_all', False)
        is_enable = data.get('is_enable', True)
        remark = data.get('remark')

        query_dd = DingDingConfModel.query.get(dd_conf_id)

        if not query_dd:
            return api_result(code=NO_DATA, message=f'钉钉配置id: {dd_conf_id} 不存在')

        if query_dd.ding_talk_url != ding_talk_url:
            if DingDingConfModel.query.filter_by(ding_talk_url=ding_talk_url).all():
                return api_result(code=UNIQUE_ERROR, message=f'ding_talk_url: {ding_talk_url} 已存在')

        query_dd.title = title
        query_dd.ding_talk_url = ding_talk_url
        query_dd.at_mobiles = at_mobiles
        query_dd.at_user_ids = at_user_ids
        query_dd.is_at_all = is_at_all
        query_dd.modifier = g.app_user.username
        query_dd.modifier_id = g.app_user.id
        query_dd.status = is_enable
        query_dd.remark = remark
        db.session.commit()

        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """钉钉 push 删除"""

        data = request.get_json()
        dd_conf_id = data.get('id')

        query_dd = DingDingConfModel.query.get(dd_conf_id)
        if not query_dd:
            return api_result(code=NO_DATA, message=f'钉钉配置id: {dd_conf_id} 不存在')

        query_dd.modifier = g.app_user.username
        query_dd.modifier_id = g.app_user.id
        query_dd.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class DingDingPushConfPageApi(MethodView):
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
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_ding_ding_conf  
        WHERE 
        id = "id" 
        and title LIKE"%B1%" 
        and ding_talk_url LIKE"%B1%" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": dd_conf_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=DingDingConfModel,
            field_list=['title', 'ding_talk_url'],
            query_list=[title, ding_talk_url],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
