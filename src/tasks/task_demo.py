from celery_app import celery_app
from src.models.user_feedback_record import UserFeedbackRecord

from src.libs.logging import logger


@celery_app.task
def task_demo(task_id):
    logger.info(f"测试任务成功  task_id {task_id}")
