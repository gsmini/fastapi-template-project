from .task_demo import task_demo
from .email_send import task_email_send
from .scheduled_tasks import beat_task_demo, beat_task_demo2

__all__ = [
    "task_demo",
    "task_email_send",
    "beat_task_demo",
    "beat_task_demo2"

]
