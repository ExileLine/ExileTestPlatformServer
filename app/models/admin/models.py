# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 下午4:32
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : manage.py
# @Software: PyCharm

from werkzeug.security import generate_password_hash, check_password_hash

from common.libs.BaseModel import *


class Admin(BaseModel):
    __tablename__ = 'exile_auth_admin'
    __table_args__ = {'comment': '后台用户表'}
    username = db.Column(db.String(32), nullable=False, unique=True, comment='用户名称(账号)')
    nickname = db.Column(db.String(32), comment='用户昵称')
    _password = db.Column(db.String(256), nullable=False, comment='用户密码')
    phone = db.Column(db.String(64), unique=True, comment='手机号')
    mail = db.Column(db.String(128), comment='邮箱')
    code = db.Column(db.String(64), unique=True, comment='用户编号')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    def __repr__(self):
        return 'Admin 模型对象-> ID:{} 用户名:{}'.format(self.id, self.username)


class Role(BaseModel):
    __tablename__ = 'exile_auth_role'
    __table_args__ = {'comment': '后台角色表'}
    name = db.Column(db.String(50), nullable=False, comment='角色名称')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'Role 模型对象-> ID:{} 角色名称:{}'.format(self.id, self.name)


class Permission(BaseModel):
    __tablename__ = 'exile_auth_permission'
    __table_args__ = {'comment': '后台权限表'}
    name = db.Column(db.String(50), nullable=False, comment='权限名称')
    resource_id = db.Column(BIGINT(20, unsigned=True), comment='ServerApi或WebRoute对应ec_crm_resource表')
    resource_type = db.Column(db.String(32), comment='SERVER_API-接口;WEB_ROUTE-页面路由')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def get_all_resource(self):
        """
        获取权限下所有资源
        :return:
        """
        return

    def __repr__(self):
        return 'Permission 模型对象-> ID:{} 权限名称:{}'.format(self.id, self.name)


class MidAdminAndRole(BaseModel):
    __tablename__ = 'exile_auth_mid_admin_role'
    __table_args__ = (
        db.Index('idx_admin_role', 'admin_id', 'role_id', 'is_deleted'),
        {'comment': '用户角色中间表'}
    )
    admin_id = db.Column(BIGINT(20, unsigned=True), comment='后台用户id')
    role_id = db.Column(BIGINT(20, unsigned=True), comment='后台用户id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')

    def __repr__(self):
        return 'MidAdminAndRole 模型对象-> ID:{} 用户id:{} 角色id:{}'.format(self.id, self.admin_id, self.role_id)


class MidPermissionAndRole(BaseModel):
    __tablename__ = 'exile_auth_mid_permission_role'
    __table_args__ = (
        db.Index('idx_role_permission', 'role_id', 'permission_id', 'is_deleted'),
        {'comment': '权限角色中间表'}
    )
    permission_id = db.Column(BIGINT(20, unsigned=True), comment='后台用户id')
    role_id = db.Column(BIGINT(20, unsigned=True), comment='后台用户id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')

    def __repr__(self):
        return 'MidPermissionAndRole 模型对象-> ID:{} 角色id:{} 权限id:{}'.format(self.id, self.role_id, self.permission_id)


class ApiResource(BaseModel):
    __tablename__ = 'exile_auth_api_resource'
    __table_args__ = {'comment': 'Api资源表'}
    name = db.Column(db.String(64), nullable=False, comment='Api名称')
    url = db.Column(db.String(128), comment='接口地址')
    uri = db.Column(db.String(128), comment='参数:如 /api/{id};备用字段')
    is_url_var = db.Column(TINYINT(1, unsigned=True), server_default=text('0'), comment='url是否拼接参数:如 /api/{id};0-否;1-是')
    method = db.Column(db.String(128), comment='Https Method 1-GET;2-POST;3-PUT;4-DELETE;5-PATCH')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'ApiResource 模型对象-> ID:{} Api名称:{}'.format(self.id, self.name)


class RouteResource(BaseModel):
    __tablename__ = 'exile_auth_route_resource'
    __table_args__ = {'comment': 'Route资源表'}
    name = db.Column(db.String(50), nullable=False, comment='资源名称')
    code = db.Column(db.String(64), comment='路由编码')
    component = db.Column(db.String(64), comment='组件名')
    pid = db.Column(db.Integer, comment='父级路由id')
    level_path = db.Column(db.JSON, comment='路由层级路径;例如:[0,1,2]代表该菜单是三级路由,上级路由的id是1,再上级的路由id是0')
    level = db.Column(db.Integer, comment='路由层级')
    path = db.Column(db.String(128), comment='uri')
    path_type = db.Column(TINYINT(1, unsigned=True), server_default=text('1'), comment='1-Api;2-Route')
    icon = db.Column(db.String(64), comment='图标')
    sequence = db.Column(db.Integer, comment='排列顺序')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'RouteResource 模型对象-> ID:{} Route名称:{}'.format(self.id, self.name)
