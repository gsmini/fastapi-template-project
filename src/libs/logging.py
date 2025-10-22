# -*- coding:utf-8 -*-
import logging

from src.config import DEBUG

LOGGER_NAME = "fastapi-template-project"


# 定义日志 输出代码行数等
def init_logger_handler():
    logger = logging.getLogger(LOGGER_NAME)

    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = init_logger_handler()
