-- -------------------------------------------------------------
-- TablePlus 2.8.2(257)
--
-- https://tableplus.com/
--
-- Database: ExilicTestPlatform
-- Generation Time: 2021-09-27 15:08:11.8840
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


CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `exilic_ass_bind` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `case_id` bigint(20) unsigned DEFAULT NULL COMMENT '用例id',
  `data_id` bigint(20) unsigned DEFAULT NULL COMMENT '数据id',
  `ass_resp_id_list` json DEFAULT NULL COMMENT 'resp断言规则list',
  `ass_field_id_list` json DEFAULT NULL COMMENT 'field断言规则list',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用例断言关系绑定';

CREATE TABLE `exilic_ass_field` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `assert_description` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '断言描述',
  `ass_json` json DEFAULT NULL COMMENT '断言',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='断言字段规则';

CREATE TABLE `exilic_ass_response` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `assert_description` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '断言描述',
  `ass_json` json DEFAULT NULL COMMENT '断言',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='断言返回值规则';

CREATE TABLE `exilic_auth_admin` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `username` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '用户名称',
  `_password` varchar(256) COLLATE utf8mb4_bin NOT NULL COMMENT '用户密码',
  `phone` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '手机号',
  `mail` varchar(128) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '邮箱',
  `code` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '用户编号',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台用户表';

CREATE TABLE `exilic_auth_api_resource` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Api资源表';

CREATE TABLE `exilic_auth_mid_admin_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `admin_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `role_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  PRIMARY KEY (`id`),
  KEY `idx_admin_role` (`admin_id`,`role_id`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户角色中间表';

CREATE TABLE `exilic_auth_mid_permission_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `permission_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `role_id` bigint(20) unsigned DEFAULT NULL COMMENT '后台用户id',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  PRIMARY KEY (`id`),
  KEY `idx_role_permission` (`role_id`,`permission_id`,`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='权限角色中间表';

CREATE TABLE `exilic_auth_permission` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '权限名称',
  `resource_id` bigint(20) unsigned DEFAULT NULL COMMENT 'ServerApi或WebRoute对应ec_crm_resource表',
  `resource_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT 'SERVER_API-接口;WEB_ROUTE-页面路由',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台权限表';

CREATE TABLE `exilic_auth_role` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL COMMENT '角色名称',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='后台角色表';

CREATE TABLE `exilic_auth_route_resource` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='Route资源表';

CREATE TABLE `exilic_test_case` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `case_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用户名称',
  `request_method` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '请求方式:GET;POST;PUT;DELETE',
  `request_url` varchar(2048) COLLATE utf8mb4_bin NOT NULL COMMENT '请求URL',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `is_pass` int(11) DEFAULT NULL COMMENT '0-不跳过;1-跳过',
  `total_execution` int(11) DEFAULT NULL COMMENT '执行次数总计',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例';

CREATE TABLE `exilic_test_case_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `data_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '用户名称',
  `request_params` json DEFAULT NULL COMMENT '请求参数',
  `request_headers` json DEFAULT NULL COMMENT 'headers',
  `request_body` json DEFAULT NULL COMMENT 'body',
  `request_body_type` tinyint(3) unsigned DEFAULT NULL COMMENT 'body请求参数类型:1-FormData;2-JsonData;3-X-FormData',
  `var_list` json DEFAULT NULL COMMENT '引用变量列表',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  `update_var_list` json DEFAULT NULL COMMENT '更新变量列表',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例参数';

CREATE TABLE `exilic_test_case_scenario` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `scenario_title` varchar(256) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '场景标题',
  `case_list` json DEFAULT NULL COMMENT '用例id列表按传参排序:[1,3,7,2...]',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例场景';

CREATE TABLE `exilic_test_databases` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '名称',
  `db_type` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '库类型',
  `db_connection` json DEFAULT NULL COMMENT '连接方式:直连,ssh,vpn...',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例-databases';

CREATE TABLE `exilic_test_env` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `env_url` varchar(2048) COLLATE utf8mb4_bin NOT NULL COMMENT '环境url',
  `env_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '环境名称',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试环境';

CREATE TABLE `exilic_test_variable` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间(结构化时间)',
  `create_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '创建时间(时间戳)',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间(结构化时间)',
  `update_timestamp` bigint(20) unsigned DEFAULT NULL COMMENT '更新时间(时间戳)',
  `is_deleted` tinyint(3) unsigned DEFAULT '0' COMMENT '0正常;其他:已删除',
  `status` tinyint(3) unsigned DEFAULT '1' COMMENT '状态',
  `var_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '变量名称',
  `var_value` json NOT NULL COMMENT '变量值',
  `var_type` tinyint(3) unsigned DEFAULT NULL COMMENT '变量值的类型:Str;Int;Json;JsonStr;List;ListStr',
  `var_source` tinyint(3) unsigned DEFAULT NULL COMMENT '值来源:1-resp_data;2-resp_header',
  `var_get_key` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '值对应的key(用于关系变量获取)',
  `creator` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '创建人',
  `creator_id` bigint(20) unsigned DEFAULT NULL COMMENT '创建人id',
  `modifier` varchar(32) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '更新人',
  `modifier_id` bigint(20) unsigned DEFAULT NULL COMMENT '更新人id',
  `remark` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='测试用例变量';




/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;