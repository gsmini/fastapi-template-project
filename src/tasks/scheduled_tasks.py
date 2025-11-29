from src.libs.logging import logger
from src.models.user import User
from celery_app import celery_app


@celery_app.task
def beat_task_demo():
    users = User.paginate()
    logger.info(users)


@celery_app.task
def beat_task_demo2():
    users = User.paginate()
    logger.info(users)
