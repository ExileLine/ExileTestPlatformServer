# -*- coding: utf-8 -*-
# @Time    : 2022/2/16 9:49 上午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : models.py
# @Software: PyCharm


from common.libs.BaseModel import *


class TestProject(BaseModel):
    __tablename__ = 'exile5_test_project'
    __table_args__ = {'comment': '项目表'}

    project_name = db.Column(db.String(128), nullable=False, unique=True, comment='项目名称')
    project_auth = db.Column(db.JSON, default=0, comment='是否公开:1-是;0-否')
    project_user = db.Column(db.JSON, default=[], comment='项目用户:project_auth为是的情况下使用')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestProject 模型对象-> ID:{} 项目名称:{}'.format(self.id, self.project_name)


class TestProjectVersion(BaseModel):
    __tablename__ = 'exile5_test_project_version'
    __table_args__ = {'comment': '项目版本迭代表'}

    version_name = db.Column(db.String(128), nullable=False, comment='版本名称')
    version_number = db.Column(db.String(32), nullable=False, comment='版本号')
    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    icon = db.Column(db.String(1024), comment='Icon')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestProjectVersion 模型对象-> ID:{} 版本名称:{} 版本号:{}'.format(self.id, self.version_name, self.version_number)


class TestVersionTask(BaseModel):
    __tablename__ = 'exile5_test_version_task'
    __table_args__ = {'comment': '版本迭代任务表'}

    version_id = db.Column(BIGINT(20, unsigned=True), comment='版本迭代id(冗余字段)')
    task_name = db.Column(db.String(128), nullable=False, comment='任务名称')
    task_type = db.Column(db.String(128), nullable=False, comment='任务类型')
    user_list = db.Column(db.JSON, comment='参与人员')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestVersionTask 模型对象-> ID:{} 任务名称:{} 任务类型:{}'.format(self.id, self.task_name, self.task_type)


class TestModuleApp(BaseModel):
    __tablename__ = 'exile5_test_module_app'
    __table_args__ = {'comment': '功能模块与应用'}

    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    module_name = db.Column(db.String(128), nullable=False, comment='模块应用名称')
    module_type = db.Column(db.String(128), default="默认", comment='模块应用名称类型(暂时未用上)')
    module_code = db.Column(db.String(128), unique=True, comment='模块应用名称类型')
    module_source = db.Column(db.String(512), comment='模块应用来源')
    case_list = db.Column(db.JSON, comment='用例id列表')
    scenario_list = db.Column(db.JSON, comment='场景id列表')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'TestModuleApp 模型对象-> ID:{} 模块应用名称:{} 类型:{}'.format(
            self.id, self.module_name, self.module_type
        )


class MidProjectAndCase(BaseModel):
    __tablename__ = 'exile5_test_mid_project_case'
    __table_args__ = (
        db.Index('idx_project_case', 'project_id', 'case_id'),
        {'comment': '项目-用例中间表'}
    )
    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidProjectAndCase 模型对象-> ID:{} 项目id:{} 用例id:{}'.format(
            self.id, self.project_id, self.case_id
        )


class MidVersionCase(BaseModel):
    __tablename__ = 'exile5_test_mid_version_case'
    __table_args__ = (
        db.Index('idx_version_case', 'version_id', 'case_id'),
        {'comment': '版本迭代-用例中间表'}
    )
    version_id = db.Column(BIGINT(20, unsigned=True), comment='迭代id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidVersionCase 模型对象-> ID:{} 迭代id:{} 用例id:{}'.format(
            self.id, self.version_id, self.case_id
        )


class MidTaskCase(BaseModel):
    __tablename__ = 'exile5_test_mid_task_case'
    __table_args__ = (
        db.Index('idx_task_case', 'task_id', 'case_id'),
        {'comment': '任务-用例中间表'}
    )
    task_id = db.Column(BIGINT(20, unsigned=True), comment='任务id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidTaskCase 模型对象-> ID:{} 任务id:{} 用例id:{}'.format(
            self.id, self.task_id, self.case_id
        )


class MidModuleCase(BaseModel):
    __tablename__ = 'exile5_test_mid_module_case'
    __table_args__ = (
        db.Index('idx_module_case', 'module_id', 'case_id'),
        {'comment': '模块-用例中间表'}
    )
    module_id = db.Column(BIGINT(20, unsigned=True), comment='模块id')
    case_id = db.Column(BIGINT(20, unsigned=True), comment='用例id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidModuleCase 模型对象-> ID:{} 模块id:{} 用例id:{}'.format(
            self.id, self.module_id, self.case_id
        )


class MidProjectScenario(BaseModel):
    __tablename__ = 'exile5_test_mid_project_scenario'
    __table_args__ = (
        db.Index('idx_project_scenario', 'project_id', 'scenario_id'),
        {'comment': '项目-场景中间表'}
    )
    project_id = db.Column(BIGINT(20, unsigned=True), comment='项目id')
    scenario_id = db.Column(BIGINT(20, unsigned=True), comment='场景id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidProjectScenario 模型对象-> ID:{} 项目id:{} 场景id:{}'.format(
            self.id, self.project_id, self.scenario_id
        )


class MidVersionScenario(BaseModel):
    __tablename__ = 'exile5_test_mid_version_scenario'
    __table_args__ = (
        db.Index('idx_version_scenario', 'version_id', 'scenario_id'),
        {'comment': '版本迭代-场景中间表'}
    )
    version_id = db.Column(BIGINT(20, unsigned=True), comment='迭代id')
    scenario_id = db.Column(BIGINT(20, unsigned=True), comment='场景id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidVersionScenario 模型对象-> ID:{} 迭代id:{} 场景id:{}'.format(
            self.id, self.version_id, self.scenario_id
        )


class MidTaskScenario(BaseModel):
    __tablename__ = 'exile5_test_mid_task_scenario'
    __table_args__ = (
        db.Index('idx_task_scenario', 'task_id', 'scenario_id'),
        {'comment': '任务-用例中间表'}
    )
    task_id = db.Column(BIGINT(20, unsigned=True), comment='任务id')
    scenario_id = db.Column(BIGINT(20, unsigned=True), comment='场景id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidTaskScenario 模型对象-> ID:{} 任务id:{} 场景id:{}'.format(
            self.id, self.task_id, self.scenario_id
        )


class MidModuleScenario(BaseModel):
    __tablename__ = 'exile5_test_mid_module_scenario'
    __table_args__ = (
        db.Index('idx_module_scenario', 'module_id', 'scenario_id'),
        {'comment': '模块-用例中间表'}
    )
    module_id = db.Column(BIGINT(20, unsigned=True), comment='模块id')
    scenario_id = db.Column(BIGINT(20, unsigned=True), comment='场景id')
    creator = db.Column(db.String(32), comment='创建人')
    creator_id = db.Column(BIGINT(20, unsigned=True), comment='创建人id')
    modifier = db.Column(db.String(32), comment='更新人')
    modifier_id = db.Column(BIGINT(20, unsigned=True), comment='更新人id')
    remark = db.Column(db.String(255), comment='备注')

    def __repr__(self):
        return 'MidModuleScenario 模型对象-> ID:{} 模块id:{} 场景id:{}'.format(
            self.id, self.module_id, self.scenario_id
        )
