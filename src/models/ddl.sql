CREATE DATABASE llm_email_process_agent;

CREATE TABLE `llm_email_process_agent`.`user`
(
    `id`           int          NOT NULL AUTO_INCREMENT COMMENT 'id autoIncrement',
    `username`     varchar(32)  NOT NULL DEFAULT '' COMMENT '用户名',
    `email`        varchar(32)  NOT NULL DEFAULT '' COMMENT 'email',
    `password`     varchar(256) NOT NULL DEFAULT '' COMMENT '密码',
    `is_stuff`     tinyint      NOT NULL DEFAULT '0' COMMENT '',
    `is_superuser` tinyint      NOT NULL DEFAULT '0' COMMENT '',
    `delete_flag`  tinyint      NOT NULL DEFAULT '0' COMMENT 'delete flag,0:normal,1:deleted',
    `create_time`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'CREATE TIME',
    `update_time`  timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `UNIQUE_username` (`username`),
    UNIQUE KEY `UNIQUE_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户信息表';



CREATE TABLE `llm_email_process_agent`.`user_feedback_type`
(
    `id`             int          NOT NULL AUTO_INCREMENT COMMENT 'id autoIncrement',
    `feedback_type`  varchar(64)  NOT NULL DEFAULT '' COMMENT '分类',
    `desc`           varchar(256) NOT NULL DEFAULT '' COMMENT '描述',
    `feedback_reply` text         NOT NULL   COMMENT '回复模版内容',
    `delete_flag`    tinyint      NOT NULL DEFAULT '0' COMMENT 'delete flag,0:normal,1:deleted',
    `create_time`    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'CREATE TIME',
    `update_time`    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `UNIQUE_feedback_type` (`feedback_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户反馈内容类型';


CREATE TABLE `llm_email_process_agent`.`user_feedback_record`
(
    `id`                int          NOT NULL AUTO_INCREMENT COMMENT 'id autoIncrement',
    `user_id`           int          NOT NULL DEFAULT 0 COMMENT '用户id',
    `user_email`        varchar(32)  NOT NULL DEFAULT '' COMMENT '用户邮箱',
    `title`             varchar(64)  NOT NULL DEFAULT '' COMMENT '用户反馈内容标题',
    `content`           varchar(256) NOT NULL DEFAULT '' COMMENT '用户反馈内容',
    `feedback_type`     varchar(64)  NOT NULL DEFAULT '' COMMENT '用户反馈内容分类用户提交',
    `feedback_type_llm` varchar(64)  NOT NULL DEFAULT '' COMMENT '用户反馈内容分类,大模型识别',
    `feedback_reply`    text         NOT NULL   COMMENT 'email回复内容',
    `status`            tinyint      NOT NULL DEFAULT '0' COMMENT '1创建待审核 2审核通过 3审核拒绝 4回复成功 5回复失败',
    `delete_flag`       tinyint      NOT NULL DEFAULT '0' COMMENT 'delete flag,0:normal,1:deleted',
    `create_time`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'CREATE TIME',
    `update_time`       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='用户反馈内容记录';

