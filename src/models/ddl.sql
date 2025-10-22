CREATE DATABASE fastapi_template_project;

CREATE TABLE `fastapi_template_project`.`user` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'id autoIncrement',
    `username` varchar(32) NOT NULL DEFAULT '' COMMENT '用户名',
    `password` varchar(32) NOT NULL DEFAULT '' COMMENT '密码',
    `delete_flag` tinyint NOT NULL DEFAULT '0' COMMENT 'delete flag,0:normal,1:deleted',
    `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'CREATE TIME',
    `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `UNIQUE_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户信息表';