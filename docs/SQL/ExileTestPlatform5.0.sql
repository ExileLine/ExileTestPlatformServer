-- -------------------------------------------------------------
-- TablePlus 2.8.2(257)
--
-- https://tableplus.com/
--
-- Database: ExileTestPlatform5.0
-- Generation Time: 2023-04-21 16:01:43.7980
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE `exile5_ass_bind` (
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `data_id` bigint(20) unsigned DEFAULT NULL COMMENT '数据id',
  `is_base` tinyint(1) unsigned DEFAULT NULL COMMENT '基础数据',
  `ass_resp_id_list` json DEFAULT NULL COMMENT 'resp断言规则list',
  `ass_field_id_list` json DEFAULT NULL COMMENT 'field断言规则list',
  `index` bigint(20) unsigned DEFAULT NULL COMMENT '排序',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_case_data` (`case_id`,`data_id`,`is_deleted`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用例断言关系绑定';

CREATE TABLE `exile5_auth_admin` (
  `username` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '用户名称(账号)',
  `nickname` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户昵称',
  `_password` varchar(256) COLLATE utf8mb4_bin NOT NULL COMMENT '用户密码',
  `phone` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '手机号',
  `mail` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮箱',
  `code` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户编号',
  `seat` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '座位',
  `department` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '部门',
  `position` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '职位',
  `superior` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上级',
  `login_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '登录类型:single;many',
  `is_tourist` tinyint(1) unsigned DEFAULT NULL COMMENT '0-游客账户;1-非游客账户',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `mail` (`mail`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台用户表';

CREATE TABLE `exile5_auth_api_resource` (
  `name` varchar(64) COLLATE utf8mb4_bin NOT NULL COMMENT 'Api名称',
  `url` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '接口地址',
  `uri` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '参数:如 /api/{id};备用字段',
  `is_url_var` tinyint(1) unsigned DEFAULT '0' COMMENT 'url是否拼接参数:如 /api/{id};0-否;1-是',
  `method` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Https Method 1-GET;2-POST;3-PUT;4-DELETE;5-PATCH',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Api资源表';

CREATE TABLE `exile5_auth_mid_admin_role` (
  `admin_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `role_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_admin_role` (`admin_id`,`role_id`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户角色中间表';

CREATE TABLE `exile5_auth_mid_permission_role` (
  `permission_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `role_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_role_permission` (`role_id`,`permission_id`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='权限角色中间表';

CREATE TABLE `exile5_auth_permission` (
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '权限名称',
  `resource_id` bigint(20) unsigned DEFAULT NULL COMMENT 'ServerApi或WebRoute对应ec_crm_resource表',
  `resource_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'SERVER_API-接口;WEB_ROUTE-页面路由',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台权限表';

CREATE TABLE `exile5_auth_role` (
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '角色名称',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台角色表';

CREATE TABLE `exile5_auth_route_resource` (
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '资源名称',
  `code` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '路由编码',
  `component` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '组件名',
  `pid` int(11) DEFAULT NULL COMMENT '父级路由id',
  `level_path` json DEFAULT NULL COMMENT '路由层级路径;例如:[0,1,2]代表该菜单是三级路由,上级路由的id是1,再上级的路由id是0',
  `level` int(11) DEFAULT NULL COMMENT '路由层级',
  `path` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'uri',
  `path_type` tinyint(1) unsigned DEFAULT '1' COMMENT '1-Api;2-Route',
  `icon` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '图标',
  `sequence` int(11) DEFAULT NULL COMMENT '排列顺序',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Route资源表';

CREATE TABLE `exile5_case_assertion` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `assert_description` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '断言描述',
  `ass_json` json DEFAULT NULL COMMENT '断言',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `assertion_type` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '断言类型:response;field',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='断言规则';

CREATE TABLE `exile5_cicd_map` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '平台项目id',
  `project_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '项目名',
  `app_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '应用名',
  `branch_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '分支名称',
  `mirror` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '镜像',
  `url` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'URL',
  `obj_json` json DEFAULT NULL COMMENT '整个json',
  `version_id` bigint(20) unsigned DEFAULT NULL COMMENT '平台版本id',
  `task_id` bigint(20) unsigned DEFAULT NULL COMMENT '平台任务id',
  `dd_push_id` bigint(20) unsigned DEFAULT NULL COMMENT '平台钉钉推送id',
  `is_set_url` bigint(20) unsigned DEFAULT NULL COMMENT '是否使用cicd的url',
  `is_active` bigint(20) unsigned DEFAULT NULL COMMENT '是否激活',
  `scheduling_id` bigint(20) unsigned DEFAULT NULL COMMENT 'ui auto scheduling_id',
  `is_safe_scan` bigint(20) unsigned DEFAULT NULL COMMENT '是否安全扫描',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='CICD映射表';

CREATE TABLE `exile5_ding_ding_conf` (
  `title` varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标题描述(机器人名称)',
  `ding_talk_url` varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'DING_TALK_URL',
  `at_mobiles` json DEFAULT NULL COMMENT 'AT_MOBILES',
  `at_user_ids` json DEFAULT NULL COMMENT 'AT_USER_IDS',
  `is_at_all` int(11) DEFAULT NULL COMMENT 'IS_AT_ALL',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='钉钉推送配置表';

CREATE TABLE `exile5_ding_ding_push_logs` (
  `send_message` text COLLATE utf8mb4_bin COMMENT '推送信息',
  `error_info` text COLLATE utf8mb4_bin COMMENT '错误堆栈信息',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='钉钉推送记录表';

CREATE TABLE `exile5_file_import_history` (
  `file_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '文件名称',
  `file_type` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '文件类型',
  `file_main_content` json NOT NULL COMMENT '文件主要内容',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='接口导入记录表';

CREATE TABLE `exile5_mail_conf` (
  `mail` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮箱',
  `mail_user` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮箱用户',
  `is_send` tinyint(1) unsigned DEFAULT NULL COMMENT '是否为发送账号',
  `send_pwd` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '发件邮箱的授权码',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='邮件推送配置表';

CREATE TABLE `exile5_test_case` (
  `case_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用例名称',
  `request_method` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '请求方式:GET;POST;PUT;DELETE...',
  `request_base_url` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '请求BaseUrl',
  `request_url` varchar(2048) COLLATE utf8mb4_bin NOT NULL COMMENT '请求URL',
  `case_status` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用例周期状态:active;dev;debug;over',
  `is_pass` tinyint(1) unsigned DEFAULT NULL COMMENT '0-不跳过;1-跳过',
  `is_shared` tinyint(1) unsigned DEFAULT NULL COMMENT '0-仅创建者执行;1-共享执行',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `is_copy` tinyint(1) unsigned DEFAULT NULL COMMENT '是否复制生成:0-否;1-是',
  `total_execution` bigint(20) unsigned DEFAULT NULL COMMENT '执行次数总计',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例';

CREATE TABLE `exile5_test_case_data` (
  `data_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '数据名称',
  `request_params` json DEFAULT NULL COMMENT 'params',
  `request_params_hash` json DEFAULT NULL COMMENT 'params hash',
  `request_headers` json DEFAULT NULL COMMENT 'headers',
  `request_headers_hash` json DEFAULT NULL COMMENT 'headers hash',
  `request_body` json DEFAULT NULL COMMENT 'body',
  `request_body_hash` json DEFAULT NULL COMMENT 'body hash',
  `request_body_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'none;form-data;x-form-data;json;text;html;xml',
  `use_var_list` json DEFAULT NULL COMMENT '引用变量列表',
  `update_var_list` json DEFAULT NULL COMMENT '更新变量列表',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `is_before` tinyint(1) unsigned DEFAULT NULL COMMENT '是否使用前置条件 0-否;1-是',
  `data_before` json DEFAULT NULL COMMENT '前置条件',
  `is_after` tinyint(1) unsigned DEFAULT NULL COMMENT '是否使用后置条件 0-否;1-是',
  `data_after` json DEFAULT NULL COMMENT '后置条件',
  `md5` varchar(512) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'md5',
  `data_size` bigint(20) unsigned DEFAULT NULL COMMENT '参数字节数',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例参数';

CREATE TABLE `exile5_test_case_scenario` (
  `scenario_title` varchar(256) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '场景标题',
  `case_list` json DEFAULT NULL COMMENT '用例id列表按传参排序:[1,3,7,2...]',
  `is_shared` tinyint(1) unsigned DEFAULT NULL COMMENT '0-仅创建者执行;1-共享执行',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `total_execution` bigint(20) unsigned DEFAULT NULL COMMENT '执行次数总计',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例场景';

CREATE TABLE `exile5_test_databases` (
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '名称',
  `db_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '库类型',
  `db_connection` json DEFAULT NULL COMMENT '连接方式:直连,ssh,vpn...',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例-databases';

CREATE TABLE `exile5_test_env` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `env_url` varchar(2048) COLLATE utf8mb4_bin NOT NULL COMMENT '环境url',
  `env_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '环境名称',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试环境';

CREATE TABLE `exile5_test_execute_logs` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `execute_id` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用例id/场景id/module_code',
  `execute_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用例名称/场景名称',
  `execute_key` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '执行标识',
  `execute_type` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '执行类型',
  `redis_key` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT 'Redis的key',
  `report_url` varchar(1024) COLLATE utf8mb4_bin NOT NULL COMMENT '报告地址',
  `file_name` varchar(1024) COLLATE utf8mb4_bin NOT NULL COMMENT '文件名称带后缀如: xxx.html',
  `trigger_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '触发类型:user_execute;timed_execute',
  `execute_status` tinyint(1) unsigned DEFAULT NULL COMMENT '执行状态',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用例执行记录表';

CREATE TABLE `exile5_test_mid_module_case` (
  `module_id` bigint(20) unsigned DEFAULT NULL COMMENT '模块id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_module_case` (`module_id`,`case_id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='模块-用例中间表';

CREATE TABLE `exile5_test_mid_module_scenario` (
  `module_id` bigint(20) unsigned DEFAULT NULL COMMENT '模块id',
  `scenario_id` bigint(20) unsigned DEFAULT NULL COMMENT '场景id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_module_scenario` (`module_id`,`scenario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='模块-用例中间表';

CREATE TABLE `exile5_test_mid_module_ui_case` (
  `module_id` bigint(20) unsigned DEFAULT NULL COMMENT '模块id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_module_ui_case` (`module_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='模块-UI用例中间表';

CREATE TABLE `exile5_test_mid_project_case` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_project_case` (`project_id`,`case_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目-用例中间表';

CREATE TABLE `exile5_test_mid_project_scenario` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `scenario_id` bigint(20) unsigned DEFAULT NULL COMMENT '场景id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_project_scenario` (`project_id`,`scenario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目-场景中间表';

CREATE TABLE `exile5_test_mid_project_ui_case` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_project_ui_case` (`project_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目-UI用例中间表';

CREATE TABLE `exile5_test_mid_task_case` (
  `task_id` bigint(20) unsigned DEFAULT NULL COMMENT '任务id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_task_case` (`task_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='任务-用例中间表';

CREATE TABLE `exile5_test_mid_task_scenario` (
  `task_id` bigint(20) unsigned DEFAULT NULL COMMENT '任务id',
  `scenario_id` bigint(20) unsigned DEFAULT NULL COMMENT '场景id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_task_scenario` (`task_id`,`scenario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='任务-用例中间表';

CREATE TABLE `exile5_test_mid_task_ui_case` (
  `task_id` bigint(20) unsigned DEFAULT NULL COMMENT '任务id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_task_ui_case` (`task_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='任务-UI用例中间表';

CREATE TABLE `exile5_test_mid_version_case` (
  `version_id` bigint(20) unsigned DEFAULT NULL COMMENT '迭代id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_version_case` (`version_id`,`case_id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='版本迭代-用例中间表';

CREATE TABLE `exile5_test_mid_version_scenario` (
  `version_id` bigint(20) unsigned DEFAULT NULL COMMENT '迭代id',
  `scenario_id` bigint(20) unsigned DEFAULT NULL COMMENT '场景id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_version_scenario` (`version_id`,`scenario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='版本迭代-场景中间表';

CREATE TABLE `exile5_test_mid_version_ui_case` (
  `version_id` bigint(20) unsigned DEFAULT NULL COMMENT '迭代id',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `idx_version_ui_case` (`version_id`,`case_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='版本迭代-UI用例中间表';

CREATE TABLE `exile5_test_module_app` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `module_name` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '模块应用名称',
  `module_type` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '模块应用名称类型(暂时未用上)',
  `module_code` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '模块应用名称类型',
  `module_source` varchar(512) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '模块应用来源',
  `case_list` json DEFAULT NULL COMMENT '用例id列表',
  `scenario_list` json DEFAULT NULL COMMENT '场景id列表',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `module_code` (`module_code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='功能模块与应用';

CREATE TABLE `exile5_test_project` (
  `project_name` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '项目名称',
  `project_auth` json DEFAULT NULL COMMENT '是否公开:1-是;0-否',
  `project_user` json DEFAULT NULL COMMENT '项目用户:project_auth为是的情况下使用',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_name` (`project_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目表';

CREATE TABLE `exile5_test_project_version` (
  `version_name` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '版本名称',
  `version_number` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '版本号',
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `icon` varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'Icon',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='项目版本迭代表';

CREATE TABLE `exile5_test_variable` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `var_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '变量名称',
  `var_init_value` json NOT NULL COMMENT '初始变量值',
  `var_value` json NOT NULL COMMENT '当前变量值',
  `var_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '变量值的类型:Str;Int;Json;JsonStr;List;ListStr',
  `var_args` json DEFAULT NULL COMMENT '函数变量扩展参数',
  `var_source` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '值来源:resp_data;resp_header',
  `var_get_key` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '值对应的key(用于关系变量获取)',
  `expression` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '取值表达式',
  `is_source` tinyint(1) unsigned DEFAULT NULL COMMENT '是否关系变量(主要用于前端标识):0-否;1-是',
  `is_expression` tinyint(1) unsigned DEFAULT NULL COMMENT '是否使用取值表达式:0-否;1-是',
  `is_active` tinyint(1) unsigned DEFAULT NULL COMMENT '是否每次更新(针对函数变量,在用例场景中):0-否;1-是',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `last_func` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上次最后使用的函数',
  `last_func_var` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '上次最后函数使用的值',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例变量';

CREATE TABLE `exile5_test_variable_history` (
  `var_id` bigint(20) unsigned DEFAULT NULL COMMENT '变量id',
  `update_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新类型',
  `before_var` json DEFAULT NULL COMMENT '修改前的值',
  `after_var` json DEFAULT NULL COMMENT '修改后的值',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例变量更新历史';

CREATE TABLE `exile5_test_version_task` (
  `version_id` bigint(20) unsigned DEFAULT NULL COMMENT '版本迭代id(冗余字段)',
  `task_name` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '任务名称',
  `task_type` varchar(128) COLLATE utf8mb4_bin NOT NULL COMMENT '任务类型',
  `user_list` json DEFAULT NULL COMMENT '参与人员',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='版本迭代任务表';

CREATE TABLE `exile5_timed_task` (
  `project_id` bigint(20) unsigned DEFAULT NULL COMMENT '项目id',
  `task_uuid` varchar(1024) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '任务UUID',
  `task_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '任务名称',
  `task_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '任务类型',
  `task_details` json DEFAULT NULL COMMENT '任务明细',
  `task_status` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '任务状态',
  `execute_type` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '执行类型',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='定时任务';

CREATE TABLE `exile5_ui_test_case` (
  `case_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用例名称',
  `case_status` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用例周期状态:active;dev;debug;over',
  `is_shared` tinyint(1) unsigned DEFAULT NULL COMMENT '0-仅创建者执行;1-共享执行',
  `is_public` tinyint(1) unsigned DEFAULT NULL COMMENT '是否公共使用:0-否;1-是',
  `total_execution` bigint(20) unsigned DEFAULT NULL COMMENT '执行次数总计',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `meta_data` json DEFAULT NULL COMMENT '业务树',
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` bigint(20) unsigned DEFAULT NULL COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='UI测试用例';




/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;