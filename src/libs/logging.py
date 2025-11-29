# -*- coding:utf-8 -*-
import logging
import os

from src.config import DEBUG

LOGGER_NAME = "fastapi-template-project"


def init_logger_handler():
    # 1. 获取自定义 logger（指定唯一名称，避免与 Celery 日志冲突）
    logger = logging.getLogger(LOGGER_NAME)

    # 2. 核心：禁用日志传播（防止被 Celery 父 logger 重复处理）
    logger.propagate = False

    # 3. 设置日志级别（DEBUG/INFO 由配置控制）
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # 4. 避免重复添加处理器（多次调用时防止多输出）
    if logger.handlers:
        return logger

    # 5. 控制台处理器（输出完整代码路径）
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    # 日志格式：替换 %(filename)s 为 %(pathname)s（显示绝对路径），保留行号等信息
    # 格式说明：
    # %(pathname)s: 完整代码路径（如 /project/src/agents/flow_agent_email.py）
    # %(lineno)d: 代码行号
    # %(funcName)s: 函数名（新增，可选，更清晰定位代码）
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(pathname)s:%(funcName)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # （可选）添加文件处理器（输出到日志文件，保留完整路径）
    #  下面可以注释掉 不过在llm项目中有利于我的本地日志定位
    # if not os.path.exists("logs"):
    #     os.makedirs("logs", exist_ok=True)
    # file_handler = logging.FileHandler(
    #     "logs/llm_email_process.log",
    #     encoding="utf-8"  # 避免中文乱码
    # )
    # file_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger


# 全局单例 logger（所有模块导入此实例，避免重复初始化）
logger = init_logger_handler()
