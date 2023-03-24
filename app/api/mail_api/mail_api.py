# -*- coding: utf-8 -*-
# @Time    : 2022/1/9 1:17 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : mail_api.py
# @Software: PyCharm

from all_reference import *
from app.models.push_reminder.models import MailConfModel


class MailApi(MethodView):
    """
    邮箱Api
    GET: 邮箱详情
    POST: 邮件新增
    PUT: 邮件编辑
    DELETE: 邮件删除
    """

    def get(self):
        """邮箱详情"""

        return

    def post(self):
        """邮箱新增"""

        data = request.get_json()
        mail_list = data.get('mail_list', [])
        if not mail_list:
            return api_result(code=NO_DATA, message='不能为空')

        for mail in mail_list:
            current_mail = mail.get('mail')
            current_mail_user = mail.get('mail_user')
            if "@" not in current_mail:
                return api_result(code=BUSINESS_ERROR, message=f'{current_mail}:邮箱格式错误')

            query_mail = MailConfModel.query.filter_by(mail=current_mail, is_deleted=0).first()
            if query_mail:
                return api_result(code=UNIQUE_ERROR, message=f'{current_mail}:已经存在')

            new_mail = MailConfModel(
                mail=current_mail,
                mail_user=current_mail_user,
                creator=g.app_user.username,
                creator_id=g.app_user.id
            )
            db.session.add(new_mail)
        db.session.commit()
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE)

    def put(self):
        """邮箱编辑"""

        data = request.get_json()
        mail_id = data.get('id')
        mail = data.get('mail')
        mail_user = data.get('mail_user')
        is_deleted = data.get('is_deleted', False)

        query_mail = MailConfModel.query.get(mail_id)
        if not query_mail:
            return api_result(code=NO_DATA, message=f'邮箱id: {mail_id} 不存在')

        if query_mail.mail != mail:
            if MailConfModel.query.filter_by(mail=mail).all():
                return api_result(code=UNIQUE_ERROR, message=f'邮箱: {mail} 已经存在')

        query_mail.mail = mail
        query_mail.mail_user = mail_user
        query_mail.modifier = g.app_user.username
        query_mail.modifier_id = g.app_user.id
        query_mail.is_deleted = is_deleted
        db.session.commit()
        return api_result(code=PUT_SUCCESS, message=PUT_MESSAGE)

    def delete(self):
        """邮箱删除"""

        data = request.get_json()
        mail_id = data.get('id')

        query_mail = MailConfModel.query.get(mail_id)
        if not query_mail:
            return api_result(code=NO_DATA, message=f'邮箱id: {mail_id}  不存在')

        query_mail.modifier = g.app_user.username
        query_mail.modifier_id = g.app_user.id
        query_mail.delete()
        return api_result(code=DEL_SUCCESS, message=DEL_MESSAGE)


class MailPageApi(MethodView):
    """
    mail page api
    POST: 邮箱分页模糊查询
    """

    def post(self):
        """邮箱分页模糊查询"""

        data = request.get_json()
        mail_id = data.get('mail_id')
        mail = data.get('mail')
        mail_user = data.get('mail_user')
        is_deleted = data.get('is_deleted', 0)
        creator_id = data.get('creator_id')
        page = data.get('page')
        size = data.get('size')

        sql = """
        SELECT * 
        FROM exile_mail_conf  
        WHERE 
        id = "id" 
        and mail LIKE"%B1%" 
        and mail_user LIKE"%B1%" 
        ORDER BY create_timestamp LIMIT 0,20;
        """

        where_dict = {
            "id": mail_id,
            "is_deleted": is_deleted,
            "creator_id": creator_id
        }

        result_data = general_query(
            model=MailConfModel,
            field_list=['mail', 'mail_user'],
            query_list=[mail, mail_user],
            where_dict=where_dict,
            page=page,
            size=size
        )
        return api_result(code=POST_SUCCESS, message=SUCCESS_MESSAGE, data=result_data)
