from celery_app import celery_app
from src.libs.send_email import send, get_register_email_content
from src.libs.logging import logger


@celery_app.task
def task_email_send(request_id, email, code, send_to):
    """

    :param request_id: 请求处理的唯一id
    :param email: 接受者邮箱
    :param code: 验证码内容
    :param send_to: 接受者邮箱
    :return:
    """
    logger.info(f"start send email {email} code: {code}, request_id:{request_id}")
    content,subject = get_register_email_content(email, code)
    send(subject, content, send_to)
    logger.info(f"end send email {email} code: {code}, request_id:{request_id}")
