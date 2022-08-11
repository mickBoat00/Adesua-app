from adesua.celery import app
from celery.utils.log import get_task_logger

from .email import send_course_approved_email

logger = get_task_logger(__name__)


@app.task(name="send_course_approved_email")
def send_course_approved_email(course_title, course_instructor):
    logger.info("Sent Course approved email.")
    return send_course_approved_email(course_title, course_instructor)
