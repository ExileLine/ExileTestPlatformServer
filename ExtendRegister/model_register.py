# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 3:08 下午
# @Author  : yangyuexiong
# @Email   : yang6333yyx@126.com
# @File    : model_register.py
# @Software: PyCharm


from app.models.admin.models import Admin
from app.models.platform_conf.models import PlatformConfModel
from app.models.test_project.models import (
    TestProject, TestProjectVersion, TestVersionTask, TestModuleApp,
    MidProjectAndCase, MidVersionCase, MidTaskCase, MidModuleCase,
    MidProjectScenario, MidVersionScenario, MidTaskScenario, MidModuleScenario,
    MidProjectAndUiCase, MidVersionUiCase, MidTaskUiCase, MidModuleUiCase,
)
from app.models.test_case.models import TestCase, TestCaseData
from app.models.test_case_assert.models import TestCaseAssertion, TestCaseAssResponse, TestCaseAssField, \
    TestCaseDataAssBind
from app.models.test_case_scenario.models import TestCaseScenario
from app.models.test_variable.models import TestVariable
from app.models.test_logs.models import TestLogs, TestExecuteLogs
from app.models.test_case_set.models import TestCaseSet
from app.models.test_env.models import TestEnv
from app.models.test_case_db.models import TestDatabases
from app.models.push_reminder.models import MailConfModel, DingDingConfModel
from app.models.timed_task.models import TimedTaskModel
from app.models.file_import.models import FileImportHistory
from app.models.test_cicd.models import TestCiCdMap
from app.models.ui_test_case.models import UiTestCase
