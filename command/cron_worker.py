# -*- coding:utf-8 -*-
import time
import os
import sys
import schedule

from pathlib import Path

# 将项目根目录加入 Python 路径，确保能导入 src 模块
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 要在sys操作后 导入包
from src.libs.logging import logger
from src.models.user import User

CRON_TIME1 = os.getenv("CRON_TIME1", "02:00")


def schedule_task_demo():
    logger.info("执行定时任务成功")
    users = User.paginate()
    logger.info(users)


def start():
    logger.info("schedule worker is working...")

    # 每2秒执行一次
    schedule.every(2).seconds.do(schedule_task_demo)
    # 每一分钟执行一次
    schedule.every(1).minutes.do(schedule_task_demo)
    # 每天2点执行
    schedule.every().day.at("02:00").do(schedule_task_demo)
    # 每周一执行
    schedule.every().monday.do(schedule_task_demo)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start()
