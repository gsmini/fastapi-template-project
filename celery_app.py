# coding:utf-8
from celery import Celery, Task
from src.config import CELERY_BROKER_URI
from celery.signals import worker_process_init, worker_process_shutdown
from src.models import db

"""
以前在使用flask的时候是这么封装celery的：
 class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    所以在flask环境下celery中直接使用orm是利用了flask的context会话隔离。
    但是fastapi是移步asgi方式不存在隔离之说，底层是dependece依赖注入方式。
如果在fastapi celery下直接使用salalchemy的orm会出现 query只能成功执行一次，后面总是无法查询命中数据，每次
重启celery才能又成功，是因为没有实现类似上面的隔离封装，所以下面的 SQLAlchemyTask 的意义也是实现类似ContextTask 会话上下文隔离回收

"""


class SQLAlchemyTask(Task):
    """Celery Task 基类，自动清理 SQLAlchemy Session"""

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db.remove()  # ✅ 每次任务结束后清理 session


def make_celery():
    celery = Celery("flastapi-template-project")
    celery.conf.update(
        {
            "broker_url": CELERY_BROKER_URI,
            "task_serializer": "json",
            "accept_content": ["json"]
        }
    )
    celery.autodiscover_tasks(["src.tasks"])
    celery.Task = SQLAlchemyTask  # ✅ 设置 Task 基类

    return celery


celery_app = make_celery()

# 根目录下执行启动：celery -A celery_app.celery_app  worker -l info   --loglevel=DEBUG
