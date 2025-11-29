# coding:utf-8
from celery import Celery, Task
from src.config import CELERY_BROKER_URI
from src.models import db
from celery.schedules import crontab

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

# 定时任务配置
beat_schedule = {
    # 示例 1：每 多少秒执行一次任务
    "beat_task_demo": {
        "task": "src.tasks.scheduled_tasks.beat_task_demo",  # 任务路径（包名.模块名.函数名）
        "schedule": 2,  # 间隔时间（单位：秒）→ 10 分钟
        "args": (),  # 任务参数（无则留空）
        "kwargs": {},
        "options": {"replace_existing": False}  # 重复启动时替换原有任务
    },

    # 示例 2：每天的15：50秒执行一次任务 timezone时区配置如果和业务系统不一致会导致任务时差！！
    "beat_task_demo2": {
        "task": "src.tasks.scheduled_tasks.beat_task_demo2",
        "schedule": crontab(minute="50", hour="15"),
        "args": (),
    }

}


class SQLAlchemyTask(Task):
    """Celery Task 基类，自动清理 SQLAlchemy Session"""

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db.remove()  # 每次任务结束后清理 session


def make_celery():
    app = Celery("flastapi-template-project")
    app.conf.update(
        {
            "broker_url": CELERY_BROKER_URI,
            "task_serializer": "json",
            "accept_content": ["json"],
            "timezone": "Asia/Shanghai"  # TODO: timezone时区配置如果和业务系统不一致会导致任务时差！！

        }
    )
    # 静态定时任务规则（启动后固定，如需动态可改用数据库）
    app.conf.beat_schedule = beat_schedule
    app.autodiscover_tasks(["src.tasks"])  # celery 任务目录
    app.Task = SQLAlchemyTask  # 设置 Task 基类

    return app


celery_app = make_celery()

# Celery Worker（消费任务）
# 根目录下执行启动：celery -A celery_app.celery_app  worker -l info   --loglevel=DEBUG
# Celery Beat（调度定时任务） 要注意的是beat定时任务是把task 推送到worker中让worker执行 也就是想要
# 使用beat必须使用worker
# celery -A celery_app beat --loglevel=INFO
